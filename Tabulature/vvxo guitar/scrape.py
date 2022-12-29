#!/usr/bin/python

from asyncio import gather
from io import TextIOWrapper
from re import IGNORECASE, compile as compileREGEX
from sys import argv
from requests import Response
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup as bs

asession = AsyncHTMLSession()

link_pattern = compileREGEX("drive", flags=IGNORECASE)
title_pattern = compileREGEX(
    r"(\({0,1}\([Gg]uit.+)|(\({0,1}[Ss]olo.+)|(\({0,1}[Ff]ingerst.+)|(\[TABS\])",
    flags=IGNORECASE,
)
SITEMAP_URI = "https://www.vvxofingerstyletab.com/sitemap.xml"


async def main():
    sitemap: Response = asession.get(SITEMAP_URI)
    soup = bs(sitemap.text, "lxml")
    posts_tasks = []

    for posts in filter(lambda x: "pt-post" in x.text.lower(), soup.find_all("loc")):
        posts_tasks.append(parse_posts(posts.text))
        # break

    posts = await gather(*posts_tasks)
    write = "write" in argv

    links_file: TextIOWrapper
    readme_file: TextIOWrapper

    if write:
        links_file = open("./links.txt", "w+")
        readme_file = open("./readme.md", "w+")

    for idx, (title, link) in enumerate(
        result
        for post in posts
        for result in post
        if None not in post
        if None not in result
    ):

        print(f"{idx+1:03}. [{title}]({link})")

        if write:
            links_file.write(link + "\n")
            readme_file.write(f"{idx+1:03}. [{title}]({link})\n")

    if write:
        links_file.close()
        readme_file.close()


async def parse_posts(url: str):
    posts: Response = await asession.get(url)
    soup = bs(posts.text, "lxml")
    post_tasks = []
    for post in soup.findAll("loc"):
        post_tasks.append(parse_post(post.text))
        # break

    ret = await gather(*post_tasks)
    if None in ret:
        ...
    return ret


async def parse_post(url: str):
    post: Response = await asession.get(url)
    soup = bs(post.text, "lxml")
    title = soup.select_one("h1.entry-title").text
    title = title_pattern.sub("", title.strip()).strip().removesuffix("-")

    for link in soup.select("div.entry-content a"):
        if link_pattern.search(link.attrs.get("href")):
            return title, link.attrs.get("href")
    return None


asession.run(main)
