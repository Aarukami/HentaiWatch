from aiographfix.api import Telegraph
from pyrogram import Client, filters,types
from pyrogram.errors import QueryIdInvalid,QueryIdEmpty
from pyrogram.types import InlineQuery, InlineQueryResultArticle,InputTextMessageContent, InlineQueryResultPhoto
from pyrogram.helpers import ikb
from requests.exceptions import HTTPError
from .utils import get_hentai,telegraphUP
from hentai import Hentai,Format
from config import INLINE_MENU_PHOTO_ICON_1

@Client.on_inline_query()
async def inline_menu(c: Client, q: InlineQuery):
    articles = [
        InlineQueryResultArticle(
            title="Hentai",
            input_message_content=InputTextMessageContent(
                f"<b>Use:</b> <code>nh (id)</code> - Send the hentai corresponding to the ID.",
                parse_mode="html"
            ),
            description="Send the hentai corresponding to the ID.",
            thumb_url=INLINE_MENU_PHOTO_ICON_1
        )
    ]

    try:
        await q.answer(
            results=articles,cache_time=0
        )
    except (QueryIdEmpty,QueryIdInvalid):
        pass

@Client.on_inline_query(filters.regex(r"^nh (?P<query>.+)"),group=-1)
async def Inline_Random_Hentai(c: Client, q: InlineQuery):
    articles = []
    query = q.query.split()
    if len(query) != 0 and query[0] == "nh":
        keyboard_buttons = [[]]
        try:
            hentai_id = int(query[1])
        except ValueError:
            return 
        try:
            hentai = get_hentai(hentai_id,"en")
            telegraph_url = await telegraphUP(hentai_id)
        except HTTPError:
            return
        
        capt = "\n".join(hentai[1].splitlines()[:5])
        hentai_info = Hentai(hentai_id)
        hentai_title = hentai_info.title(Format.Pretty)
        keyboard_buttons[0].append(
           ("nhentai",hentai_info.url, "url")
        )
        keyboard_buttons[0].append(
            ("telegraph",telegraph_url,"url")
        )
        articles.append(
            InlineQueryResultPhoto(
                photo_url=hentai[0],
                title=hentai_title,
                description=hentai[3],
                caption=capt,
                reply_markup=ikb(keyboard_buttons)
            )
        )
    try:
        await q.answer(
            results=articles,cache_time=0
        )
    except (QueryIdEmpty,QueryIdInvalid):
        pass