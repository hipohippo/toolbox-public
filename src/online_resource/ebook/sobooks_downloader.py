import re
from pathlib import Path
from typing import Tuple, List

import requests

from request_common.request_download_file import request_download


def get_book_url(year: str, month: str, bookid: int) -> str:
    return f"https://sobooks.cloud/{year}/{month}/{bookid}.epub"


def get_page_url(bookid: int) -> str:
    return f"https://sobooks.cc/books/{bookid}.html"


def get_download_url(bookid: int) -> Tuple[str, str, str]:
    bookpage = requests.get(get_page_url(bookid))
    time_search = re.search(r".*时间：</strong>(\d{4})-(\d{2})-(\d{2}).*", bookpage.text)
    isbn = re.search(r".*ISBN：</strong>(\d{13}).*", bookpage.text)[1]
    year = time_search[1]
    month = time_search[2]
    book_title_search = re.search(r".*<title>(.*) by", bookpage.text)
    book_title = book_title_search[1]
    return (f"https://sobooks.cloud/{year}/{month}/{bookid}.epub", book_title, isbn)


def batch_download(ids: List[int], destination: Path):
    for bookid in ids:
        try:
            book_file_url, book_title, book_isbn = get_download_url(bookid)
            request_download(book_file_url, destination)
            print(f"downloaded {bookid}， {book_title}")
        except Exception as e:
            print(f"failed to download {bookid}", e)


if __name__ == "__main__":
    batch_download([21497], ...)
