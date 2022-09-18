from typing import List

from telebot import types

from keyboards import logger
from serialization import ValidCityInstance


def create_city_choice(function_shortname: str,
                       city_list: List[ValidCityInstance]
                       ) -> types.InlineKeyboardMarkup:

    markup = types.InlineKeyboardMarkup(row_width=1)

    for city in city_list:
        button = types.InlineKeyboardButton(
            text=f"{city.city.capitalize()} - "
                 f"{city.country} область: {city.state}",
            callback_data=f"{function_shortname} "
                          f"{round(city.lon, 4)} "
                          f"{round(city.lat, 4)}"
        )
        markup.add(button)

    logger.debug(f"Create keyboard markup: {markup}")
    return markup
