from requests import Response
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup as bs
from asyncio import gather, Semaphore, get_event_loop
from re import compile

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from create_crawljob import write_crawljob

SITEMAP = "https://fingertabs.com/post-sitemap.xml"
URL_REGEX = compile(r"(?<=\?file=)http.:\/\/fingertabs.+")

asession = AsyncHTMLSession()
semaphore = Semaphore(10)


async def get_page(url: str):
    page = await asession.get(url)
    print('hit')
    soup = bs(page.text, 'html.parser')
    ret = set()
    title: str

    if title_tag := soup.find('h2', class_='post-title'):
        title = title_tag.text
    else:
        title = 'unknown'

    if iframe := soup.find('iframe', class_='pdfjs-viewer'):
        if res := URL_REGEX.search(iframe.attrs.get('src')):
            ret.add(res.group())

    if target := soup.find('div', id='timer_2'):
        for i in target.find_all('a', rel=False):
            ret.add(i.attrs.get('href'))

    return ret, title.strip()


async def safe_get(i: str):
    async with semaphore:  # semaphore limits num of simultaneous downloads
        return await get_page(i)


async def main():
    body: Response = await asession.get(SITEMAP)
    soup = bs(body.text, 'xml')

    tasks = [safe_get(i.find('loc').text) for i in soup.find_all('url')[:10]]

    results = await gather(*tasks)

    print('# Fingertabs')
    for links, title in results:
        print(f'- {title}')
        for link in links:
            print(f"\t- [{link.split('.')[-1]}]({link})")

    crawl_data = []
    for links, title in results:
        data = {
            'link': list(links),
            'filename': title,
            'identity': 'fingertabs',
            'category': 'tab',
        }
        crawl_data.append(data)

    write_crawljob(crawl_data)


if __name__ == "__main__":
    loop = get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
