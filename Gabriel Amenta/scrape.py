#!/usr/bin/python

from enum import Enum
import aiofiles
import asyncio
from os import listdir, getcwd
from os.path import join, isfile
from typing import List
from re import IGNORECASE, compile

print(__package__)
from ..create_crawljob import Data

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


async def reader(file_name: str, identity: str) -> None:

    links: List[Data] = []

    async with aiofiles.open(file_name, mode="r") as f:
        name = file_name.replace(".description", "")
        name = video_title_pattern.sub("", name).strip()
        flag = True
        link_type: LinkType | None = None

        async for line in f:

            link_type = getType(line)

            if (
                link_type is not None
                and 'http' in line
                and backlist_pattern.match(line) is None
            ):
                link = tab_pattern.sub('', line.strip()).strip()
                links.append(
                    {
                        'link': link,
                        'filename': name,
                        'identity': identity,
                        'category': link_type.name,
                    }
                )
                link_type = None
                flag = False

        if flag:
            print(f"{identity}. {name}: No links available")


async def parser(file_names: List[str]):
    tasks = [reader(file_name, generate_id()) for file_name in file_names]
    await asyncio.gather(*tasks)


asyncio.run(parser(get_files(getcwd())))
