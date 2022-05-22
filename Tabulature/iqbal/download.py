import aiofiles
import asyncio
from os import listdir, getcwd
from os.path import join, isfile
from typing import List
from re import search

"""
Run this first ->
youtube-dl --skip-download --write-description https://www.youtube.com/playlist?list=PLASPZ6BqjcC3vyb40nsseVVxIJFbSrLC0
"""

def get_files(mypath: str) -> List[str]:
    return [f for f in listdir(mypath) if isfile(join(mypath, f)) and 'description' in f]    

async def reader(file_name: str)-> None:
    async with aiofiles.open(file_name, mode='r') as f:
        try:
            name = search(r'(.+)\(', file_name).group(1).strip()
        except Exception:
            try:
                name = search(r'(.+)\- F', file_name).group(1).strip()
            except:
                name = file_name
        flag = True
        async for line in f:
            if 'http' in line:
                print(f'[{name}]: {line}')
                flag = False
        if flag:
            print(f'[{name}]: No links available')

async def parser(file_names: List[str]):
    tasks = [reader(file_name) for file_name in file_names]
    await asyncio.gather(*tasks)

asyncio.run(parser(get_files(getcwd())))
