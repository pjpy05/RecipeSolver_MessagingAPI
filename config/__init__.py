import os
# import json
from dotenv import load_dotenv
# from google.oauth2 import service_account

# .envファイルの読み込み
load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LIFF_ID = os.getenv("LIFF_ID")
NEXT_PUBLIC_LIFF_ID=os.getenv("NEXT_PUBLIC_LIFF_ID")
NEXT_PUBLIC_LINE_CHANNEL_ACCESS_TOKEN=os.getenv("NEXT_PUBLIC_LINE_CHANNEL_ACCESS_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_SPECIFIC_GOOGLE_SHEET_ID = os.getenv("USER_SPECIFIC_GOOGLE_SHEET_ID")
DEVELOPERS_GOOGLE_SHEET_ID = os.getenv("DEVELOPERS_GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# # Google Sheets APIの認証情報をロード
# def get_google_credentials():
#     GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")  # Render用の環境変数
#     if GOOGLE_CREDENTIALS_JSON:
#         credentials_info = json.loads(GOOGLE_CREDENTIALS_JSON)
#         return service_account.Credentials.from_service_account_info(credentials_info)
#     else:
#         raise ValueError("Google credentials JSON is not set in the environment variables")
    
REDIS_URL = os.getenv("REDIS_URL")