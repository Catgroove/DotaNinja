from peewee import *
from app import db


class BaseModel(Model):
    class Meta(object):
        database = db


class Match(BaseModel):
    match_id = BigIntegerField(primary_key=True)
    match_seq_num = BigIntegerField()
    radiant_win = BooleanField()
    duration = IntegerField()
    start_time = IntegerField()
    tower_status_radiant = IntegerField()
    tower_status_dire = IntegerField()
    barracks_status_radiant = IntegerField()
    barracks_status_dire = IntegerField()
    cluster = IntegerField()
    first_blood_time = IntegerField()
    lobby_type = IntegerField()
    human_players = IntegerField()
    leagueid = IntegerField()
    positive_votes = IntegerField()
    negative_votes = IntegerField()
    game_mode = IntegerField()
    engine = IntegerField()


class MatchPlayer(BaseModel):
    match_id = ForeignKeyField(
        Match,
        on_delete="CASCADE",
        related_name="players"
    )
    account_id = BigIntegerField()
    player_slot = IntegerField()
    hero_id = IntegerField()
    item_0 = IntegerField()
    item_1 = IntegerField()
    item_2 = IntegerField()
    item_3 = IntegerField()
    item_4 = IntegerField()
    item_5 = IntegerField()
    kills = IntegerField()
    deaths = IntegerField()
    assists = IntegerField()
    leaver_status = IntegerField()
    gold = IntegerField()
    last_hits = IntegerField()
    denies = IntegerField()
    gold_per_min = IntegerField()
    xp_per_min = IntegerField()
    gold_spent = IntegerField()
    hero_damage = IntegerField()
    tower_damage = BigIntegerField()
    hero_healing = BigIntegerField()
    level = IntegerField()
    ability_upgrades = CharField()

    class Meta(object):
        primary_key = CompositeKey("match_id", "player_slot")


class Player(BaseModel):
    account_id = BigIntegerField(primary_key=True)
    steamid = CharField(max_length=32)
    avatar = CharField(max_length=255)
    avatarmedium = CharField(max_length=255)
    avatarfull = CharField(max_length=255)
    profileurl = CharField(max_length=255)
    personaname = CharField(max_length=255)
    last_login = DateTimeField(null=True)
