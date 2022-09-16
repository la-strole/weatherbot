import os
import re
import logging

import telebot

import weather
import serialization

# Add logger
logger = logging.getLogger('telegram_bot')
f_handler = logging.FileHandler('../log.txt')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
logger.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))

bot_token = os.getenv("BOT_TOKEN")

assert bot_token
bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=['help', ])
def send_help(message):
    bot.reply_to(message, "1. 'погода <город>' - узнать текущую погоду;"
                          "2. 'погода <город> <число>' - "
                          "погода на число (доступно на 5 дней вперед);\n"
                 )


@bot.message_handler(func=lambda message: message.text.startswith('Погода') or
                                          message.text.startswith('погода'))
def send_weather(message):
    # Parse the message if it is current weather or forcast
    request = re.findall(r'[пП]огода (\D+)(\d*)', message.text)[0]

    try:

        assert request
        city, day = request

        # If it is weather forcast
        if city and day:
            # Validate day
            valid_day = serialization.ValidDay(day=int(day))
            replay_text = weather.get_weather_forcast_day(city=city,
                                                          day=valid_day.day)
            if replay_text:
                logger.debug(f"Send weather forcast to city {city} "
                             f"day={day}")
                bot.reply_to(message, replay_text)
            else:
                err_msg = f"Не могу найти погоду для {city}. Попробуйте еще раз."
                logger.debug(f"Can not find weather forcast - "
                             f"city={city}, day={day}.")
                bot.reply_to(message, err_msg)

        # If it is current weather
        if city:
            replay_test = weather.get_current_weather(city=city)
            if replay_test:
                logger.debug(f"Send current weather for city {city}")
                bot.reply_to(message, replay_test)
            else:
                err_msg = f"Не могу найти погоду для {city}. Попробуйте еще раз."
                logger.debug(f"Can not send current weather for city {city}")
                bot.reply_to(message, err_msg)
        else:
            logger.debug(f"Wrong user request {request}")
            bot.reply_to(message, 'Не могу найти погоду. Попробуйте еще раз.')

    except (AssertionError, ValueError) as e:
        logger.error(e)
