import traceback
import subprocess
import os

from meval import meval 

from pyrogram import Client,filters, types
from requests.models import HTTPError

from .utils import get_hentai,telegraphUP

from config import SUDO_LIST,MAX_MESSAGE_LENGTH,INIT_MESSAGE_PHOTO



@Client.on_message(filters.command(['sh', 'shell']) & filters.user(SUDO_LIST))
async def command_shell(c: Client, m: types.Message):
    """
    Execute shell commands

    NOTE: Although it is quite obvious, it is important to remember that this
          command is quite dangerous, since it gives the user full shell access
    """

    initial_index = 3
    if m.text.startswith('/shell'):
        initial_index = 6

    code = m.text[initial_index:]

    result = subprocess.getoutput(code)

    result_file = "output.txt"

    if len(result) > MAX_MESSAGE_LENGTH:
        with open(result_file, "w") as f:
            f.write(result)

        await m.reply_document(result_file)
        os.remove(result_file)
        return

    if len(result) < 1:
        result = "Command Executed"

    await m.reply(result)


@Client.on_message(filters.command(['ev', 'eval'])  & filters.user(SUDO_LIST))
async def command_on_eval(c: Client, m: types.Message):
    """
    Allows user to run Python scripts

    NOTE: This implementation can be harmful, since it has complete
          access to the bot internals
    """
    
    command = m.text.split()[0]

    eval_code = m.text[len(command) + 1 :]

    message = await m.reply_text("Processando...")
    result = ""

    result_file="output.txt"

    try:
        result = await meval(eval_code, globals(), **locals())

    except BaseException:
        result = "Error: <code>{}</code>".format(traceback.format_exc())

    if MAX_MESSAGE_LENGTH >= len(str(result)):
        await message.edit_text(result)
    else:
        with open(result_file, "w") as f:
            f.write(result)

        await m.reply_document(result_file)
        os.remove(result_file)
        return

@Client.on_message(filters.command("telegraph") & filters.user(SUDO_LIST))
async def sudo_command_telegraph(c: Client, m: types.Message):
    hentai_id = m.text.split()[1]
    init_message = await m.reply_photo(photo=INIT_MESSAGE_PHOTO,
                                        caption=f"Telegraph: nhentai.net/g/{hentai_id}"
    )
    try:
        hentai_info = get_hentai(hentai_id,m.from_user.language_code)
        telegraph_url = await telegraphUP(hentai_id)
    except BaseException as err:
        return await init_message.edit_text(f"ERROR: <code>{err}</code>",parse_mode="html")
    capt = "\n".join(hentai_info[1].splitlines()[:5])
    nhentai_button = types.InlineKeyboardButton("nhentai.net", url=hentai_info[2])
    telegraph_button = types.InlineKeyboardButton("Telegraph",url=telegraph_url)
    keyboard = types.InlineKeyboardMarkup([[nhentai_button,telegraph_button]])
    Media = types.InputMediaPhoto(
        media=hentai_info[0],
        caption=capt,
        parse_mode="html"
    )
    await init_message.edit_media(Media,keyboard)