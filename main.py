from telebot import TeleBot

import settings
from handlers import callback_handlers, command_handlers, message_handlers

# Add bot instance
token = settings.TELEGRAM_BOT_TOKEN
assert token
bot = TeleBot(token)

# Add command handlers
command_handlers.command_help(bot)

# Add message handlers
message_handlers.message_weather_handler(bot)

# Add callback handlers
callback_handlers.callback_handler(bot)

if __name__ == "__main__":
    bot.infinity_polling()
