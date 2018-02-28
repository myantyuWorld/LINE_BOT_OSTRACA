# -*- coding: utf-8 -*-
import os
import urllib2
import datetime
from bs4 import BeautifulSoup       # webスクレイピング用
from flask import Flask, jsonify, request    # Flask, JSON用  
from flask_cors import CORS         # CORS対策クロスオーバーリソースシェアリング
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
CORS(app) # <-追加

line_bot_api = LineBotApi('F4UzKoSzxVVvwKJ2wqrIJnwAbJ5nVYI3o5YD7Lp5OfoQkpOAtSkPpN0OwRHXwG3SEnd7zwinxx7IPjLX99g5X96LlLTWW9mPnEtrkhvqD/tWmpf5oL/m+0WNZ4TTNBuU5rIapkUB3Xo1E5xmuywh7gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('35a57e3c8b09c2ca733c8a2c0dd51ab0')

@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    print(body["message"])
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# Beautifulsoup4を用いた時刻表の時刻抽出メソッド（共通）
# def bs4method(fileName):
#     soup = BeautifulSoup(open(fileName), "html.parser")
#     # 時／分の塊を取得する    
#     div = soup.find('div', class_='time-tables')
#     timetables = div.find_all('dl')
#     # 現在時刻を取得
#     now = "{0:%H}".format(datetime.datetime.now())
#     minute = "{0:%M}".format(datetime.datetime.now())
#     print "now hour --> " + now + " : " + minute #現在時刻
#     nowTimeTable =  timetables[int(now) - 6] # 現在の時間の時刻表

#     # その時間の時刻表を取得
#     timeframe = nowTimeTable.find_all('span', class_='time') 
#     minlist = [] 
#     for timeframe in timeframe:
#         # いまより後の時刻表を表示
#         if minute < timeframe.string: 
#             minlist.append(timeframe.string)
    
#     # 分が45以降なら、次の時間の時刻表を検査する
#     if int(minute) >= 45:
#         now = int(now) + 1 # 時間を1時間すすめる
#         nowTimeTable = timetables[int(now) - 6]
#         timeframe = nowTimeTable.find_all('span', class_='time') 
#         for var in range(0,5):
#             minlist.append(timeframe[var].string)
    
#     # JSONの形式
#     timetable = {
#         'hour': now,
#         'min' : minlist
#     }

#     return timetable


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)