# -*- coding: utf-8 -*
import os

token = os.environ.get('TOKEN_AUTOPOSTER')
chat_id = os.environ.get('CHAT_ID_AUTOPOSTER').split(', ')
post_int = int(os.environ.get('POST_INTERVAL'))
caption_text = os.environ.get('CAPTION_text').split(', ')
