from flask import Flask
from flask.ext.openid import OpenID
from peewee import SqliteDatabase
from config import API_KEY
from pydota import PyDota
from celery import Celery


app = Flask(__name__)
app.config.from_object("config")
db = SqliteDatabase("dotaninja.db")
api = PyDota(API_KEY)
oid = OpenID(app)
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

from app import models, views
