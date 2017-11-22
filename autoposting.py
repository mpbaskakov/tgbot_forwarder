from telegram.ext import Updater, CommandHandler
import logging
import config
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def scan_folder(folder):
    files = os.listdir(folder)
    list_of_files = []
    for f in files:
        if f.endswith('.mp4'):
            list_of_files.append(os.path.join(folder, f))
    return set(list_of_files)


def alarm(bot):
    """Send the alarm message."""
    list_of_files = scan_folder('gif')
    for f in list_of_files:
        bot.send_video(config.chat_id, f)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.token)

    updater.dispatcher.add_handler(MessageHandler())
    # updater.dispatcher.add_handler(CallbackQueryHandler(start))
    # updater.dispatcher.add_handler(CommandHandler('help', help))
    # updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()