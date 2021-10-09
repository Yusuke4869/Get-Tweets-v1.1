import os
import re
import json
from typing import Union

import requests
from requests_oauthlib import OAuth1
from datetime import datetime, timedelta, timezone

from src.settings import settings
from src.db import DataBase
from src.sending import Sending

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_KEY_SECRET = os.environ["CONSUMER_KEY_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

JST = timezone(timedelta(hours=+9), "JST")
API_URL = "https://api.twitter.com/1.1/search/tweets.json"
URL_Pattern = "https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+"

sending = Sending()

db_names = settings.get_db_names()
db = DataBase(db_names["database_name"], db_names["collection_name"])

class Execution:

    def __init__(self) -> None:
        self.Twitter = OAuth1(CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def mark_url(self, url) -> str:
        marked_url = f"begin_{url}_end"
        return marked_url

    def regenerate_text(self, content: str, urls: Union[list, None]=None) -> Union[str, None]:
        if not content:
            return None

        if not urls:
            new_content = re.sub(URL_Pattern, "", content).replace("\n\n\n", "\n\n").rstrip()
            return new_content

        tmp_content = content

        # 全てのURLに印を付ける
        match_urls = re.findall(URL_Pattern, content)
        for url in match_urls:
            tmp_content = re.sub(url, self.mark_url(url), tmp_content)

        # ツイートに含まれる短縮URLを本来のURLに置き換え
        for url in urls:
            tmp_content = re.sub(self.mark_url(url["url"]), url["expanded_url"], tmp_content)

        # その他のURLを取り除く
        new_content = re.sub(self.mark_url(URL_Pattern), "", tmp_content).replace("\n\n\n", "\n\n").rstrip()

        return new_content

    def running(self) -> None:
        try:
            data = db.find_one({"name": settings.get_db_program_name()})
            since = data["since"]
        except Exception as e:
            since = datetime.now(JST).strftime("%Y-%m-%d_00:00:00")

        parameters = {
            "count": 100,
            "q": f"{settings.get_searchword()} since:{since}_JST",
            # Tweet全文取得
            "tweet_mode": "extended"
        }

        res = requests.get(API_URL, params=parameters, auth=self.Twitter)

        if res.status_code != 200:
            return

        # 検索と検索時刻取得
        now = datetime.now(JST).strftime("%Y-%m-%d_%H:%M:%S")
        tweets = json.loads(res.text)

        for tweet in reversed(tweets["statuses"]):
            tweeturl = f"https://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}"

            user = tweet["user"]["name"]
            isRetweet = False
            media_urls = []

            # リツイートかどうか
            if "retweeted_status" in tweet:
                isRetweet = True
                user_tweet = tweet
                tweet = tweet["retweeted_status"]

            tweet_content = self.regenerate_text(tweet["full_text"], tweet["entities"]["urls"])

            if isRetweet:
                user_tweet_content = self.regenerate_text(user_tweet["full_text"], user_tweet["entities"]["urls"])
                # 引用リツイート
                if re.match("(RT)", user_tweet_content) == None:
                    text = f"{user}\n\n{user_tweet_content}\n\nRT {tweet_content}\n\n{tweeturl}"
                else:
                    text = f"{user}\n\nRT {tweet_content}\n\n{tweeturl}"
            else:
                text = f"{user}\n\n{tweet_content}\n\n{tweeturl}"

            # 引用リツイート画像
            if isRetweet and "extended_entities" in user_tweet:
                for data in user_tweet["extended_entities"]["media"]:
                    url = data["media_url_https"]
                    media_urls.append(url)

            if "extended_entities" in tweet:
                for data in tweet["extended_entities"]["media"]:
                    url = data["media_url_https"]
                    media_urls.append(url)

            # LINEに送信
            if text and media_urls and settings.sending_to_line():
                sending.to_line(text, media_urls)

            # Discordに送信
            if tweeturl and settings.sending_to_discord():
                sending.to_discord(tweeturl)

        # nowを保存
        setting_data = db.find_one({"name": settings.get_db_program_name()})

        if not setting_data:
            setting_data = {
                "name": settings.get_db_program_name()
            }

        setting_data["since"] = now
        db.update_one({"name": settings.get_db_program_name()}, setting_data)