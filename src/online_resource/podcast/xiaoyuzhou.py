import logging
from pathlib import Path
from typing import Tuple, List

import requests
from bs4 import BeautifulSoup

from podcast_download.common import audio_download


def parse_audio_link(fmid: str) -> Tuple[str, List[str]]:
    url = f"https://www.xiaoyuzhoufm.com/episode/{fmid}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features="html.parser")
    audio_link = (soup.find_all("meta", {"property": "og:audio"})[0])["content"]
    audio_title = (soup.find_all("meta", {"property": "og:title"})[0])["content"]
    return audio_title, [audio_link]


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    fmid = "649fa34563a61044f4f42df4"
    title, audio_links = parse_audio_link(fmid)
    fns = audio_download(title, fmid, audio_links, destination)
