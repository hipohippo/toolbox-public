import re
from pathlib import Path
from typing import List

from request_common.request_download_file import request_download

EMOJI_PATTERN = re.compile(
    "(["  # .* removed
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f680-\U0001f6ff"  # transport & map symbols
    "\U0001f1e0-\U0001f1ff"  # flags (iOS)
    "])",
    flags=re.UNICODE,
)


def audio_download(
    title: str, episode_id: str, audio_links: List[str], dest_folder: Path
) -> List[Path]:
    fns = []
    for idx, audio_link in enumerate(audio_links):
        file_ext = audio_link.split(".")[-1].split("?")[0]
        title = re.sub(EMOJI_PATTERN, r"", title)
        title = re.sub(r"[#/&;:'<>\|\"\?\.\*\^\\]", "", title)
        fn = (dest_folder / f"{title}_{episode_id}_{idx}.{file_ext}").expanduser()
        request_download(audio_link, fn)
        fns.append(fn)
    return fns
