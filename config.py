# -*- coding: utf-8 -*
import os

token = os.environ['TOKEN']
chat_id = os.environ['CHAT_ID'].split(', ')
database_url = os.environ['DATABASE_URL']
port = int(os.environ.get('PORT', '5000'))
time_s = int(os.environ.get('TIME_S'))
time_e = int(os.environ.get('TIME_E'))
