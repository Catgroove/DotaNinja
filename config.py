# Set application directories
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_DIR = os.path.join(BASE_DIR, "app/json")
HERO_IMG_DIR = os.path.join(BASE_DIR, "app/static/assets/heroes")
ITEM_IMG_DIR = os.path.join(BASE_DIR, "app/static/assets/items")

# Connection settings
debug = True
port = 8080
host = "127.0.0.1"

# Celery config
CELERY_BROKER_URL="redis://localhost:6379"
CELERY_RESULT_BACKEND="redis://localhost:6379"

# Keys
SECRET_KEY = ""
API_KEY = ""
