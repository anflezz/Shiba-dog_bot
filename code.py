#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

TOKEN = 'token'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('I know a lot of dogs')

def howmany(update, context):
    update.message.reply_text('How many dogs?')
    return 0

def help(update, context):
    logging.info(f'user: {update.message.chat.username} send command help')
    update.message.reply_text('''I can show you as many dogs as you want
Insert /wantDog to see them
Insert /WhereAreAllDogs to know where are all shiba-dogs
Insert /start to know what i know''')

def kuda(update, context):
    update.message.reply_text('I have them')

def wantDog(update, context):
    s = update.message.text
    if s.isdigit() == False:
      update.message.reply_text('Insert only a number, please')
    else:
      y=f'http://shibe.online/api/shibes?count={s}&urls=true&httpsUrls=true'
      response = requests.get(y)
      x=response.content.decode()
      o=json.loads(x)
      for u in o:
        update.message.reply_photo(u)
      return ConversationHandler.END


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text('Bye! I hope we can talk again some day.',
                             )
    return ConversationHandler.END


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("WhereAreAllDogs", kuda))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('wantDog', howmany)],

        states={
            0: [MessageHandler(Filters.text, wantDog)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
    logging.info('Start bot!')
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
