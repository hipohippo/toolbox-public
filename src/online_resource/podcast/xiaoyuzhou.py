import logging
from pathlib import Path
from typing import Tuple, List

import requests
from bs4 import BeautifulSoup

from online_resource.podcast.common import audio_download

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "cookie": "_jid=26cf50f3cc404df5babb4f26cc22fa26; SERVERID=a0dfe0218d4c9ae1b90b439f8cf67ba4|1727659237|1727659153",
    "if-none-match": "2zh14ppl7i1py7",
    "priority": "u=1, i",
    "purpose": "prefetch",
    "referer": "https://www.xiaoyuzhoufm.com/episode/66da5946bfd7110df49820a2",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}


def parse_audio_link(fmid: str) -> Tuple[str, List[str]]:
    url = f"https://www.xiaoyuzhoufm.com/episode/{fmid}"
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.content, features="html.parser")
    audio_link = (soup.find_all("meta", {"property": "og:audio"})[0])["content"]
    audio_title = (soup.find_all("meta", {"property": "og:title"})[0])["content"]
    return audio_title, [audio_link]


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    fmid = "66da5946bfd7110df49820a2"
    destination_folder = f"~/downloads"
    title, audio_links = parse_audio_link(fmid)
    title = title.replace("？","").replace("?","").replace("：","").replace(":", "")
    fns = audio_download(title, fmid, audio_links, Path(destination_folder))
