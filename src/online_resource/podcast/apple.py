import re
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from podcast_download.common import audio_download


def parse_audio_link(url: str) -> Tuple[str, List[str]]:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    title = soup.find("meta", {"property": "og:title"})["content"]
    script_content = soup.find("script", {"id": "shoebox-media-api-cache-amp-podcasts"})
    script_content = script_content.string.replace(r"\"", '"')
    reg = r'"assetUrl":"(https:[^"]+)"'
    links = re.findall(reg, script_content)
    return title[1:], links


if __name__ == "__main__":
    url = "https://podcasts.apple.com/us/podcast/return-stacked-bonds-managed-futures-etf/id1402620531?i=1000620646427"
    url = "https://podcasts.apple.com/us/podcast/126-noam-chomsky-decoding-the-human-mind-neural-nets/id1438378439?i=1000618027273"
    url = "https://podcasts.apple.com/us/podcast/ep08-%E7%A5%9E%E5%A5%87%E7%9A%84%E5%A5%A5%E7%89%B9%E6%9B%BC%E5%8D%A1%E7%89%87-%E5%92%8C%E5%AE%83%E7%9A%84%E4%B8%89%E4%B8%AA%E6%9A%97%E7%BA%BF%E6%95%85%E4%BA%8B/id1625255175?i=1000579313751"
    episode_id = re.findall(r".+\?i=(\w+)", url)[0]
    title, links = parse_audio_link(url)
    fns = audio_download(title, episode_id, links, destination)
