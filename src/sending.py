import os
import requests

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

class Sending:

    def __init__(self) -> None:
        self.LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"

    def to_line(self, message: str, image_urls: list, token: str=LINE_NOTIFY_TOKEN) -> None:
        if not token:
            return
        elif not message:
            return

        isImage = len(image_urls)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        if message and isImage == 0:
            data = {
                "message": f"\n{message}",
                "notificationDisabled": "true"
            }
            requests.post(self.LINE_NOTIFY_URL, headers=headers, data=data)
            return

        i = 0

        for image_url in image_urls:
            data = {
                "imageThumbnail": image_url,
                "imageFullsize": image_url,
                "message": "画像↓",
                "notificationDisabled": "true"
            }

            if i == 0:
                data["message"] = f"\n{message}"

            requests.post(self.LINE_NOTIFY_URL, headers=headers, data=data)
            i+=1

    def to_discord(self, message: str, webhook: str=DISCORD_WEBHOOK_URL) -> None:
        if not webhook:
            return

        data = {
            "content": message
        }
        requests.post(webhook, data=data)