import aiofiles
import asyncio
from os import listdir, getcwd
from os.path import join, isfile
from typing import List
from re import search, sub, IGNORECASE

"""
Run this first ->
youtube-dl --skip-download --write-description https://www.youtube.com/channel/UCI8C1y5Ivt5yzxwsHpTL1gw/videos
"""


def get_files(mypath: str) -> List[str]:
    return [
        f for f in listdir(mypath) if isfile(join(mypath, f)) and "description" in f
    ]


identity = 0


def generate_id():
    global identity
    identity += 1
    return identity


async def reader(file_name: str, identity) -> None:
    async with aiofiles.open(file_name, mode="r") as f:
        name = file_name.replace(".description", "")
        name = sub(
            r"(\({0,1}\([Gg]uit.+)|(\({0,1}[Ss]olo.+)|(\({0,1}[Ff]ingerst.+)|(\[TABS\])",
            "",
            name,
        ).strip()
        flag = True
        async for line in f:
            if "http" in line and "soundcloud" not in line:
                print(f"{identity}. [{name}] ", line.strip())
                flag = False
        if flag:
            print(f"{identity}. [{name}]: No links available")


async def parser(file_names: List[str]):
    tasks = [reader(file_name, generate_id()) for file_name in file_names]
    await asyncio.gather(*tasks)


asyncio.run(parser(get_files(getcwd())))
