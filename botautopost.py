import config
import telebot
import time
import os
from flask import Flask, request

bot = telebot.TeleBot(config.token, threaded=False)

server = Flask(__name__)


@bot.message_handler(content_types=["document"])
def save_doc(message):
    list_of_files_id = []
    list_of_files_id.append(message.document.file_id)
    list_to_write = ''.join(list_of_files_id)
    with open('list.txt', 'a') as f:
        f.write(list_to_write + '\n')


@bot.message_handler(commands=['clean'])
def clean_list():
    pass


def delete_from_list(file_id):
    pass


@bot.message_handler(commands=['list'])
def print_file_id(message):
    with open('list.txt', 'rb') as f:
        bot.send_message(message.chat.id, f.read())


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


@bot.message_handler(commands=['start'])
def main(message):
    list_of_files = load_file_id()
    for file_id in list_of_files:
        print(file_id)
        if check_sended(file_id):
            bot.send_document(config.chat_id, file_id)
            save_sended(file_id)
            time.sleep(3600)


def load_file_id():
    list_of_files = []
    with open('list.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            list_of_files.append(line.strip('\n'))
    return list_of_files


@server.route("/bot", methods=['POST'])
def getmessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://botautopost.herokuapp.com/bot")
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)