from telebot import types

import serialization
from keyboards import logger


def change_forcast_day(day: int,
                       lon: float,
                       lat: float) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    try:
        serialization.ValidDay(day=day - 1)
    except Exception:
        left_button = types.InlineKeyboardButton(text='',
                                                 callback_data='error')
    else:
        left_button = types.InlineKeyboardButton(
            text=f"\u2b05 {day - 1} число",
            callback_data=f"chd {day - 1} {lon} {lat}"  # previous forcast
        )

    try:
        serialization.ValidDay(day=day + 1)
    except Exception:
        right_button = types.InlineKeyboardButton(text='',
                                                  callback_data='error')
    else:
        right_button = types.InlineKeyboardButton(
            text=f"\u27a1 {day + 1} число",
            callback_data=f"chd {day + 1} {lon} {lat}"  # next forcast
        )

    markup.add(left_button, right_button)
    logger.debug(f"Create keyboard markup: {markup}")
    return markup
