from telebot import TeleBot


def command_help(bot: TeleBot):
    @bot.message_handler(commands=['help', ])
    def send_help(message):
        bot.reply_to(message, "1. 'погода <город>' - "
                              "узнать текущую погоду;\n"
                              "2. 'погода <город> <число>' - "
                              "погода на число "
                              "(доступно на 5 дней вперед).\n"
                     )
        return None

    @bot.message_handler(commands=['start', ])
    def send_start(message):
        msg = "<b>погодный бот:</b>\n" \
              "1. 'погода город' - узнать текущую погоду;\n" \
              "2. 'погода город число' - погода на число " \
              "(доступно на 5 дней вперед).\n"
        bot.reply_to(message, msg, parse_mode='HTML')
        return None
