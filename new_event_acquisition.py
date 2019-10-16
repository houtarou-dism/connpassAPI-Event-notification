#新しいイベントを追加するコード

import re
import json
import requests
import time
import datetime
import mysql.connector as mydb
from datetime import datetime as dt


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

dt_today = datetime.date.today()        #今日の日付を取得

dt_today = dt_today.strftime('%Y-%m-%d')         #dateから文字列に変換
dt_today = dt.strptime(dt_today, '%Y-%m-%d')        #文字列からdatetimeに変換

r = 'https://connpass.com/api/v1/event/?keyword=福岡&order=3&count=100'        #イベント検索      
slack_webhook = '自分のslackのwebhook URL'     #webhook URL

data = requests.get(r).json()

cur.execute('SELECT id FROM data')      #データを取得（id）
id_date = cur.fetchall()

dict_store = {}

for key in data['events']:

    count=0
    
    key_id = key['event_id']        #イベントID
    key_title = key['title']        #タイトル
    key_catch = key['catch']        #キャッチ
    key_address = key['address']        #開催場所
    key_started_at = key['started_at']      #イベント開催日時
    key_event_url = key['event_url']        #connpass.com 上のURL
    key_started_at = key_started_at.split('T')[0]       #T以降の文字列を削除
    key_started_at = dt.strptime(key_started_at, '%Y-%m-%d')

    
    if re.compile("キーワード").search(str(key_address)):  #key_addressの文字列に対し、キーワードを部分一致

        if re.compile("キーワード").search(str(key_title)):      #弾きたい文字列を書く
            continue
        else:
            
            if dt_today <= key_started_at:      #取得日より後

                for i in id_date:

                    #新規のデータか比較
                    if str(key_id) != str(i)[1:7]:      #リストの値"(数値,)"で出てくるのを"数値"だけ抽出して比較
                        count+=1
                    else:
                        continue

                if count == len(id_date):

                    key_started_at = key_started_at.strftime('%Y-%m-%d')       #datetimeをstrに変換
                    
                    #新規のイベントをデータベースに追加
                    cur.execute("INSERT INTO data (id, title, catchs, dates, urls) VALUES (%s, %s, %s, %s, %s)",
                    (key_id, key_title, key_catch, key_started_at, key_event_url))
                    
                    store_summary = [key_title, key_catch, key_started_at, key_event_url]      #リストにリストを追加
                    dict_store[key_id] = store_summary      #辞書にリスト追加　キーはid


conn.commit()

# DB操作が終わったらカーソルとコネクションを閉じる
cur.close()
conn.close()

if dict_store != {}:

    dict_store = json.dumps(dict_store, indent=4, ensure_ascii=False)

    payload = {
        "text": dict_store
    }

    requests.post(slack_webhook, data=json.dumps(payload))
else:
    payload = {
        "text": "新規イベントはありません"
    }

    requests.post(slack_webhook, data=json.dumps(payload))