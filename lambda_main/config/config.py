import os
import boto3
import json
from botocore.exceptions import ClientError


session = boto3.session.Session()

def get_secret_client(region_name):
    """
    建立 AWS Secrets Manager 客戶端，用於存取機密資訊
    :param region_name: AWS 區域
    :return: Secrets Manager 客戶端
    """
    return session.client(service_name='secretsmanager', region_name=region_name)

class Config:
    """
    Config 類別 - 管理 AWS Lambda 環境變數與 Secrets Manager 機密
    """
    SECRETS = {
        'GOOGLE_SHEET': "dev/LineBot/GoogleSheet",
        'LINE_BOT_CONFIG': "dev/LineBot/Config"
    }

    def __init__(self, lambda_role):
        """
        初始化 Config 類別，根據 lambda_role 加載不同的設定
        :param lambda_role: 角色類型 (lambda_update / lambda_main)
        """
        self.AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')
        if lambda_role == 'lambda_update':
            self.load_lambda_update_config()
        elif lambda_role == 'lambda_main':
            self.load_lambda_main_config()
        else:
            raise ValueError(f"Invalid lambda_role: {lambda_role}")
        
    def get_secret(self, secret_name):
        """
        從 AWS Secrets Manager 獲取機密資訊
        :param secret_name: 機密名稱
        :return: 字串或字典格式的機密
        """
        try:
            client = get_secret_client(self.AWS_REGION)
            response = client.get_secret_value(SecretId=secret_name)
            secret = response['SecretString']
            print(secret)
            try:
                return json.loads(secret)
            except json.JSONDecodeError:
                return secret

        except ClientError as e:
            print(f"ClientError while retrieving secret {secret_name}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error retrieving secret {secret_name}: {e}")
            raise

    def load_config_value(self, key, secret_name):
        """
        讀取 Secrets Manager 內的特定值
        :param key: 機密中的 Key
        :param secret_name: 機密名稱
        :return: 讀取到的值
        """
        try:
            secret_data = self.get_secret(secret_name)
            if isinstance(secret_data, dict):
                return secret_data.get(key) 
            else:
                raise ValueError(f"The secret {secret_name} is not a JSON object.")
        except Exception as e:
            print(f"Error loading {key}: {e}")
            raise

    def load_lambda_update_config(self):
        """
        加載 `lambda_update` 環境變數（與 Google Sheets 整合）
        """
        self.GOOGLE_SERVICE_ACCOUNT_KEY = self.load_config_value(key='GoogleSheetToken', secret_name=self.SECRETS['GOOGLE_SHEET'])
        self.GOOGLE_SHEET_ID = self.load_config_value(key="GOOGLE_SHEET_ID", secret_name=self.SECRETS['GOOGLE_SHEET'])
        self.GOOGLE_SHEET_NAME = self.load_config_value(key="GOOGLE_SHEET_NAME", secret_name=self.SECRETS['GOOGLE_SHEET'])

    def load_lambda_main_config(self):
        """
        加載 `lambda_main` 環境變數（與 LINE Bot 整合）
        """
        self.OPENAI_API_KEY = self.load_config_value(key="OPENAI_API_KEY", secret_name=self.SECRETS['LINE_BOT_CONFIG'])
        self.CHANNEL_SECRET = self.load_config_value(key="CHANNEL_SECRET", secret_name=self.SECRETS['LINE_BOT_CONFIG'])
        self.CHANNEL_ACCESS_TOKEN = self.load_config_value(key="CHANNEL_ACCESS_TOKEN", secret_name=self.SECRETS['LINE_BOT_CONFIG'])
        self.USER_ID = self.load_config_value(key="USER_ID", secret_name=self.SECRETS['LINE_BOT_CONFIG'])
        self.BUCKET_NAME = self.load_config_value(key="BUCKET_NAME", secret_name=self.SECRETS['LINE_BOT_CONFIG'])


