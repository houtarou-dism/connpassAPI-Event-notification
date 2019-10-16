#最初、データベースにイベントデータを入れるためのコード

import re
import json
import requests
import time
import datetime
import mysql.connector as mydb
from datetime import datetime as dt


dt_today = datetime.date.today()        #今日の日付を取得

dt_today = dt_today.strftime('%Y-%m-%d')         #dateから文字列に変換
dt_today = dt.strptime(dt_today, '%Y-%m-%d')        #文字列からdatetimeに変換

# コネクション
conn = mydb.connect(
    host='127.0.0.1',
    port='3306',
    user='ユーザー名',
    password='パスワード',
    database='データベース名'
)

# DB操作用にカーソルを作成
cur = conn.cursor()

r = 'https://connpass.com/api/v1/event/?keyword=福岡&order=3&count=100'        #イベント検索      
slack_webhook = '自分のslackのwebhook URL'     #webhook URL

data = requests.get(r).json()
  
for key in data['events']:

    key_id = key['event_id']        #イベントID
    key_title = key['title']        #タイトル
    key_catch = key['catch']        #キャッチ
    key_address = key['address']        #開催場所
    key_started_at = key['started_at']      #イベント開催日時
    key_event_url = key['event_url']        #connpass.com 
    key_started_at = key_started_at.split('T')[0]       #T以降の文字列を削除
    key_started_at = dt.strptime(key_started_at, '%Y-%m-%d')

    
    if re.compile("キーワード").search(str(key_address)):  #key_addressの文字列に対し、キーワードを部分一致

        if re.compile("キーワード").search(str(key_title)):      #弾きたい文字列を書く
            continue
        else:

            if dt_today <= key_started_at:      #取得日より後

                key_started_at = key_started_at.strftime('%Y-%m-%d')       #datetimeをstrに変換
                #新規のイベントをデータベースに追加
                cur.execute("INSERT INTO data (id, title, catchs, dates, urls) VALUES (%s, %s, %s, %s, %s)", 
                (key_id, key_title, key_catch, key_started_at, key_event_url))

conn.commit()

# DB操作が終わったらカーソルとコネクションを閉じる
cur.close()
conn.close()