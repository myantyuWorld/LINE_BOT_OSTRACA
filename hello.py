import os
from flask import Flask

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

line_bot_api = LineBotApi('F4UzKoSzxVVvwKJ2wqrIJnwAbJ5nVYI3o5YD7Lp5OfoQkpOAtSkPpN0OwRHXwG3SEnd7zwinxx7IPjLX99g5X96LlLTWW9mPnEtrkhvqD/tWmpf5oL/m+0WNZ4TTNBuU5rIapkUB3Xo1E5xmuywh7gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('35a57e3c8b09c2ca733c8a2c0dd51ab0')

@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/good')
def good():
    name = "Good"
    return name

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
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


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)