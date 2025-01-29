import os
import sys
import awsgi

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'routes', 'line_bot_routes'))
from routes.line_bot_routes_sdk_v3 import app

def lambda_handler(event, context):
    """
    AWS Lambda 執行入口
    這個函數會接收 API Gateway 發送的 `event`，並將其傳遞給 Flask 應用處理。

    awsgi.response 會將 Flask 的回應轉換成 AWS Lambda 能理解的格式。
    """
    return awsgi.response(app, event, context)

