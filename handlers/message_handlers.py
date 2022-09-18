import re

from telebot.async_telebot import AsyncTeleBot

import serialization
import weather
from handlers import forcast_history, logger
from keyboards import change_forcast_day, inline_keyboard_choose_city


def message_weather_handler(bot: AsyncTeleBot):
    @bot.message_handler(
        func=lambda message:
        message.text.startswith('Погода') or message.text.startswith('погода')
    )
    async def send_weather(message):

        try:

            # Parse the message if it is current weather or forcast
            request = re.findall(r'[пП]огода (\D+)(\d*)', message.text)[0]

            assert request
            city, day = request
            base_error_msg = "Извините, Не удается найти прогноз по запросу."

            # Validate day.
            if day:
                try:
                    day = int(day)
                    serialization.ValidDay(day=day)
                except Exception as e:
                    logger.error(f"message_weather_handler: "
                                 f"Validate day: Invalid day={day}. {e}")
                    await bot.send_message(message.chat.id,
                                           base_error_msg)
                    return None

            # Get coordinates by city name.
            geocoding = weather.get_geocoding(city=city)
            if not geocoding:
                logger.error(f"message_weather_handler: "
                             f"Can not get geocoding info for city= {city}")
                await bot.send_message(message.chat.id,
                                       base_error_msg)
                return None
            # If there is only one city with this name.
            if len(geocoding) == 1:
                city_lon = round(geocoding[0].lon, 4)
                city_lat = round(geocoding[0].lat, 4)

                # If it is weather forcast request.
                if city and day:
                    forcast = weather.get_weather_forcast_day_api(lon=city_lon,
                                                                  lat=city_lat)

                    # Add forcast to dictionary
                    logger.debug(f"message_weather_handler:"
                                 f"Change forcast dictionary "
                                 f"(handlers/__init__.py)"
                                 f"key={message.chat.id}, value={forcast}")
                    forcast_history[message.chat.id] = forcast

                    if not forcast:
                        logger.error(f"message_weather_handler: "
                                     f"Can not get forcast for city={city}")
                        await bot.send_message(message.chat.id,
                                               base_error_msg)
                        return None
                    msg = forcast.get(day)
                    if msg:
                        markup = change_forcast_day.change_forcast_day(
                            day=day,
                            lon=round(city_lon, 4),
                            lat=round(city_lat, 4)
                        )
                        logger.debug(f"message_weather_handler:"
                                     f"Send forcast for city={city}, "
                                     f"day={day}")
                        await bot.send_message(message.chat.id,
                                               msg,
                                               reply_markup=markup,
                                               parse_mode='HTML')
                        return None
                    else:
                        logger.debug(f"message_weather_handler:"
                                     f"Can not get msg=forcast.get(day), "
                                     f"city={city}, day={day}")
                        await bot.send_message(message.chat.id,
                                               base_error_msg)
                        return None

                # If it is current weather request
                elif city:

                    msg = weather.get_current_weather_api(lon=city_lon,
                                                          lat=city_lat)

                    logger.debug(f"message_weather_handler:"
                                 f"Send current weather for city={city}")
                    await bot.send_message(message.chat.id,
                                           msg,
                                           parse_mode='HTML')
                    return None

                else:
                    logger.error(f"message_weather_handler:"
                                 f"Error - not city ({city}) and day={day}")
                    await bot.send_message(message.chat.id,
                                           base_error_msg)
                    return None

            # If there are multiple cities with this name
            else:

                # Define function - get current weather or forcast
                if city and day:
                    function_type = f'gfw-{day}'
                elif city:
                    function_type = 'gcv'
                else:
                    logger.error(f"message_weather_handler:"
                                 f"Multiple cities with the same name:"
                                 f"Can not define city and day:"
                                 f" city={city}, day={day}")
                    function_type = ''

                markup = inline_keyboard_choose_city.create_city_choice(
                    function_shortname=function_type,
                    city_list=geocoding
                )
                logger.debug("message_weather_handler:"
                             "Send list with cities with the same name.")
                await bot.send_message(message.chat.id,
                                       "<b>Несколько городов "
                                       "с таким названием, "
                                       "выберите нужный:</b>",
                                       reply_markup=markup,
                                       parse_mode='HTML'
                                       )
                return None

        except Exception as e:
            logger.error(e)
            await bot.reply_to(message, 'Не могу найти погоду. '
                                        'Попробуйте еще раз. '
                                        'Прогноз доступен '
                                        'на пять дней вперед.')
            return None
