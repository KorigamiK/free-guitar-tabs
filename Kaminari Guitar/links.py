import asyncio
from scraper import scraper
from aiohttp import ClientSession
from asyncio import run

LAST_PAGE = 127

class kaminari:
    page_template = "https://music.kaminari.info/page/{}/"
    index = 0

    def __init__(self, request: scraper) -> None:
        self.request = request

    async def _get_from_page(self, link):
        try:
            page = await self.request.get(link)
            get_link = lambda x: x.get("href")
            return map(get_link, page.select('h5 > a[data-type="works"]'))
        except RuntimeError:
            print("Runtime error")

    async def get_download_link(self, tabulature_url):
        kaminari.index += 1
        idx = kaminari.index
        # print(f'starting {idx}')
        page = await self.request.get(tabulature_url)
        try:
            title = page.select_one('.titles > a').text
            ret = page.select_one('[target="_blank"]').get("href")
            print(f'{idx: 04}. [{title}]({ret})')
        except Exception as e:
            print(f'Exception {e} on {tabulature_url}')
        # return ret

    async def get_all_pages(self):
        for links in asyncio.as_completed(
            [
                self._get_from_page(kaminari.page_template.format(number))
                for number in range(1, LAST_PAGE+1)
            ]
        ):
            links = await links
            for link in links:
                yield link

    async def get_all_links(self):
        tasks = []
        async for tabulature in self.get_all_pages():
            tasks.append(self.get_download_link(tabulature))

        await asyncio.gather(*tasks)
        # print(result)


async def main():
    async with ClientSession() as session:
        request = scraper(session)
        parser = kaminari(request)
        await parser.get_all_links()


run(main())