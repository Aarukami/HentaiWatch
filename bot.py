from pyrogram import Client
from os import getenv

from config import API_ID,API_HASH,BOT_TOKEN,PLUGINS

Client('bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN,plugins=PLUGINS).run()