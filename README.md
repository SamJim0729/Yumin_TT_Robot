裕民桌球場 LINE Bot 系統
介紹
裕民桌球場 LINE Bot 系統是一個基於 AWS Lambda 和 LINE Messaging API 的互動式機器人，提供使用者關於桌球場的課程資訊、營業資訊、租桌服務等相關功能。系統具備高度模組化設計，支援動態更新，並使用 Google Sheets 作為配置管理工具，結合 AWS 基礎設施以實現穩定且高效的運行環境。

-----------------------------------------------------------------------------------

專案架構
系統功能
LINE Bot 功能
提供課程資訊（團體課程、個人課程）。
顯示租桌服務費用及規則。
提供球館營業時間與地點資訊。
支援多媒體回覆（圖片、地理位置）。
動態更新
透過 Google Sheets 管理配置，並自動更新至 Lambda。
模組化設計
使用 AWS Lambda 和 API Gateway 實現無伺服器化架構，具備高可擴展性。

-----------------------------------------------------------------------------------

專案目錄結構
project/
│
├── lambda_main/
│   ├── app.py                      # Lambda 主入口（LINE Webhook 接收器）
│   ├── routes/                     # 路由模組
│   │   └── line_bot_routes_sdk_v3.py
│   ├── controllers/                # 控制器模組
│   │   └── line_bot_controller_sdk_v3.py
│   ├── models/                     # 業務邏輯與模型模組
│   │   ├── llm_model.py            # LangChain 與 OpenAI 模型
│   │   ├── conversation_history.py # 聊天歷史管理（DynamoDB 整合）
│   │   └── function_handler.py     # 球館資訊函數
│   ├── views/                      # 視圖模板（LINE 回應模板）
│   │   └── message_templates_sdk_v3.py
│   └── config/
│       └── config.py               # 配置管理（Secrets Manager 整合）
│
├── lambda_update/
│   ├── app.py                      # Lambda 更新入口（Google Sheets 同步）
│   ├── utils/                      # 工具模組
│   │   └── update_function_handler.py
│   └── config/
│       └── config.py               # 配置管理
│
└── requirements.txt                # Python 依賴清單

-----------------------------------------------------------------------------------

技術棧
後端技術
AWS Lambda：作為無伺服器運行環境。
Amazon API Gateway：連接 LINE Webhook 請求與 Lambda。
DynamoDB：儲存聊天記錄。
Secrets Manager：安全管理 LINE Bot 金鑰與 Google Sheets API 憑證。
Amazon S3：儲存靜態圖片資源，生成預簽名 URL。
外部服務
LINE Messaging API：與使用者互動。
Google Sheets：管理球館資訊與配置。
OpenAI (LangChain)：處理語言模型對話回應。

-----------------------------------------------------------------------------------

環境變數
以下環境變數需在 Lambda 中設定，提供動態配置支持：

變數名稱	說明	範例值
AWS_REGION	AWS 部署的區域	ap-northeast-1
BUCKET_NAME	S3 Bucket 名稱	yumin-tt-robot-photos
DYNAMODB_TABLE	聊天記錄的 DynamoDB 表名稱	Yumin_ChatSession
MESSAGE_TTL	聊天記錄的有效期限（秒）	180
GOOGLE_SHEET_ID	Google Sheets 的 ID	your-google-sheet-id
GOOGLE_SHEET_NAME	Google Sheets 工作表名稱	Sheet1
CHANNEL_SECRET	LINE Bot 的 Channel Secret	your-channel-secret
CHANNEL_ACCESS_TOKEN	LINE Bot 的 Access Token	your-access-token
OPENAI_API_KEY	OpenAI API 金鑰	your-openai-api-key

-----------------------------------------------------------------------------------

部署指南
1. 本地開發環境設置
安裝 Python 依賴：
pip install -r requirements.txt
本地測試：
模擬 AWS Lambda：
python lambda_main/app.py

2. 部署至 AWS Lambda
壓縮專案
將專案目錄打包為 .zip 文件，並確保包含所有依賴模組。
zip -r lambda_main.zip lambda_main/
上傳 Lambda

登入 AWS Console，將壓縮檔案上傳至對應的 Lambda 函數。
設置環境變數

按上述環境變數配置 Lambda。
3. CI/CD 自動化部署
使用 GitHub Actions 或 AWS CodePipeline 設置自動部署：
觸發條件：代碼推送至 main 分支。
步驟：
自動生成 .zip 文件。
使用 AWS CLI 部署至 Lambda。
測試 API。

-----------------------------------------------------------------------------------

測試指南
1. 測試 LINE Bot Webhook
使用 Postman 或直接向 LINE Bot 傳送訊息。
測試範例：
傳送「營業時間」，檢查回應是否正確。
點擊主選單按鈕，檢查是否收到對應回應。
2. 測試 Lambda 更新邏輯
手動修改 Google Sheets，觸發 lambda_update 更新配置。
檢查 function_handler.py 是否正確更新。






