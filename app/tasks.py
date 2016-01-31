from app import api, celery, db
from pydota import PyDotaError, download_hero_image, download_item_image
from models import DoesNotExist, IntegrityError, Match, MatchPlayer
from helpers import dict_to_json_file
from config import JSON_DIR, HERO_IMG_DIR, ITEM_IMG_DIR
import os
import urllib


@celery.task(rate_limit="1/s") #  limit as per Valve's specification
def add_match(match_id):
    """Queries a match from the Steam API and adds it to the database.
    Returns True if it succeeds or if match already exists, or False if it fails.
    """
    match = api.get_match_details(match_id)["result"]

    if "error" in match:
        return False

    try:
        new_match = Match.create(**match)
    except IntegrityError:
        return True
    except PyDotaError:
        return False

    player_list = [dict(match_id=new_match.match_id, **player) for player in match["players"]]

    with db.atomic():
        MatchPlayer.insert_many(player_list).execute()

    return True


@celery.task()
def get_all_matches(account_id):
    """Try to retrieve and add all matches from a player to the database."""
    matches = api.get_match_history(account_id=account_id)["result"]
    while matches["results_remaining"] >= 0 and matches["num_results"] > 1:
        for match in matches["matches"]:
            try:
                Match.get(Match.match_id == match["match_id"])
            except DoesNotExist:
                new_match_task = add_match.delay(match["match_id"])
        matches = api.get_match_history(account_id=account_id, start_at_match_id=match["match_id"])["result"]


@celery.task()
def update_heroes():
    """Update the list of heroes and download the images."""
    heroes = api.get_heroes()
    dict_to_json_file(heroes, os.path.join(JSON_DIR, "heroes.json"))
    for hero in heroes["result"]["heroes"]:
        download_hero_image(hero["name"][14:], "sb", os.path.join(HERO_IMG_DIR, str(hero["id"])+"_sb.png"))
        download_hero_image(hero["name"][14:], "lg", os.path.join(HERO_IMG_DIR, str(hero["id"])+"_lg.png"))


@celery.task()
def update_items():
    """Update the list of items and download the images."""
    items = api.get_game_items()
    dict_to_json_file(items, os.path.join(JSON_DIR, "items.json"))
    for item in items["result"]["items"]:
        download_item_image(item["name"][5:], os.path.join(ITEM_IMG_DIR, str(item["id"])+"_lg.png"))
