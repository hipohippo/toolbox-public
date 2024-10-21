import requests
from enum import Enum

from neodb.item import NeoDBItem


class ShelfType(Enum):
    WISHLIST = "wishlist"
    COMPLETE = "complete"
    PROGRESS = "progress"


class Category(Enum):
    TV = "tv"
    MOVIE = "movie"
    BOOK = "book"


class Visibility(Enum):
    PUBLIC = 0
    FOLLOWERS = 1
    SELF = 2


class FieldName(Enum):
    SHELF_TYPE = "shelf_type"  # wishlist, complete, progress
    VISIBILITY = "visibility"  # 0, 1, 2
    RATING_GRADE = "rating_grade"  # 1-10
    COMMENT_TEXT = "comment_text"
    TAGS = "tags"  # list of strings as tags
    SHARE_TO_MASTODON = "share_to_mastodon"  # true or false


class NeoDB:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://neodb.social/api"
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json",
        }

    def mark_complete(self, item_uuid: str, comment_text: str) -> tuple[int, dict]:
        endpoint = f"{self.base_url}/me/shelf/item/{item_uuid}"
        fields = {
            FieldName.SHELF_TYPE.value: ShelfType.COMPLETE.value,
            FieldName.VISIBILITY.value: Visibility.SELF.value,
            FieldName.COMMENT_TEXT.value: comment_text,
            FieldName.TAGS.value: [],
            FieldName.SHARE_TO_MASTODON.value: False,
        }
        response = requests.post(endpoint, headers=self.headers, json=fields)
        return response.status_code, response.json()

    def mark_wish(self, item_uuid: str, comment_text: str) -> tuple[int, dict]:
        endpoint = f"{self.base_url}/me/shelf/item/{item_uuid}"
        fields = {
            FieldName.SHELF_TYPE.value: ShelfType.WISHLIST.value,
            FieldName.VISIBILITY.value: Visibility.SELF.value,
            FieldName.COMMENT_TEXT.value: comment_text,
            FieldName.TAGS.value: [],
            FieldName.SHARE_TO_MASTODON.value: False,
        }
        response = requests.post(endpoint, headers=self.headers, json=fields)
        return response.status_code, response.json()

    def get_mark(self, item_uuid: str) -> tuple[int, dict]:
        endpoint = f"{self.base_url}/me/shelf/item/{item_uuid}"
        response = requests.get(endpoint, headers=self.headers)
        return response.status_code, response.json()

    def search_items(self, query: str, page_number: int) -> tuple[int, dict]:
        endpoint = f"{self.base_url}/catalog/search?"
        params = {
            "query": query,
            "page": page_number,
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code == 200:
            results = response.json().get("data", [])
            items = [NeoDBItem(item) for item in results]
            return response.status_code, items
        else:
            return response.status_code, []
