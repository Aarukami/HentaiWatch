from pyrogram import Client, filters, types
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
    texto += '\nRepo do bot: [HentaiWatchBot](https://github.com/Luska1331/HentaiWatchBot)'
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
        await sm.edit_text(
            f"Ocorreu um erro durante a execução do codigo:\n<code>{error}</code>"
        )
        return
    output_message = f"<b>Input\n&gt;</b> <code>{eval_code}</code>\n\n"
    await sm.edit_text(output_message)


@app.on_message(filters.regex(r'^/changelog'))
async def changelog(c: app, m: types.Message):
    texto = '\n-> Botão gerador de hentai foi adicionado ao <code>/nhentai</code>.\n    <code>Nota: Botão somente no modo random.</code>'
    texto += '\n-> Canal e Grupo foram criados.'
    texto += '\n-> <code>/about</code> adicionado.'
    texto += '\n-> <code>/changelog</code> foi adicionado, uso global'
    texto += '\n-> <code>/getnhentai</code> foi adicionado como teste, uso somente no privado.'
    texto += '\n-> <code>/nhentai</code> foi adicionado como teste, uso global.' 
    await m.reply(texto, parse_mode='html')
    
@app.on_message(filters.regex('^/help'))
async def command_help(c: app, m: types.Message):
    texto = '\n<code>/getnhentai (ID)</code> -> Lhe envia as paginas do ID enviado.'
    texto += '\n<code>/nhentai (ID)</code> -> Lhe envia a capa juntamente com informaçoes basicas do ID definido.'
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
                await m.reply_photo(photo, caption=texto, parse_mode='HTML')
            except:
                await m.reply('ID invalido, tente novamente, seu corno.')
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
        keyboard = [[("Gerar novo hentai", f"genhentai|{m.chat.id}")]]
        photo = doujin.cover
        await m.reply_photo(photo, caption=texto, parse_mode='HTML', reply_markup=ikb(keyboard))

@app.on_callback_query(filters.regex('genhentai'))
async def newhentai(c: app, cq: types.CallbackQuery):
    data, chatid = cq.data.split('|')
    if "genhentai" in data:
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
        keyboard = [[("Gerar novo hentai", f"genhentai|{chatid}")]]
        photo = doujin.cover
        InlineText = "Espere somente alguns instantes."
        await cq.answer(InlineText)
        await c.send_photo(int(chatid) ,photo, caption=texto, parse_mode='HTML', reply_markup=ikb(keyboard))



app.run()
