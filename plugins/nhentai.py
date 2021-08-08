from pyrogram import filters, types, Client
from pyrogram.helpers import ikb
from hentai import Hentai, Utils, Format

from .locale import StringResources, Locale

NHCHANNEL = -1001599914804

def get_hentai(nid, langcode):
    lang = StringResources(Locale.load(langcode))
    doujin = Hentai(nid)


    tags = " | ".join([ tag.name for tag in doujin.tag ])

    capt = lang.res['nhentai']['msg'].format(
            doujin.upload_date,
            doujin.title(Format.Pretty),
            nid,
            tags,
            doujin.url
            )

    capt += "\n<-------->\n"

    photo = doujin.cover

    return photo, capt


@Client.on_message(filters.command(['start']))
async def command_start(c: Client, m: types.Message):
    lang = StringResources(Locale.load(m.from_user.language_code))

    msg = lang.res['start']['msg'].format(m.from_user.mention)

    channel = types.InlineKeyboardButton("nHentaiWatch", url="https://t.me/nHentaiWatch")
    group = types.InlineKeyboardButton("HentaiWatchGroup", url="https://t.me/HentaiWatchGroup")

    keyboard = types.InlineKeyboardMarkup([ [channel, group] ])

    await m.reply(msg, reply_markup=keyboard)


@Client.on_message(filters.command(['help']))
async def command_help(c: Client, m: types.Message):
    lang = StringResources(Locale.load(m.from_user.language_code))
    msg = lang.res['help']['msg']
    await m.reply(msg, parse_mode='html')


@Client.on_message(filters.command(['nh', 'nhentai']))
async def command_nhentai(c: Client, m: types.Message):
    msg = m.text.split()
    is_private_chat = False
    is_random_generated = False
    nids = []
    lang = StringResources(Locale.load(m.from_user.language_code))

    doujins = []

    if m.chat.type == "private":
        is_private_chat = True

    if len(msg) > 1:
        try:
            nids = [ int(nid) for nid in msg[1:] ]
        except ValueError:
            await m.reply(lang.res['nhentai']['errorNid'])
    else:
        nids.append(Utils.get_random_id())
        is_random_generated = True

    for nid in nids:
        h = get_hentai(nid, m.from_user.language_code)
        doujins.append(types.InputMediaPhoto(media=h[0], caption=h[1]))
        hentai_cover = h[0]
        hentaiid = nid
        capt = h[1]
        

    keyboard_buttons = [ [] ]

    if is_random_generated:
        keyboard_buttons[0].append(
            (lang.res['nhentai']['btnGenhentai'],
                f"genhentai|{m.chat.id}|{m.from_user.id}|{m.from_user.first_name}|{m.from_user.language_code}|{m.chat.type}")
        )

    if is_private_chat:
        keyboard_buttons[0].append(
            (lang.res['nhentai']['btnPrivate'],
                f"warnmen|{m.from_user.id}|{m.from_user.first_name}|{hentaiid}|{m.from_user.language_code}")
        )

    message_reply = await m.reply_photo(hentai_cover,caption=capt,parse_mode="html")

    if len(keyboard_buttons) < 1:
        return

    await message_reply.edit_reply_markup(ikb(keyboard_buttons))


@Client.on_callback_query(filters.regex('genhentai'))
async def callback_newhentai(c: Client, cq: types.CallbackQuery):
    data, chat_id, userid, fname, langcode, chattype = cq.data.split('|')
    nid = Utils.get_random_id()
    lang = StringResources(Locale.load(langcode))
    h = get_hentai(nid, langcode)
    is_private_chat = False
    photo = h[0]
    caption = h[1]

    keyboard_buttons = [
        [ (lang.res['nhentai']['btnGenhentai'],
            f"genhentai|{chat_id}|{userid}|{fname}|{langcode}|{chattype}") ]
    ]

    if chattype == "private":
        is_private_chat = True

    if is_private_chat:
        keyboard_buttons[0].append(
            (lang.res['nhentai']['btnPrivate'],
                f"warnmen|{userid}|{fname}|{nid}|{langcode}")
        )

    await c.send_photo(chat_id,
            photo,
            caption=caption,
            parse_mode='HTML',
            reply_markup=ikb(keyboard_buttons)
            )


@Client.on_callback_query(filters.regex("warnmen"))
async def callback_warnmensage(c: Client, cq: types.CallbackQuery):
    data, userid, fname, nid, langcode = cq.data.split('|')

    lang = StringResources(Locale.load(langcode))

    keyboard_buttons = [
        [ (lang.res['nhentai']['yes'], f"sendhentai|{userid}|{fname}|{nid}|{langcode}"),
          (lang.res['nhentai']['no'], f"delmenwarn|{langcode}") ]
    ]

    await cq.message.reply(lang.res["nhentai"]["warnmen"], reply_markup=ikb(keyboard_buttons))


@Client.on_callback_query(filters.regex("delmenwarn"))
async def callback_delwarnmen(c: Client, cq: types.CallbackQuery):
    data, langcode = cq.data.split("|")
    lang = StringResources(Locale.load(langcode))

    await c.delete_messages(cq.message.chat.id, cq.message.message_id)
    await c.send_message(cq.message.chat.id, lang.res['nhentai']['cancel'])



@Client.on_callback_query(filters.regex("sendhentai"))
async def callback_send_hentai(c: Client, cq: types.CallbackQuery):
    data, userid, fname, nid, langcode = cq.data.split('|')
    
    lang = StringResources(Locale.load(langcode))

    doujin = Hentai(nid)

    caption =   f"Enviado por <a href=\"tg://user?id={userid}\">{fname}</a>" + \
                f"\nData de Upload: <code>{doujin.upload_date}</code>"       + \
                f"\nTitulo: {doujin.title(Format.Pretty)}"                   + \
                f"\nID: <code>{nid}</code>"                                  + \
                f"\nTags: "

    caption += " | ".join([ tag.name for tag in doujin.tag ])

    photo = doujin.cover

    keyboard_button = types.InlineKeyboardButton("nhentai.net", url=doujin.url)
    keyboard_markup = types.InlineKeyboardMarkup([ [keyboard_button] ])

    post = await c.send_photo(NHCHANNEL,
            photo,
            caption,
            parse_mode="html",
            reply_markup=keyboard_markup
            )

    await c.delete_messages(cq.message.chat.id, cq.message.message_id)

    mensage = lang.res['nhentai']['publish'].format(post.link)

    await cq.message.reply(mensage, disable_web_page_preview=True)
