# Twitter Search  

Twitterを定期的に検索します.  

## Requirement  

- Python3
- Twitter API Access Tokens
- MongoDB Atlas (Customizable and Changeable)

(Optional)
- LINE Notify TOKEN
- Discord Webhook URL

## Run  

`Linux, macOS`  
```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python3 main.py
```

`Windows`  
```shell
$ python3 -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
$ python3 main.py
```

## Settings  

`settings.yaml`で設定を変更できます.  

### search  

|項目|説明|型|初期値|
|:-:|:-:|:-:|:-:|
|account_ids|検索するアカウントのID|list|[null]|
|and_words|AND検索で使用するワード|list|[null]|
|or_words|OR検索で使用するワード|list|[null]|
|ignore_words|無視するワード|list|[null]|

### sending  

|項目|説明|型|初期値|
|:-:|:-:|:-:|:-:|
|line|LINEに送信するか|boolean|false|
|discord|Discordに送信するか|boolean|false|

### database  

<small>MongoDB Atlasに関する設定です.</small>  

|項目|説明|型|初期値|
|:-:|:-:|:-:|:-:|
|database_name|データベースの名前|string|bot|
|collection_name|コレクションの名前|string|twitter|
|program_name|このプログラムの名前<br>上2項目が同じものにおいて, 一意の名前|string|template|

### control  

|項目|説明|型|初期値|
|:-:|:-:|:-:|:-:|
|interval|実行間隔(分)|integer|5|

## Anything else  

`server.py`を動かす必要はありません.  
必要に応じて動作させてください.  