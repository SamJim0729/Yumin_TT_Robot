import boto3
import time
import os
from botocore.exceptions import ClientError

dynamodb_resource = boto3.resource('dynamodb')

class ConversationHistory:
    """
    ConversationHistory - 管理用戶聊天歷史，儲存與讀取對話記錄
    使用 AWS DynamoDB 作為儲存後端，確保聊天歷史可持續存取
    """
    def __init__(self, user_id):
        """
        初始化聊天記錄管理類別
        :param user_id: LINE 用戶 ID
        """
        self.user_id = user_id
        self.table_name = os.getenv('DYNAMODB_TABLE', 'Yumin_ChatSession')
        self.table = dynamodb_resource.Table(self.table_name)
        

    def load_user_history(self):
        """
        從 DynamoDB 查詢該用戶的聊天歷史
        :return: 以列表回傳聊天歷史 [(role, message), ...]
        """
        try:
            response = self.table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(self.user_id),
                ScanIndexForward=True
            ) 

            messages = [(item['role'], item['message']) for item in response.get('Items', [])]
            return messages

        except ClientError as e:
            print(f"Error loading history for user {self.user_id}: {e}")
            return []

    def append_message(self, role, message):
        """
        儲存新的聊天記錄到 DynamoDB
        :param role: 訊息角色 ('human' 表示使用者, 'ai' 表示 AI)
        :param message: 訊息內容
        """
        try:
            tag = 1 if role == 'human' else 2
            timestamp = str(int(time.time())) + "-" + str(tag)
            expiration_time = int(time.time()) + int(os.getenv('MESSAGE_TTL', 180))
            self.table.put_item(
                Item={
                    'user_id': self.user_id,
                    'timestamp': timestamp,
                    'role': role,
                    'message': message,
                    'expirationTime': expiration_time
                }
            )
        except ClientError as e:
            print(f"Error appending message for user {self.user_id}: {e}")


