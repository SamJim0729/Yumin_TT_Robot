import os
import sys
from flask import Flask, request, abort
from flask_session import Session

from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, MessagingApiBlob
from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3 import WebhookHandler

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'controllers'))
from controllers.line_bot_controller_sdk_v3 import LineBotController
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from config.config import Config

config = Config(lambda_role='lambda_main')

app = Flask(__name__)
app.json.ensure_ascii = False

configuration = Configuration(access_token=config.CHANNEL_ACCESS_TOKEN)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
line_bot_blob_api = MessagingApiBlob(api_client)
bot_controller = LineBotController(line_bot_api, line_bot_blob_api)
handler = WebhookHandler(config.CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    """
    LINE Webhook 入口點
    1. 取得請求中的簽名，並驗證合法性
    2. 解析請求內容，交給 `handler` 處理
    """
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """
    處理 LINE Bot 的文字訊息事件
    交由 `LineBotController` 來處理訊息
    """
    bot_controller.handle_message_event(event)

@handler.add(PostbackEvent)
def handle_postback(event):
     """
    處理 LINE Bot 的按鈕點擊事件
    交由 `LineBotController` 來處理 Postback 事件
    """
     bot_controller.handle_postback_event(event)



