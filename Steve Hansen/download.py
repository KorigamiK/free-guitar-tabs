import asyncio
from requests_html import AsyncHTMLSession, HTML
from time import time
from re import search

def timer(function):
    async def wrapped_func(*args):
        s = time()
        res = await function(*args)
        print(f'{function.__name__} took {time()-s} seconds')
        return res
    return wrapped_func

assession = AsyncHTMLSession()
loop = assession.loop

# @timer
async def get_links(google_url, start):
    res  =  await assession.get(google_url.format(start))
    # await res.arender()
    for i in res.html.absolute_links:
        print(i)


url = 'https://www.google.com/search?q=site:https://stevehansenyt.weebly.com/&sxsrf=ALeKk00Y6S1fmRDbny6rL_opEYPfybOc-w:1617385514341&ei=KlhnYIHjE5K5rQHRlbqgAQ&start={}&sa=N&ved=2ahUKEwiBoK_IjuDvAhWSXCsKHdGKDhQQ8tMDegQIAxA2'
@timer
async def main():
    tasks = [get_links(url, i) for i in range(0, 20, 10)]
    await asyncio.gather(*tasks)

# loop.run_until_complete(main())
# loop.run_until_complete(get_links(url, 10))
async def test():
    res = await assession.get('https://web.archive.org/web/20201101050950/https://stevehansenyt.weebly.com/tabs.html')
    for i in res.html.absolute_links:
        print(search(r'\/(htt.+)', i).group(1))

loop.run_until_complete(test())