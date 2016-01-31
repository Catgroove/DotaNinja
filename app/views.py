from flask import abort, flash, g, session, redirect, render_template, \
    request, url_for
from flask.ext.paginate import Pagination
from app import app, api, db, oid
from .models import Match, MatchPlayer, Player, DoesNotExist, IntegrityError
from .helpers import json_file_to_dict, dict_to_json_file, \
    convert_to_32_bit
from .filters import *
from config import JSON_DIR

import tasks
import datetime
import os
import re


@app.before_request
def before_request():
    g.db = db
    g.db.connect()
    g.user = None
    if "account_id" in session:
        g.user = Player.get(Player.account_id == session["account_id"])


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route("/login")
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    return oid.try_login("http://steamcommunity.com/openid")


@oid.after_login
def create_or_login(resp):
    match = re.compile(
        "steamcommunity.com/openid/id/(.*?)$").search(resp.identity_url)
    query = api.get_player_summaries(match.group(1))
    if query["response"]["players"]:
        steamdata = query["response"]["players"][0]
    else:
        abort(404)

    player, created = Player.get_or_create(
        account_id=convert_to_32_bit(int(steamdata["steamid"])),
        defaults=steamdata)

    # update variable information if player exists
    if player:
        g.user = player
        g.user.avatar = steamdata["avatar"]
        g.user.avatarmedium = steamdata["avatarmedium"]
        g.user.avatarfull = steamdata["avatarfull"]
        g.user.personaname = steamdata["personaname"]
    else:
        g.user = created

    g.user.last_login = datetime.datetime.now()
    g.user.save()

    session["account_id"] = g.user.account_id

    tasks.get_all_matches.delay(g.user.account_id)

    flash("You are now logged in as {}".format(g.user.personaname))
    return redirect(oid.get_next_url())


@app.route("/logout")
def logout():
    session.pop("account_id", None)
    flash("You are now logged out.")
    return redirect(url_for("index"))


@app.route("/")
def index():
    if session.get("account_id"):
        return redirect(url_for("player_page", account_id=session.get("account_id")))
    return render_template("index.html")


@app.route("/players/<int:account_id>")
def player_page(account_id):
    try:
        player = Player.get(Player.account_id == account_id)
    except DoesNotExist:
        abort(404)
    return render_template("player.html", player=player)


@app.route("/matches/<int:match_id>")
def render_match(match_id=None):
    try:
        match = Match.get(Match.match_id == match_id)
    except DoesNotExist:
        return redirect(url_for("add_match", match_id=match_id))
    return render_template("match.html", match=match, match_id=match_id)


@app.route("/add", methods=["POST", "GET"])
@app.route("/add/<int:match_id>", methods=["POST", "GET"])
def add_match(match_id=None):
    if request.method == "POST":
        match = tasks.add_match.delay(match_id)
        if match.get() == True:
            return redirect(url_for("render_match", match_id=match_id))


@app.route("/players/<int:account_id>/matches", defaults={"page": 1})
@app.route("/players/<int:account_id>/matches/<int:page>")
def list_matches(account_id, page):
    try:
        matches = MatchPlayer.select(Match, MatchPlayer).join(Match).where(MatchPlayer.account_id == account_id).order_by(Match.start_time.desc())
    except DoesNotExist:
        matches = {}

    PER_PAGE = 20
    DISPLAY_MSG = "Showing {start} to {end} of {total} entries."

    pagination = Pagination(page=page, total=matches.count(), bs_version=3, per_page=PER_PAGE, display_msg=DISPLAY_MSG)
    return render_template("matches.html", matches=matches.paginate(page, PER_PAGE), pagination=pagination)


@app.route("/heroes", methods=["POST", "GET"])
def list_heroes():
    if request.method == "POST":
        tasks.update_heroes.delay()
    heroes = json_file_to_dict(os.path.join(JSON_DIR, "heroes.json"))["result"]["heroes"]
    return render_template("heroes.html", heroes=heroes)


@app.route("/items", methods=["POST", "GET"])
def list_items():
    if request.method == "POST":
        tasks.update_items.delay()
    items = json_file_to_dict(os.path.join(JSON_DIR, "items.json"))["result"]["items"]
    return render_template("items.html", items=items)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
