from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs

class scraper():
    def __init__(self, session: ClientSession):
        self.session = session

    async def get(self, url: str) -> bs:
        async with self.session.get(url) as resp:
            ret = await resp.text()

        return bs(ret, 'html.parser')