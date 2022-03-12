# -*- coding: utf8 -*-
from telegram.ext import Updater, CommandHandler, dispatcher, MessageHandler
from telegram.ext.filters import Filters
from bot.message_handlers import handle_get_favourite, handle_clear_favourite, handle_get_rates, handle_message,  handle_start, handle_sticker
import sys
import logging
import config

#initializing the bot 
try:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    updater = Updater(token=config.TOKEN, use_context=True)
    dispatcher = updater.dispatcher
                    
    #adding handlers
    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    sticker_handler = MessageHandler(Filters.sticker & (~Filters.command & ~Filters.text), handle_sticker)
    start_handler = CommandHandler("start", handle_start)
    get_rates_handler = CommandHandler("getrates", handle_get_rates)
    get_favourite_handler = CommandHandler("getfavourite", handle_get_favourite)
    clear_favourite = CommandHandler("clearfavourite", handle_clear_favourite)

#adding handlers to react on user's messages
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(sticker_handler)
    dispatcher.add_handler(get_rates_handler)
    dispatcher.add_handler(get_favourite_handler)
    dispatcher.add_handler(clear_favourite)
    
    #RUN
    updater.start_polling()
    
except Exception as err:
    print(f"The bot stopped. Reason: {err}")
    updater.stop()
    sys.exit()