from json import dump
from os import getcwd
from pathlib import Path
from typing import List, Optional, TypedDict
from unicodedata import category

class Data(TypedDict):
    filename: str
    link: str
    identity: str
    category: Optional[str]

class CrawlJob(TypedDict):
    text: str
    filename: str
    downloadFolder: str
    autoconfirm: Optional[str]
    autostart: Optional[str]


def write_crawljob(links: List[Data]) -> bool:

    jobs: List[CrawlJob] = []
    downloadFolder = Path.joinpath(getcwd(), 'tabs')

    for data in links:
        match data:
            case {'filename': filename, 'link': link}:
                jobs.append({
                    'text': link,
                    'filename': filename,
                    'downloadFolder': downloadFolder
                })

    with open('download.crawljob', 'w') as file:
        dump(jobs, file)

    return True