
import re
import os
import sys
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'views'))
from views.message_templates_sdk_v3 import *

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'))
from models.llm_model import LangChainModel
from models.conversation_history import ConversationHistory

class LineBotController:
    """
    LINE Bot 控制器，處理訊息與 Postback 事件，並與 LangChain AI 整合
    """
    def __init__(self, line_bot_api, line_bot_blob_api):
        """
        初始化 LINE Bot 控制器
        :param line_bot_api: 用於傳送訊息的 LINE Messaging API
        :param line_bot_blob_api: 用於處理 Blob 資料的 API
        """
        self.line_bot_api = line_bot_api
        self.line_bot_blob_api = line_bot_blob_api
        self.language_model = LangChainModel() 
        import boto3
        self.dynamodb = boto3.resource('dynamodb')  

    def handle_message_event(self, event):
        """
        處理 LINE Bot 接收到的訊息事件
        :param event: 來自 LINE 平台的事件資料
        """
        user_id = event.source.user_id
        message = event.message.text

        if re.match(r'資訊|球館資訊|說明|圖卡|牌卡|介紹', message):
            self.reply_message(event.reply_token, [main_menu_view()])
        else:
            self.process_language_model(event, user_id, message)

    def process_language_model(self, event, user_id, message):
        """
        使用 LangChain AI 模型處理用戶訊息，並記錄聊天歷史
        :param event: LINE 訊息事件
        :param user_id: 使用者 ID
        :param message: 使用者傳送的訊息
        """
        history = ConversationHistory(user_id)
        user_history = history.load_user_history()
        response = self.language_model.get_response(message, user_history)
        self.reply_message(event.reply_token, [TextMessage(text=response)])
        history.append_message("human", message)
        history.append_message("ai", response)

    def handle_postback_event(self, event):
        """
        處理 LINE Bot 的 Postback 事件（當用戶點擊按鈕時觸發）
        :param event: LINE 平台發送的事件資料
        """
        data = event.postback.data
        handlers = {
            '主選單(input)':lambda:main_menu_view(),
            '團體課(input)':lambda:group_class_main_view(),
            '個人課(input)':lambda:one_on_one_class_main_view(),
            '租桌零打(input)':lambda:casual_play_main_view(),
            '球場位置(input)':lambda:get_location_message_view(),
            '場地介紹(input)':lambda:get_court_photos_view()
        }
        self.reply_message(event.reply_token, handlers[data]())
    
    def reply_message(self, reply_token, messages):
        """
        發送回應訊息到 LINE 平台
        :param reply_token: LINE API 提供的回應 Token
        :param messages: 要發送的訊息列表
        """
        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=messages
            )
        )
        

