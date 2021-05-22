import logging

import requests
import telebot
from telegram import Update, ForceReply, bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging

from cowin import vaccine_notifers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = "1754468723:AAHFqk7AX7OAkSiw7V53OIhuU9GmLhlz7nE";
CHATID = "-409554185"
age =1;
keyboard = [
    [
        InlineKeyboardButton('18-44', callback_data='1'),
        InlineKeyboardButton('45+', callback_data='2')
    ]
]
# Define a few command handlers. These usually take the two arguments update and
# context.


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text("Here are the values of stringList", reply_markup=InlineKeyboardMarkup(keyboard))


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    pincode= update.message.text
    slotAvailable = vaccine_notifers(update.message.text, age);
    update.message.reply_text(slotAvailable+str(age)+str(pincode), reply_markup=InlineKeyboardMarkup(keyboard))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    print(update)
    chat_id= query.message.chat.id
    query.answer()

    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data
    # Now u can define what choice ("callback_data") do what like this:
    if choice == '1':
        global age
        age=1;
        # slotAvailable = vaccine_notifers(431005);
        # # update.(slotAvailable)
        # base_url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + CHATID + '&text={0}'.format(
        #     slotAvailable)
        # requests.get(base_url)
    elif choice == '2':
        age=2;
        # slotAvailable = vaccine_notifers(390001);
        # base_url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + CHATID + '&text={0}'.format(
        #     slotAvailable)
        # requests.get(base_url)
        # update.message.reply_to_message(slotAvailable)
    pinCodeMessage='Kindly enter your Pincode'
    base_url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + str(chat_id) + '&text={0}'.format(
        pinCodeMessage)
    requests.get(base_url)


if __name__ == '__main__':
    main()
