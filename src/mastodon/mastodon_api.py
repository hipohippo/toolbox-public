import requests
from typing import List, Optional


class Mastodon:
    def __init__(self, api_key: str, instance_url: str):
        self.api_key = api_key
        self.instance_url = instance_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def post(
        self,
        status: str,
        media_ids: Optional[List[str]] = None,
        visibility: str = "public",
    ) -> dict:
        """
        Post a status to Mastodon, optionally with attached media.

        :param status: The text content of the post
        :param media_ids: List of media IDs to attach to the post
        :param visibility: Visibility of the post (public, unlisted, private, direct)
        :return: The response from the Mastodon API
        """
        endpoint = f"{self.instance_url}/api/v1/statuses"
        data = {
            "status": status,
            "visibility": visibility,
        }
        if media_ids:
            data["media_ids"] = media_ids

        response = requests.post(endpoint, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def upload_media(self, file_path: str, description: Optional[str] = None) -> str:
        """
        Upload a media file to Mastodon.

        :param file_path: Path to the media file
        :param description: Optional description for the media
        :return: The media ID
        """
        endpoint = f"{self.instance_url}/api/v2/media"
        files = {"file": open(file_path, "rb")}
        data = {}
        if description:
            data["description"] = description

        headers = self.headers.copy()
        headers.pop("Content-Type", None)  # Remove Content-Type for file upload

        response = requests.post(endpoint, files=files, data=data, headers=headers)
        response.raise_for_status()
        return response.json()["id"]

    def post_with_media(
        self,
        status: str,
        file_paths: List[str],
        descriptions: Optional[List[str]] = None,
        visibility: str = "public",
    ) -> dict:
        """
        Post a status with attached media to Mastodon.

        :param status: The text content of the post
        :param file_paths: List of paths to media files
        :param descriptions: Optional list of descriptions for each media file
        :param visibility: Visibility of the post (public, unlisted, private, direct)
        :return: The response from the Mastodon API
        """
        if descriptions and len(file_paths) != len(descriptions):
            raise ValueError("Number of file paths must match number of descriptions")

        media_ids = []
        for i, file_path in enumerate(file_paths):
            description = descriptions[i] if descriptions else None
            media_id = self.upload_media(file_path, description)
            media_ids.append(media_id)

        return self.post(status, media_ids, visibility)


if __name__ == "__main__":
    # Initialize the Mastodon client
    mastodon = Mastodon(
        api_key="your_api_key_here", instance_url="https://m.cmx.im"
    )

    # Post a simple text status
    mastodon.post("Hello, Mastodon!")

    # Post a status with a single image
    mastodon.post_with_media("Check out this image!", ["path/to/image.jpg"])

    # Post a status with multiple images and descriptions
    mastodon.post_with_media(
        "Multiple images with descriptions",
        ["path/to/image1.jpg", "path/to/image2.jpg"],
        ["Description for image 1", "Description for image 2"],
    )
