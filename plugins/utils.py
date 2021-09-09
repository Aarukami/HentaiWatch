from .locale import StringResources,Locale
from hentai import Hentai,Format
import aiohttp
import re
from aiographfix import Telegraph
from config import SHORT_NAME,AUTHOR_NAME,AUTHOR_URL

def get_hentai(nid, language_code):
    lang = StringResources(Locale.load(language_code))
    doujin = Hentai(nid)


    tags = ", ".join([ tag.name for tag in doujin.tag ])

    capt = lang.res['nhentai']['msg'].format(
            doujin.upload_date,
            doujin.title(Format.Pretty),
            nid,
            doujin.num_pages,
            tags + ".",
            doujin.url
            )

    photo = doujin.cover

    link = doujin.url

    return photo, capt, link, tags

async def telegraphUP(nid):

        tmp = []
        html_content = ''
        url = f'https://cin.pw/v/{nid}'
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                        regex = re.findall('<img\ssrc="(.*?)"\swidth=".*?"\sheight=".*?"\s\/>', await resp.text())
        
        for tmp_image in regex:
                tmp.append(tmp_image)

        for img in tmp:
                html_content += f"<img src=\"{img}\"/>\n"

        doujin = Hentai(nid)
        telegraph = Telegraph()
        await telegraph.create_account(SHORT_NAME,AUTHOR_NAME, author_url=AUTHOR_URL)
        page = await telegraph.create_page(
                title=doujin.title(Format.Pretty),
                content=html_content
        )
        page_url = page.url
        await telegraph.close()
        return page_url
