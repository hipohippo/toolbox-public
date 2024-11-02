from mastodon import Mastodon
from configparser import ConfigParser

this_config = ConfigParser()
this_config.read("config.ini")

api = Mastodon(
    client_id=this_config["mastodon"]["client_id"],
    client_secret=this_config["mastodon"]["client_secret"],
    access_token=this_config["mastodon"]["access_token"],
    api_base_url="https://m.cmx.im",
)

api.toot("测试tgbot")

media_ids = []
media = api.media_post(media_path / media_file, mime_type="image/png")
media_ids.append(media["id"])
api.status_post("测试tgbot", media_ids=media_ids)
