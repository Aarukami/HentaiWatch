from pyrogram import Client
from os import getenv

API_ID = getenv('APIID')
API_HASH = getenv('APIHASH')
BOT_TOKEN = getenv('TOKEN')

app = Client('bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)