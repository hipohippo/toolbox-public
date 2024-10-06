import re
from pathlib import Path
from typing import List

from request_common.request_download_file import request_download

EMOJI_PATTERN = re.compile(
    "(["  # .* removed
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "])",
    flags=re.UNICODE,
)


def audio_download(title: str, episode_id: str, audio_links: List[str], dest_folder: Path) -> List[Path]:
    fns = []
    for idx, audio_link in enumerate(audio_links):
        file_ext = audio_link.split(".")[-1].split("?")[0]
        title = re.sub(EMOJI_PATTERN, r"", title)
        title = re.sub(r"[#/&;:'<>\|\"\?\.\*\^\\]", "", title)
        fn = (dest_folder / f"{title}_{episode_id}_{idx}.{file_ext}").expanduser()
        request_download(audio_link, fn)
        fns.append(fn)
    return fns
