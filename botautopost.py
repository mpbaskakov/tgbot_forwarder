import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import config
from db_connect import write_to_base, read_from_base

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def print_file_id(bot, update):
    update.message.reply_text("List of id's:\n" + read_from_base())


def send_document(bot, update):
    file_id = read_from_base()[0][0]
    bot.send_document(config.chat_id, file_id)
    write_to_base(file_id, erase=True)


def start(bot, update, job_queue, chat_data):
    job = job_queue.run_repeating(send_document, interval=random.randint(2000, 4000), first=0)
    chat_data['job'] = job


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def save_doc(bot, update):
    write_to_base(update.message.document.file_id, erase=False)


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

