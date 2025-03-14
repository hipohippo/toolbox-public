import io  # Note: io.BytesIO is StringIO.StringIO on Python2.
import logging
from pathlib import Path

import PIL
import httpx
import requests
from PIL import Image

"""
https://jdhao.github.io/2020/06/21/faster_im_download_with_requests/
stream or not?
As said in the previous post, for large files, we may want to use stream parameter when making the request, 
which will reduce the memory overhead. So we have two ways to get the binary image from the response:

using response.content
using response.raw.read()  -> stream=True is required
"""


# Using .content (simplest/official) (see Zhenyi Zhang's answer):
def todo_refactor():
    r = requests.get("http://lorempixel.com/400/200")
    r.raise_for_status()
    with io.BytesIO(r.content) as f:
        with Image.open(f) as img:
            img.show()

    # Using .raw (see Martijn Pieters's answer):
    r = requests.get("http://lorempixel.com/400/200", stream=True)
    r.raise_for_status()
    r.raw.decode_content = (
        True  # Required to decompress gzip/deflate compressed responses.
    )
    with PIL.Image.open(r.raw) as img:
        img.show()
    r.close()  # Safety when stream=True ensure the connection is released.


def download_stream_chunk_httpx(url: str, dest: Path):
    with httpx.stream("GET", url) as resp, open(dest, "wb") as f:
        for data in resp.iter_bytes(4096):
            f.write(data)


def download_stream_chunk(url: str, dest: Path):
    resp = requests.get(url, stream=True)
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(4096):
            f.write(chunk)


def request_download(url: str, dest: Path):
    download_stream_chunk(url, dest)
    logging.info(f"downloaded to {dest} - {(dest.stat().st_size) / 1048576} MB")
