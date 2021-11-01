import os

#Config - bot.py
API_ID = os.getenv('8153612') or "Your API ID here"
API_HASH = os.getenv('6c9636ea928b50402b7d7c69a6eba45c') or "Your API HASH here"
BOT_TOKEN = os.getenv('2077017001:AAHE9GF1OK2u3jRR9Ns5yZKycsQCR8HW0eY') or "BOT TOKEN here"
PLUGINS = dict(root="plugins")

#Config - plugins/utils.py -> TelegraphUP()
SHORT_NAME = "HW"
AUTHOR_NAME = "Shouko komi"
AUTHOR_URL = "https://t.me/HentaiWatchBot"

#Cofig - plugins/sudoers.py
SUDO_LIST = [2021224869]
MAX_MESSAGE_LENGTH = 4096

# -> sudo_command_telegraph()
INIT_MESSAGE_PHOTO = "https://telegra.ph/file/5efdb99994b1528f77ccf.png"

#Config - plugins/nhentai.py
LOGCHAT = -1001513602613
NHCHANNEL = -1001632904989
LOG_MESSAGE = "{} has been added on {}"

#Config - plugins/inline.py
INLINE_MENU_PHOTO_ICON_1 = "https://te.legra.ph/file/de239bf119e5e52fe2f07.jpg"
