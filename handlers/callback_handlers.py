from telebot import TeleBot

import serialization
import weather
from handlers import forcast_history, logger
from keyboards import change_forcast_day


def callback_handler(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler_function(call):

        logger.debug(f"callback_handler_function: Get callback {call}")
        response: str = call.data
        parent_msg = call.message
        data = response.split()

        try:

            # If function = get_current_weather
            if data[0] == "gcv":
                lon = float(data[1])
                lat = float(data[2])
                msg = weather.get_current_weather_api(lat=lat, lon=lon)
                logger.debug("callback_handler: "
                             "send current weather.")
                bot.send_message(parent_msg.chat.id,
                                 msg,
                                 parse_mode='HTML'
                                 )
                return None

            # If function = get_weather_forcast
            elif data[0].startswith("gfw"):
                day = int(data[0].split("-")[1])
                lon = float(data[1])
                lat = float(data[2])

                # Validate day
                try:
                    serialization.ValidDay(day=day)
                except Exception as e:
                    logger.error(f"callback_handler: "
                                 f"Validate day: Invalid day={day}. {e}")
                    bot.send_message(parent_msg.chat.id,
                                     'Не могу найти прогноз. '
                                     'Попробуйте еще раз.')
                    return None
                forcast = weather.get_weather_forcast_day_api(lat=lat,
                                                              lon=lon)
                # Add forcast to dictionary
                logger.debug(f"callback_handler:"
                             f"Change forcast dictionary "
                             f"(handlers/__init__.py)"
                             f"key={parent_msg.chat.id}, value={forcast}")
                forcast_history[parent_msg.chat.id] = forcast

                if not forcast:
                    logger.error("callback_handler: "
                                 "Can not get forcast for city")
                    bot.send_message(parent_msg.chat.id,
                                     'Не могу найти прогноз. '
                                     'Попробуйте еще раз.')
                    return None

                msg = forcast.get(day)
                if msg:
                    markup = change_forcast_day.change_forcast_day(
                        day=day,
                        lon=round(lon, 4),
                        lat=round(lat, 4)
                    )
                    logger.debug(f"callback_handler:"
                                 f"Send forcast for city. day={day}")
                    bot.send_message(parent_msg.chat.id,
                                     msg,
                                     reply_markup=markup,
                                     parse_mode='HTML'
                                     )
                    return None
                else:
                    logger.debug(f"callback_handler:"
                                 f"Can not get msg=forcast.get(day), "
                                 f"city, day={day}")
                    bot.send_message(parent_msg.chat.id,
                                     'Не могу найти прогноз. '
                                     'Попробуйте еще раз.')
                    return None

            # If function = change day forcast
            elif data[0].startswith("chd"):

                day = int(data[1])
                lon = float(data[2])
                lat = float(data[3])

                # Validate day
                try:
                    serialization.ValidDay(day=day)
                except Exception as e:
                    logger.error(f"callback_handler: "
                                 f"Validate day: Invalid day={day}. {e}")
                    bot.send_message(parent_msg.chat.id,
                                     'Прогноз доступен '
                                     'на пять дней вперед. '
                                     'Попробуйте еще раз.')
                    return None

                # Try to ask handlers.__init__ dict for the data
                chat_id = parent_msg.chat.id
                if chat_id in forcast_history:
                    forcast = forcast_history[chat_id].get(day)
                    if forcast:
                        msg = forcast
                        markup = change_forcast_day.change_forcast_day(
                            day=day,
                            lon=round(lon, 4),
                            lat=round(lat, 4)
                        )
                        logger.debug("callback_handler: "
                                     "Send forcast for day from global "
                                     "dictionary (__handlers/__init__)")

                        bot.edit_message_text(
                            text=msg,
                            message_id=parent_msg.message_id,
                            chat_id=parent_msg.chat.id,
                            reply_markup=markup,
                            parse_mode='HTML'
                        )
                        return None

                # Ask weather API for forcast
                else:
                    logger.debug("callback_handler: "
                                 "Can not find forcast for day from global "
                                 "dictionary (__handlers/__init__)")
                    forcast = weather.get_weather_forcast_day_api(lon=lon,
                                                                  lat=lat)
                    # Add forcast to dictionary
                    logger.debug(f"callback_handler:"
                                 f"Change forcast dictionary "
                                 f"(handlers/__init__.py)"
                                 f"key={parent_msg.chat.id}, value={forcast}")
                    forcast_history[parent_msg.chat.id] = forcast

                    if not forcast:
                        logger.error("callback_handler: "
                                     "Can not get forcast for city")
                        bot.send_message(
                            parent_msg.chat.id,
                            'Прогноз доступен на пять дней вперед. '
                            'Попробуйте еще раз.'
                        )
                        return None

                    msg = forcast.get(day)
                    if msg:
                        markup = change_forcast_day.change_forcast_day(
                            day=day,
                            lon=round(lon, 4),
                            lat=round(lat, 4)
                        )
                        logger.debug(f"callback_handler:"
                                     f"Send forcast for city, day={day}")
                        bot.send_message(parent_msg.chat.id,
                                         msg,
                                         reply_markup=markup,
                                         parse_mode='HTML'
                                         )
                        return None

                    else:
                        logger.debug(f"callback_handler:"
                                     f"Can not get msg=forcast.get(day), "
                                     f"city, day={day}")
                        bot.send_message(
                            parent_msg.chat.id,
                            'Прогноз доступен на пять дней вперед. '
                            'Попробуйте еще раз.'
                        )
                        return None

            else:
                logger.warning(f"callback_handler: "
                               f"unhandled data from callback  - do nothing. "
                               f"data= {data}")
                return None

        except Exception as e:
            logger.error(f"Error in callback answer {response} - {e}")
