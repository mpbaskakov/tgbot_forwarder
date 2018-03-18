from random import randrange, randint
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
    file_list = read_from_base(config.chat_id[job.context[0]][1:])
    job.context[1] += 1
    if job.context[0] == 4:
        return
    if not file_list:
        pass
    else:
        file_id = file_list[randint(0, len(file_list) - 1)][0]
        bot.send_document(config.chat_id[job.context[0]], file_id)
        write_to_base(config.chat_id[job.context[0]][1:], file_id, erase=True)
    job.context[0] += 1
    if job.context[0] == 4:
        job.context[0] = 0


def start(bot, update, job_queue, chat_data, args):
    if args:
        job = job_queue.run_repeating(send_document, interval=config.post_int, first=0, context=int(args[0])-1)
    else:
        job = job_queue.run_repeating(send_document, interval=config.post_int, first=0, context=0)
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


def job_stop(bot, update, job_queue):
    job_queue.schedule_removal()


def rewrite(bot, update):
    rows = read_from_base(config.chat_id[-1][1:])
    truncate_all(bot, update)
    for c in config.chat_id:
        for row in rows:
            write_to_base(c[1:], row[0], erase=False)


def count_time(bot, update):
    file_count = []
    for c in config.chat_id:
        file_count.append(len(read_from_base(c[1:])))
    file_count_h = [round(f*config.post_int*len(file_count)/8, 2) for f in file_count]
    file_count_d = [round(f*config.post_int*len(file_count)*3, 2) for f in file_count]
    update.message.reply_text("Time left:\n {}\n {}".format(str(file_count_h), str(file_count_d)))


def count_max():
    file_count = []
    for c in config.chat_id:
        file_count.append(len(read_from_base(c[1:])))
    max_files_index = file_count.index(max(file_count))
    return int(max_files_index)


def show_jobs(bot, update, job_queue):
    update.message.reply_text(str(job_queue.jobs()[0]))


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True, pass_chat_data=True, pass_args=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", print_file_id))
    dp.add_handler(CommandHandler("ct", create_table))
    dp.add_handler(CommandHandler("tall", truncate_all))
    dp.add_handler(CommandHandler("all_del", delete_all))
    dp.add_handler(CommandHandler("re", rewrite))
    dp.add_handler(CommandHandler("jobs", show_jobs, pass_job_queue=True))
    dp.add_handler(CommandHandler("count", count_time))
    dp.add_handler(CommandHandler("stop", job_stop, pass_job_queue=True))
    dp.add_handler(MessageHandler(Filters.document, save_doc))

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=config.port,
                          url_path=config.token)
    updater.bot.set_webhook("https://botautopost.herokuapp.com/" + config.token)

    job_queue = updater.job_queue
    channel_id = count_max()
    job = job_queue.run_repeating(send_document, interval=config.post_int, first=0, context=[channel_id, 0])


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

