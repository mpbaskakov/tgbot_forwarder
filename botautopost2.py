import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def load_file_id():
    list_of_files = []
    with open('list.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            list_of_files.append(line.strip('\n'))
    return list_of_files


def print_file_id(bot, update):
    with open('list.txt', 'r') as f:
        update.message.reply_text("List of id's:\n" + f.read())


def send_document(bot, update):
    list_of_files = load_file_id()
    bot.send_document(config.chat_id, list_of_files[0])
    list_of_files.remove(list_of_files[0])
    with open('list.txt', 'w') as file:
        for f in list_of_files:
            file.write(f + '\n')


def start(bot, update, job_queue, chat_data):
    job = job_queue.run_repeating(send_document, interval=random.randint(2000, 4000), first=0)
    chat_data['job'] = job


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def save_doc(bot, update):
    with open('list.txt', 'a') as f:
        f.write(update.message.document.file_id + '\n')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def job_stop(bot, update, job_queue, chat_data):
    print(chat_data)
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']



def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.token)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", print_file_id))
    dp.add_handler(CommandHandler("stop", job_stop, pass_job_queue=True, pass_chat_data=True))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.document, save_doc))

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get('PORT', '5000')),
                          url_path=config.token)
    updater.bot.set_webhook("https://botautopost.herokuapp.com/" + config.token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

