import json
from bs4 import BeautifulSoup
import re
from telegram import InputMediaPhoto
from urllib.parse import urlparse, parse_qs

from preview import Preview
from utils.clean_html import clean_article_html
from utils.tools import text_length
from enums import MSG_TYPE

IMG_HOST_URL = "https://cdn.cdnjson.com/tva1.sinaimg.cn/large/"


class Status(object):
    def __init__(self, js):
        self.js = js
        if "page_info" in js:
            self.type = js["page_info"]["type"]
        else:
            self.type = "regular"
        self.user = js["user"]
        if "longText" in js:  # do NOT use js['isLongText'] to tell
            self.text = js["longText"]["longTextContent"]
        else:
            self.text = js["text"]
        self.author = js["user"]["screen_name"]
        self.pic_ids = js["pic_ids"]
        self.retweet = None
        if "retweeted_status" in js:
            self.retweet = Status(js["retweeted_status"])
        soup_text = f"<b>@{self.author}</b>: {self.text}"
        self.soup = BeautifulSoup(soup_text, "html.parser")
        self.cleaned = False

    def has_video(self):
        return self.type == "video" or (self.retweet and self.retweet.type == "video")

    def get_video(self):
        if self.type == "video":
            return self.js["page_info"]["urls"]["mp4_hd_mp4"]
        else:
            return self.retweet.get_video()

    def clean(self):
        if not self.cleaned:
            for item in self.soup.find_all("span", {"class": "url-icon"}):
                img = item.find("img")
                if img.has_attr("alt"):
                    item.replace_with(img["alt"])
            for img in self.soup.find_all("img", {"style": "width: 1rem;height: 1rem"}):
                img.replace_with("")
            for tag in self.soup.find_all("br"):
                tag.replace_with("\n")
            for a in self.soup.find_all("a"):
                url = a["href"]
                if url.startswith("https://weibo.cn/sinaurl?"):
                    a["href"] = parse_qs(urlparse(url).query)["u"][0]
            self.text = str(self.soup)
        self.cleaned = True

    def get_string(self):
        self.clean()
        text = self.text
        text = clean_article_html(text)
        if self.retweet:
            text += "\n----------\n"
            text += self.retweet.get_string()
        return text

    def get_content(self):
        self.clean()
        new_str = "".join([f"<p>{item}</p>" for item in str(self.soup).split("\n")])
        self.soup = BeautifulSoup(new_str, "html.parser")
        soup = self.soup
        js = self.js
        for pic_id in self.pic_ids:
            soup.append(soup.new_tag("img", src=f"{IMG_HOST_URL}{pic_id}.jpg"))
        if self.retweet:
            soup.append(soup.new_tag("hr"))
            soup.append(self.retweet.get_content())
        if self.has_video():
            video_url = status.get_video()
            video = soup.new_tag("video", src=video_url)
            soup.append(video)
        return soup


class Weibo(Preview):
    def __init__(self, pattern: re.Pattern, headers) -> None:
        super(Weibo, self).__init__(pattern, headers=headers)

    async def clean_url(self):
        if self.URL.startswith("https://weibo.com"):
            self.URL = f"https://m.weibo.cn/status/{self.URL.split('/')[4]}"

    def viewer(self, res):
        json_string = res.text.split("$render_data = [")[1].split("][0] ||")[0]
        js = json.loads(json_string)
        title = js["status"]["status_title"]
        status = Status(js["status"])
        html_string = status.get_string()
        soup = status.get_content()
        if text_length(soup.text) <= 4800:
            if status.pic_ids:
                media = [InputMediaPhoto(f"{IMG_HOST_URL}{pic_id}.jpg") for pic_id in status.pic_ids]
                return (MSG_TYPE.DIRECT_PHOTOS, (media, html_string))
            elif status.has_video():  # TODO: only handle video of length <= 120
                video_url = status.get_video()
                return (MSG_TYPE.DIRECT_VIDEO, (video_url, html_string))
            else:
                return (MSG_TYPE.DIRECT_TEXT, html_string)
        content = status.get_content()
        author = js["status"]["user"]["screen_name"]
        return (MSG_TYPE.TELEGRAGH_ARTICLES, (title, author, content))


WEIBO_PATTERN = re.compile(r"(\b(?:https?://)?m\.weibo\.cn/status/\S*|https://weibo.com/\d+/\S+)")
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57"
}
weibo = Weibo(WEIBO_PATTERN, headers)
