#!/usr/bin/python

from enum import Enum
from posixpath import dirname
import sys
import aiofiles
import asyncio
from os import listdir, getcwd
from os.path import join, isfile
from typing import List
from re import IGNORECASE, compile

sys.path.append(dirname(dirname(dirname(__file__))))

from Tabulature.create_crawljob import CrawlJob, Data, write_crawljob, write_readme

''''
Run this first ->
../write_descriptions.sh https://www.youtube.com/channel/UCjrsgDvC-EQB3k56iV22jug/videos
'''


def get_files(mypath: str) -> List[str]:
    return [
        f for f in listdir(mypath) if isfile(join(mypath, f)) and "description" in f
    ]


identity = 0
backlist_pattern = compile(
    'instagram|facebook|twitter|youtube|subscri|alphaco|wallpaper|source|youtu\.be',
    flags=IGNORECASE,
)
tab_pattern = compile(r'tab[s]{0,1}[:]{0,1}', IGNORECASE)


def generate_id():
    global identity
    identity += 1
    return f'{identity:02d}'


video_title_pattern = compile(
    r"(\({0,1}\([Gg]uit.+)|(\({0,1}[Ss]olo.+)|(\({0,1}[Ff]ingerst.+)|(【TAB】.+)|(\[TABS\])|(guitar cover.+)",
    flags=IGNORECASE,
)


class LinkType(Enum):
    tab = 1
    tone = 2


def getType(line: str) -> LinkType | None:
    if line.lower().startswith(LinkType.tab.name):
        return LinkType.tab
    if line.lower().startswith(LinkType.tone.name):
        return LinkType.tone
    return None


async def reader(file_name: str, identity: str) -> list[Data]:

    link: list[Data] = []

    async with aiofiles.open(file_name, mode="r") as f:
        name = file_name.replace(".description", "")
        name = video_title_pattern.sub("", name).strip()
        flag = True
        link_type: LinkType | None = None

        async for line in f:

            if link_type is None:
                link_type = getType(line)

            if (
                link_type is not None
                and 'http' in line
                and backlist_pattern.search(line) is None
            ):
                url = tab_pattern.sub('', line.strip()).strip()

                link.append(
                    {
                        'link': url,
                        'filename': name.strip()
                        + ('.pdf' if link_type.value == LinkType.tab.value else '.rar'),
                        'identity': identity,
                        'category': link_type.name,
                    }
                )
                link_type = None
                flag = False

        if flag:
            print(f"{identity}. {name}: No links available")

    return link


async def parser(file_names: List[str]):
    tasks = [reader(file_name, generate_id()) for file_name in file_names]
    results = await asyncio.gather(*tasks)

    links = [data for result in results for data in result]

    write_crawljob(links)
    write_readme(links)


asyncio.run(parser(get_files(getcwd())))
