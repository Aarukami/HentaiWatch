import meval
import traceback
import subprocess
import os

from pyrogram import Client,filters, types

sudolist = [
    1853611480,
]

MAX_MESSAGE_LENGTH = 4096

@Client.on_message(filters.command(['sh', 'shell']) & filters.user(sudolist))
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


@Client.on_message(filters.command(['ev', 'eval'])  & filters.user(sudolist))
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