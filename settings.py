import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPEN_WEATHER_TOKEN = os.environ.get("OPENWEATHER_TOKEN")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
