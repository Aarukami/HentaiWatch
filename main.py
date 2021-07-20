from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton
from pyromod.helpers import ikb
import os

sudolist = [1853611480]

API_ID = os.getenv('APIID')
API_HASH = os.getenv('APIHASH')
BOT_TOKEN = os.getenv('TOKEN')

app = Client('bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.regex(r'^/start'))
async def start(c: app, m: types.Message):
    texto = 'O HentaiWatchBot esta ativo.'
    texto += '\nQualquer duvida olhe o /help'
    texto += '\nFique atento as novidades do HentaiWatch:'
    canal = types.InlineKeyboardButton("Canal", url="https://t.me/HentaiWatchNews")
    grupo =types.InlineKeyboardButton("Grupo", url="https://t.me/HentaiWatchSupport")
    keyboard = types.InlineKeyboardMarkup([[canal, grupo]])
    await m.reply(texto,reply_markup=keyboard)

@app.on_message(filters.regex(r'^/about'))
async def aboutbot(c: app, m: types.Message):
    texto = 'Informações sobre o bot:'
    texto += '\nBot criado por [Luska1331](https://t.me/Luska1331)'
    texto += '\nRepo do bot: [HentaiWatch](https://github.com/Luska1331/HentaiWatch)'
    await m.reply(texto, parse_mode='md', disable_web_page_preview=True)

@app.on_message(filters.regex('^/ev(al)? ') & filters.user(sudolist))
async def on_eval_m(c: app, m: types.Message):
    import traceback
    from meval import meval
    import io
    command = m.text.split()[0]
    eval_code = m.text[len(command) + 1 :]
    sm = await m.reply_text("Processando...")
    try:
        stdout = await meval(eval_code, globals(), **locals())
    except BaseException:
        error = traceback.format_exc()
        await sm.edit_text(f"Ocorreu um erro durante a execução do codigo:\n<code>{error}</code>")
        return
    output_message = f"<b>Input\n&gt;</b> <code>{eval_code}</code>\n\n"
    await sm.edit_text(output_message)


@app.on_message(filters.regex(r'^/changelog'))
async def changelog(c: app, m: types.Message):
    texto = '\n-> Foi adicionado botão para publicar hentais gerados pelo /nhentai.\n    <code>Nota: Canal onde os hentais serão postados @nHentaiWatch'
    texto += '\n-> <code>/getnhentai</code> foi removido por causar floodwait ao bot.'
    texto += '\n-> Botão gerador de hentai foi adicionado ao <code>/nhentai</code>.\n    <code>Nota: Botão somente no modo random.</code>'
    texto += '\n-> Canal e Grupo foram criados.'
    texto += '\n-> <code>/about</code> adicionado.'
    texto += '\n-> <code>/changelog</code> foi adicionado, uso global'
    texto += '\n-> <code>/getnhentai</code> foi adicionado como teste, uso somente no privado.'
    texto += '\n-> <code>/nhentai</code> foi adicionado como teste, uso global.' 
    await m.reply(texto, parse_mode='html')
    
@app.on_message(filters.regex('^/help'))
async def command_help(c: app, m: types.Message):
    texto = '\n<code>/nhentai (ID)</code> -> Lhe envia a capa juntamente com informaçoes basicas do ID definido.'
    texto += '\n<code>/nhentai</code> -> Lhe envia a capa juntamente com informaçoes basicas do hentai escolhido randomicamente.'
    texto += '\n<code>/changelog</code> -> Lhe envia uma lista com as ultimas mudanças no bot.'
    await m.reply(texto, parse_mode='html')

@app.on_message(filters.regex(r'^/shell (?P<text>.+)'))
async def shell(c: app, m: types.Message):
    import os
    if m.from_user.id in sudolist:
        code = m.matches[0]['text']
        import subprocess
        output = subprocess.getoutput(f'{code}')
        if len(output) > 4096:
            with open("output.txt", "w") as f:
                f.write(output)
            await m.reply_document("output.txt")
            return os.remove("output.txt")
        if output == '':
            await m.reply('command executed')
        else:
            await m.reply(output)

@app.on_message(filters.regex(r'^/nhentai(\s(?P<text>.+))?'))
async def nhentai(c: app, m: types.Message):
    mensagem = m.matches[0]['text']
    if mensagem:
        if mensagem.isdecimal():
            try:
                try:
                    from hentai import Hentai, Format, Utils
                    nid = mensagem
                    doujin = Hentai(nid)
                    texto = f'Data de Upload: <code>{doujin.upload_date}</code>'
                    texto += f'\nTitulo: {doujin.title()}'
                    texto += f'\nID: <code>{nid}</code>'
                    texto += f'\nTags: '
                    for tag in doujin.tag:
                        texto +=  f'{tag.name} | '
                    texto += f'\nLink: {doujin.url}'
                    photo = doujin.cover
                    if m.chat.type == "private":
                        keyboard = [[(f"Publicar hentai", f"warnmen|{m.from_user.id}|{m.from_user.first_name}|{nid}")]]
                        await m.reply_photo(photo, caption=texto, parse_mode='HTML', reply_markup=ikb(keyboard))
                    else:
                        await m.reply_photo(photo, caption=texto, parse_mode='HTML')
                except BaseException as err:
                    await m.reply(err)
            except BaseException as err:
                await m.reply("nID invalido, tente outro nID.")
        else:
            await m.reply('Digita um numero, seu animal.') 
    else:
        from hentai import Hentai, Format, Utils
        nid = Utils.get_random_id()
        doujin = Hentai(nid)
        texto = f'Data de Upload: <code>{doujin.upload_date}</code>'
        texto += f'\nTitulo: {doujin.title()}'
        texto += f'\nID: <code>{nid}</code>'
        texto += f'\nTags: '
        for tag in doujin.tag:
            texto +=  f'{tag.name} | '
        texto += f'\nLink: {doujin.url}'
        if m.chat.type == 'private':
            keyboard = [[("Gerar novo hentai", f"genhentai|{m.chat.id}|{m.from_user.id}|{m.from_user.first_name}"),("Publicar hentai", f"warnmen|{m.from_user.id}|{m.from_user.first_name}|{nid}")]]
        else:
            keyboard = [[("Gerar novo hentai", f"genhentai|{m.chat.id}|{m.from_user.id}|{m.from_user.first_name}")]]
        
        photo = doujin.cover
        await m.reply_photo(photo, caption=texto, parse_mode='HTML', reply_markup=ikb(keyboard))

@app.on_callback_query(filters.regex('genhentai'))
async def newhentai(c: app, cq: types.CallbackQuery):
    data, chatid, userid, fname = cq.data.split('|')
    if "genhentai" in data:
        InlineText = "Espere somente alguns instantes."
        await cq.answer(InlineText)
        from hentai import Hentai, Format, Utils
        nid = Utils.get_random_id()
        doujin = Hentai(nid)
        texto = f'Data de Upload: <code>{doujin.upload_date}</code>'
        texto += f'\nTitulo: {doujin.title()}'
        texto += f'\nID: <code>{nid}</code>'
        texto += f'\nTags: '
        for tag in doujin.tag:
            texto +=  f'{tag.name} | '
        texto += f'\nLink: {doujin.url}'
        photo = doujin.cover
        if cq.message.chat.type == 'private':
            keyboard = [[("Gerar novo hentai", f"genhentai|{chatid}|{userid}|{fname}"),("Publicar hentai", f"warnmen|{userid}|{fname}|{nid}")]]
        else:
            keyboard = [[("Gerar novo hentai", f"genhentai|{chatid}|{userid}|{fname}")]]
        await c.send_photo(int(chatid) ,photo, caption=texto, parse_mode='HTML', reply_markup=ikb(keyboard))

@app.on_callback_query(filters.regex("warnmen"))
async def warnmensage(c: Client, cq: types.CallbackQuery):
    data, userid, fname, nid = cq.data.split('|')
    keyboard = [[("Sim", f"sendhentai|{userid}|{fname}|{nid}"),("Não", "delmenwarn")]]
    await cq.message.reply('Deseja enviar esse hentai?', reply_markup=ikb(keyboard))

@app.on_callback_query(filters.regex("delmenwarn"))
async def delwarnmen(c: Client, cq: types.CallbackQuery):
    await c.delete_messages(cq.message.chat.id, cq.message.message_id)
    await c.send_message(cq.message.chat.id, "Envio cancelado.")

@app.on_callback_query(filters.regex("sendhentai"))
async def sendhetani(c: Client, cq: types.CallbackQuery):
    data, userid, fname, nid = cq.data.split('|')
    from hentai import Hentai
    doujin = Hentai(nid)
    texto = f'Enviado por <a href="tg://user?id={userid}">{fname}</a>'
    texto += f'\nData de Upload: <code>{doujin.upload_date}</code>'
    texto += f'\nTitulo: {doujin.title()}'
    texto += f'\nID: <code>{nid}</code>'
    texto += f'\nTags: '
    for tag in doujin.tag:
        texto +=  f'{tag.name} | '
    photo = doujin.cover
    KB = InlineKeyboardButton("nhentai.net", url=doujin.url)
    BK = types.InlineKeyboardMarkup([[KB]])
    nhentailink = await c.send_photo(-1001599914804, photo, texto, parse_mode="html", reply_markup=BK)
    await c.delete_messages(cq.message.chat.id, cq.message.message_id)
    SA = f"Obrigado por divulgar o hentai ao nosso canal.\nLink do post: https://t.me/nHentaiWatch/{nhentailink.message_id}"
    await cq.message.reply(SA, disable_web_page_preview=True)

app.run()
