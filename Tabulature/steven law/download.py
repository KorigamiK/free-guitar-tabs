import asyncio
from requests_html import AsyncHTMLSession
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
        if 'pdf' in i:
            print(search(r'https:\/\/.+pdf', i).group(0))

# url = 'https://www.google.com/search?q=site:https://stevehansenyt.weebly.com/&sxsrf=ALeKk00Y6S1fmRDbny6rL_opEYPfybOc-w:1617385514341&ei=KlhnYIHjE5K5rQHRlbqgAQ&start={}&sa=N&ved=2ahUKEwiBoK_IjuDvAhWSXCsKHdGKDhQQ8tMDegQIAxA2'
@timer
async def main(url):
    tasks = [get_links(url, i) for i in range(0, 150, 10)]
    await asyncio.gather(*tasks)

url = 'https://www.google.co.in/search?q=site:https://stevenlaw.files.wordpress.com/&lr=&as_qdr=all&biw=1366&bih=660&sxsrf=ALeKk032zoettmgE55xfLLdCMdsB555xMg:1617628543636&ei=fw1rYNmvJuuR4-EPu7mJsAg&start={}&sa=N&ved=2ahUKEwiZ6-L1l-fvAhXryDgGHbtcAoY4HhDy0wN6BAgBEEM'
loop.run_until_complete(main(url))
# loop.run_until_complete(get_links(url, 10))
async def test():
    res = await assession.get('https://web.archive.org/web/20201101050950/https://stevehansenyt.weebly.com/tabs.html')
    for i in res.html.absolute_links:
        print(search(r'\/(htt.+)', i).group(1))

# loop.run_until_complete(test())
