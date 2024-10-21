def safe_float(value: str) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


class NeoDBItem:
    def __init__(self, raw_data: dict):
        """
        书: type=Edition, category=book
        电视剧: type=TVSeason, category=tv
        播客（不明白）: type=Podcast, category=podcast
        播客（忽左忽右）: type=Album, category=music
        电影: type=Movie, category=movie
        音乐: type=Album, category=music
        Show: type=Performance, category=performance
        游戏: type=Game, category=game
        """
        self.raw_data = raw_data
        self.url: str = raw_data.get("id", "INVALID")
        self.uuid: str = raw_data.get("uuid", "INVALID")
        self.parent_uuid: str = raw_data.get("parent_uuid", "")
        self.external_resources: list[dict] = raw_data.get("external_resources", [])
        self.type = raw_data.get("type", "")  # TVSeason, Edition, Album
        self.category: str = raw_data.get(
            "category", ""
        )  # tv, book, movie, music, podcast
        self.title: str = raw_data.get("title", "")
        self.display_title: str = raw_data.get("display_title", "")
        self.description: str = raw_data.get("description", "")
        self.publisher: str = raw_data.get("publisher", "")
        self.year: str = raw_data.get("year", "")
        self.cover_image_url: str = raw_data.get("cover_image_url", "")
        self.rating: float = safe_float(raw_data.get("rating", 0.0))
        self.director: str = "_".join(raw_data.get("director", []))
        self.author: str = "_".join(raw_data.get("author", []))
        self.artist: str = "_".join(raw_data.get("artist", []))
        self.host: str = "_".join(raw_data.get("host", []))

        actor_list = raw_data.get("actor", [])[:10]
        if actor_list:
            if actor_list[0] is not None and isinstance(actor_list[0], dict):
                self.actor = "_".join([actor["name"] for actor in actor_list])
            elif actor_list[0] is not None and isinstance(actor_list[0], str):
                self.actor = "_".join(actor_list)
            else:
                self.actor = ""
        else:
            self.actor = ""

        self.by: str = {
            "book": self.author,
            "music": self.artist,
            "tv": self.director,
            "movie": self.director,
            "podcast": self.host,
            "performance": self.director,
            "game": self.publisher,
        }.get(self.category, "")

    def __str__(self) -> str:
        return (
            f"URL: {self.url}\n"
            f"UUID: {self.uuid}\n"
            f"Parent UUID: {self.parent_uuid}\n"
            f"External Resources: {self.external_resources}\n"
            f"Type: {self.type}\n"
            f"Category: {self.category}\n"
            f"Title: {self.title}\n"
            f"Display Title: {self.display_title}\n"
            f"Description: {self.description}\n"
            f"Publisher: {self.publisher}\n"
            f"Year: {self.year}\n"
            f"Cover Image URL: {self.cover_image_url}\n"
            f"Rating: {self.rating}\n"
            f"Director: {self.director}\n"
            f"Author: {self.author}\n"
            f"Actor: {self.actor}\n"
            f"By: {self.by}"
        )

    def __repr__(self) -> str:
        return self.__str__()
