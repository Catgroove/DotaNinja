from app import app
from flask import url_for
from .models import Player, DoesNotExist
from .helpers import json_file_to_dict
from config import JSON_DIR

import datetime
import arrow
import os

@app.template_filter("game_mode")
def game_mode(mode_id):
    return json_file_to_dict(os.path.join(JSON_DIR, "game_mode.json"))[str(mode_id)]["name"]


@app.template_filter("region")
def region(cluster):
    regions = json_file_to_dict(os.path.join(JSON_DIR, "regions.json"))["regions"]
    for region, values in regions.items():
        if values.get("clusters") and str(cluster) in values.get("clusters"):
            return (values["display_name"][len("#dota_region_"):].capitalize())


@app.template_filter("duration")
def duration(duration):
    return str(datetime.timedelta(seconds=duration))


@app.template_filter("time_since")
def time_since(time):
    return arrow.get(time).humanize()


@app.template_filter("result")
def result(result):
    if result:
        return "Won"
    return "Lost"


@app.template_filter("hero_image")
def hero_image(hero_id):
    return url_for("static", filename="assets/heroes/{}_sb.png".format(hero_id))


@app.template_filter("item_image")
def item_image(item_id):
    return url_for("static", filename="assets/items/{}_lg.png".format(item_id))


@app.template_filter("player_name")
def player_name(account_id):
    try:
        return Player.get(Player.account_id == account_id).personaname
    except DoesNotExist:
        return account_id
