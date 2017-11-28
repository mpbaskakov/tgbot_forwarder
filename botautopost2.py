from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import config
import time

PORT = int(os.environ.get('PORT', '5000'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def check_sended(file_id):
    list_of_files = []
    with open('list_sended.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            list_of_files.append(line.strip('\n'))
    print(list_of_files)
    if not list_of_files.count(file_id):
        return True
    return False


def save_sended(file_id):
    with open('list_sended.txt', 'a') as f:
        f.write(file_id + '\n')


def load_file_id():
    list_of_files = []
    with open('list.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            list_of_files.append(line.strip('\n'))
    return list_of_files


def print_file_id(message):
    with open('list.txt', 'rb') as f:
        bot.send_message(message.chat.id, f.read())


def start(bot, update):
    list_of_files = load_file_id()
    for file_id in list_of_files:
        print(file_id)
        if check_sended(file_id):
            bot.send_document(config.chat_id, file_id)
            save_sended(file_id)
            time.sleep(10)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def save_doc(message):
    list_of_files_id = []
    list_of_files_id.append(message.document.file_id)
    list_to_write = ''.join(list_of_files_id)
    with open('list.txt', 'a') as f:
        f.write(list_to_write + '\n')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", print_file_id))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.document, save_doc))

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=config.token)
    updater.bot.set_webhook("https://botautopost.herokuapp.com/" + config.token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

