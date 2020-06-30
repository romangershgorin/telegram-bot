from telegram.ext import Updater
from telegram.ext import CommandHandler
import table_parser


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="I'm a bot, please talk to me!")


def check_district(update, context):
    result = table_parser.check_district()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Smolensk is {}found in the list'.format('' if result else 'not '))


def get_all_districts(update, context):
    districts = table_parser.get_processed_districts()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=districts)


print('Selflogs: starting...')
updater = Updater(token='1342737629:AAGW0mpQUPC5Kl699f7O1cNYj7Qd7c5SL4w', use_context=True)
start_handler = CommandHandler('start', start)
check_district_handler = CommandHandler('check', check_district)
all_districts_handler = CommandHandler('all', get_all_districts)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(check_district_handler)
dispatcher.add_handler(all_districts_handler)


updater.start_polling()
