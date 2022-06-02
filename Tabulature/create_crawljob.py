from json import dump
from os import getcwd
from os.path import join
from typing import List, Optional, TypedDict
from unicodedata import category


class Data(TypedDict):
    filename: str
    link: str
    identity: str
    category: Optional[str]
    ext: Optional[str]

class CrawlJob(TypedDict):
    '''
    {
        "downloadFolder" : null,(null|"String")
        "chunks" : 0,(int)
        "overwritePackagizerEnabled" : true, (true|false)
        "extractAfterDownload" : "UNSET",(null,"UNSET","TRUE","FALSE")
        "priority" : null, (null,"HIGHEST","HIGHER","HIGH","DEFAULT","LOW","LOWER","LOWEST")
        "type" : "NORMAL", ("NORMAL")
        "enabled" : null,(null,"UNSET","TRUE","FALSE")
        "autoStart" : "UNSET",(null,"UNSET","TRUE","FALSE")
        "forcedStart" : "UNSET",(null,"UNSET","TRUE","FALSE")
        "addOfflineLink" : true,(true|false)
        "extractPasswords" : null,(null,["pw1","pw2"])
        "downloadPassword" : null,(null|"String")
        "filename" : null,(null|"String")
        "autoConfirm" : "UNSET", (null,"UNSET","TRUE","FALSE")
        "comment" : null,(null|"String")
        "text" : null,(null|"String")
        "packageName" : null, (null|"String")
        "deepAnalyseEnabled" : false,(true|false)
        "setBeforePackagizerEnabled" : false(true|false)
    }
    '''
    text: str
    filename: str
    downloadFolder: str
    autoconfirm: Optional[str]
    autostart: Optional[str]
    extractAfterDownload: bool

def write_crawljob(links: List[Data]) -> bool:

    jobs: List[CrawlJob] = []
    downloadFolder = join(getcwd(), 'tabs')

    for data in links:
        match data:
            case {'filename': filename, 'link': link, 'ext': ext}:
                jobs.append({
                    'text': link,
                    'filename': filename + ext,
                    'downloadFolder': downloadFolder,
                    'extractAfterDownload': "FALSE"
                })
                continue
            
            case {'filename': filename, 'link': link}:
                jobs.append({
                    'text': link,
                    'filename': filename,
                    'downloadFolder': downloadFolder,
                    'extractAfterDownload': "FALSE"
                })
                continue

    with open('download.crawljob', 'w') as file:
        dump(jobs, file)

    return True

def write_readme(links: List[Data]) -> None:
    with open('./Readme.md', 'w') as file:
        for data in links:
            if data.get('category'):
                file.write(f"{data['identity']}. {data['filename']}\n")
                file.write(f'\t- [{data["category"]}]({data["link"]})\n')
                continue
            file.write(f"{data['identity']}. [{data['filename']}]({data['link']})\n\n")
        