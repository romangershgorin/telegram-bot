from telegram.ext import Updater
from telegram.ext import CommandHandler
import table_parser
import logging
import os


current_district_count = 0


def start(update, context):
    context.bot.send_message(
        chat_id=-448378877,
        text="Я умею искать города с одобренными больничными для 65+")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я умею искать города с одобренными больничными для 65+")


def check_district(update, context):
    result = table_parser.check_district()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Smolensk is {}found in the list'.format('' if result else 'not '))


def send_long_message(context, chat_id, message):
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            context.bot.send_message(chat_id, message[x:x+4096])
    else:
        context.bot.send_message(chat_id, message)


def get_all_districts(update, context):
    count, districts = table_parser.get_processed_districts()
    send_long_message(context, update.effective_chat.id, districts)


def callback(context):
    global current_district_count
    district_count, districts = table_parser.get_processed_districts()
    if current_district_count < district_count:
        send_long_message(context, -448378877, districts)
        context.bot.send_message(chat_id=-448378877, text=districts)
        current_district_count = district_count
    else:
        context.bot.send_message(chat_id=-448378877, text="No update yet :(")


def main():
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    PORT = os.environ.get('PORT', 8443)
    MODE = os.environ.get('MODE')
    TOKEN = '1342737629:AAGW0mpQUPC5Kl699f7O1cNYj7Qd7c5SL4w'

    logging.info('Starting bot...')

    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('check', check_district))
    updater.dispatcher.add_handler(CommandHandler('all', get_all_districts))
    
    job_queue = updater.job_queue
    job_queue.run_repeating(callback, 300)

    if MODE == 'HEROKU':
        logging.info('Setting up webhook...')
        updater.start_webhook(
            listen='0.0.0.0', 
            port=PORT, 
            url_path=TOKEN)
        updater.bot.set_webhook('https://zozman-telegram-bot.herokuapp.com/{}'.format(TOKEN))
    else:
        logging.info('Using long polling...')
        updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()