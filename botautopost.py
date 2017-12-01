import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import config
from db_connect import write_to_base, read_from_base, create_table, truncate_all, delete_all

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def print_file_id(bot, update):
    # TODO implement this function
    update.message.reply_text("List of id's:\n" + ''.join(read_from_base()))


def send_document(bot, job):
    file_list = read_from_base(config.chat_id[job.context][1:])
    file_id = file_list[random.randint(0, len(file_list))][0]
    bot.send_document(config.chat_id[job.context], file_id)
    write_to_base(config.chat_id[job.context][1:], file_id, erase=True)
    job.context += 1
    if job.context == 5:
        job.context = 0


def start(bot, update, job_queue, chat_data):
    job = job_queue.run_repeating(send_document, interval=random.randint(config.time_s, config.time_e), first=0, context=0)
    chat_data['job'] = job


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def save_doc(bot, update):
    # TODO add categories by filename
    for c in config.chat_id:
        write_to_base(c[1:], update.message.document.file_id, erase=False)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def job_stop(bot, update, job_queue, chat_data):
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
    dp.add_handler(CommandHandler("ct", create_table))
    dp.add_handler(CommandHandler("tall", truncate_all))
    dp.add_handler(CommandHandler("all_del", delete_all))
    dp.add_handler(CommandHandler("stop", job_stop, pass_job_queue=True, pass_chat_data=True))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.document, save_doc))

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=config.port,
                          url_path=config.token)
    updater.bot.set_webhook("https://botautopost.herokuapp.com/" + config.token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

