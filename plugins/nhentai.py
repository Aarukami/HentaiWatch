from pyrogram import filters, types, Client
from pyrogram.helpers import ikb
from pyrogram.errors import ReplyMarkupInvalid
from hentai import Utils
from requests.exceptions import HTTPError
from .utils import get_hentai,telegraphUP
from .locale import StringResources, Locale
from config import NHCHANNEL, LOGCHAT, LOG_MESSAGE


@Client.on_message(filters.command(['start']))
async def command_start(c: Client, m: types.Message):
    lang = StringResources(Locale.load(m.from_user.language_code))
    msg = lang.res['start']['msg'].format(m.from_user.mention)
    await m.reply(msg)


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
            return await m.reply(lang.res['nhentai']['errornid'])
    else:
        nids.append(Utils.get_random_id())
        is_random_generated = True

    for nid in nids:
        try:
            h = get_hentai(nid, m.from_user.language_code)
        except (TypeError,HTTPError):
            return await m.reply("ERROR: ID was not found")
        doujins.append(types.InputMediaPhoto(media=h[0], caption=h[1]))
        hentai_cover = h[0]
        hentaiid = nid
        capt = h[1]
        

    keyboard_buttons = [ [] ]

    if is_random_generated:
        keyboard_buttons[0].append(
            (lang.res['nhentai']['btnGenhentai'],
                f"genhentai|{m.chat.id}|{m.from_user.language_code}")
        )

    if is_private_chat:
        keyboard_buttons[0].append(
            (lang.res['nhentai']['btnPrivate'],
                f"warnmen|{hentaiid}|{m.from_user.language_code}")
        )

    message_reply = await m.reply_photo(hentai_cover,caption=capt,parse_mode="html")

    if len(keyboard_buttons) >= 1:
        try:
            await message_reply.edit_reply_markup(ikb(keyboard_buttons))
        except ReplyMarkupInvalid:
            pass

@Client.on_callback_query(filters.regex('genhentai'))
async def callback_newhentai(c: Client, cq: types.CallbackQuery):
    data, chat_id, langcode = cq.data.split('|')
    nid = Utils.get_random_id()
    lang = StringResources(Locale.load(langcode))
    h = get_hentai(nid, langcode)
    is_private_chat = False
    photo = h[0]
    caption = h[1]
    chattype = cq.message.chat.type
    

    keyboard_buttons = [
        [ (lang.res['nhentai']['btnGenhentai'],
            f"genhentai|{chat_id}|{langcode}") ]
    ]

    if chattype == "private":
        is_private_chat = True

    if is_private_chat:
        keyboard_buttons[0].append(
            (lang.res['nhentai']['btnPrivate'],
                f"warnmen|{nid}|{langcode}")
        )

    await c.send_photo(chat_id,
            photo,
            caption=caption,
            parse_mode='HTML',
            reply_markup=ikb(keyboard_buttons)
            )


@Client.on_callback_query(filters.regex("warnmen"))
async def callback_warnmensage(c: Client, cq: types.CallbackQuery):
    data,nid, langcode = cq.data.split('|')

    lang = StringResources(Locale.load(langcode))

    keyboard_buttons = [
        [ (lang.res['nhentai']['yes'], f"sendhentai|{nid}|{langcode}"),
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
    data,nid, langcode = cq.data.split('|')
    
    lang = StringResources(Locale.load(langcode))

    h = get_hentai(nid, "en")
    telegraph_url = await telegraphUP(nid)
    
    caption = f"Submitted by {cq.from_user.mention}\n"

    for tmp in h[1].splitlines()[:5]:
        caption += tmp + "\n"
    
    photo = h[0]
    
    nhentai_button = types.InlineKeyboardButton("nhentai.net", url=h[2])
    telegraph_button = types.InlineKeyboardButton("Telegraph",url=telegraph_url)
    keyboard = types.InlineKeyboardMarkup([[nhentai_button,telegraph_button]])

    post = await c.send_photo(NHCHANNEL,
            photo,
            caption,
            parse_mode="html",
            reply_markup=keyboard
            )

    await c.delete_messages(cq.message.chat.id, cq.message.message_id)

    mensage = lang.res['nhentai']['publish'].format(post.link)

    await cq.message.reply(mensage, disable_web_page_preview=True)


@Client.on_message(filters.new_chat_members)
async def join_message(c: Client, m: types.Message):
    bot_me = await c.get_me()
    if bot_me.id in [i.id for i in m.new_chat_members]:
        bot_full_name = "@" + bot_me.username
        warn_format = f"<code>{m.chat.title}</code>"
        if m.chat.username != None:
            warn_format = f"<code>{m.chat.title}</code> (@{m.chat.username})"
        await c.send_message(LOGCHAT,LOG_MESSAGE.format(bot_full_name,warn_format),parse_mode="html")