from telebot.async_telebot import AsyncTeleBot


def command_help(bot: AsyncTeleBot):
    @bot.message_handler(commands=['help', ])
    async def send_help(message):
        await bot.reply_to(message, "1. 'погода <город>' - "
                                    "узнать текущую погоду;\n"
                                    "2. 'погода <город> <число>' - "
                                    "погода на число "
                                    "(доступно на 5 дней вперед).\n"
                           )
        return None

    @bot.message_handler(commands=['start', ])
    async def send_start(message):
        msg = "<b>погодный бот:</b>\n" \
              "1. 'погода город' - узнать текущую погоду;\n" \
              "2. 'погода город число' - погода на число " \
              "(доступно на 5 дней вперед).\n"
        await bot.reply_to(message, msg, parse_mode='HTML')
        return None
