import os

#Config - bot.py
API_ID = os.getenv('16409691') or "Your API ID here"
API_HASH = os.getenv('a60b42fe202a7ffbb97043df46901227') or "Your API HASH here"
BOT_TOKEN = os.getenv('5137140779:AAEzozrs9bOBdTYVatswZcO1zw2b6JLEpeU') or "BOT TOKEN here"
PLUGINS = dict(root="plugins")

#Config - plugins/utils.py -> TelegraphUP()
SHORT_NAME = "HT"
AUTHOR_NAME = "Hemtai"
AUTHOR_URL = "http://t.me/Fking_Hemtai_09Bot"

#Cofig - plugins/sudoers.py
SUDO_LIST = [5053846242]
MAX_MESSAGE_LENGTH = 4096

# -> sudo_command_telegraph()
INIT_MESSAGE_PHOTO = "https://telegra.ph/file/5efdb99994b1528f77ccf.png"

#Config - plugins/nhentai.py
LOGCHAT =  -1001747988223
NHCHANNEL = -1001632904989
LOG_MESSAGE = "{} has been added on {}"

#Config - plugins/inline.py
INLINE_MENU_PHOTO_ICON_1 = "https://te.legra.ph/file/de239bf119e5e52fe2f07.jpg"
