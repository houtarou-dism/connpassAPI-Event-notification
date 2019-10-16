# connpassAPI-event-notification

connpassAPIとwebhookを利用して、slackへ新規イベントを通知するプログラムを書きました。（pythonとmysqlの練習）  

**data_acquisition.py**  
最初、データベースにイベントデータを入れるためのコード

**new_event_acquisition.py**  
新しいイベントをデータベースに追加するコード

**event.sql**  
テーブル作成のsql

**event_data.py**  
手動でイベント検索する用のコード
