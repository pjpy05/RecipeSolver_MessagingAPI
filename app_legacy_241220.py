from flask import Flask, request, abort, jsonify
import logging
from linebot.models import MessageEvent,TextSendMessage,ImageMessage,TextMessage
from linebot.exceptions import InvalidSignatureError
import os

from line_bot.line_client import LineClient
from line_bot.scenario_a.steps import go_to_next_step

# # Googleの認証設定用（シートの共有で必要）
# from flask import redirect, url_for, session, request
# from google_auth_oauthlib.flow import Flow
# from requests_oauthlib import OAuth2Session
# import os
# import json
# from config import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET

# 設定
app = Flask(__name__)
line_client = LineClient()
line_api=line_client.api
line_handler=line_client.handler


# Webhookエンドポイントを設定
@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel secret and signature.")
        abort(400)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")  # その他のエラーをキャッチしてログに出力
        abort(500)
    return "OK"


@line_handler.add(MessageEvent)
def handle_message(event):
    go_to_next_step(event)

# @line_handler.add(MessageEvent,message=TextMessage)
# def handle_message(event):
#     go_to_next_step(event)

# @line_handler.add(MessageEvent,message=ImageMessage)
# def handle_message(event):
#     go_to_next_step(event)

# # Google OAuth設定
# GOOGLE_CLIENT_SECRETS = {
#     "web": {
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "redirect_uris": ["https://test241201.onrender.com/callback"],
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token"
#     }
# }
# SCOPES = ['openid', 'email', 'profile']
# flow = Flow.from_client_config(GOOGLE_CLIENT_SECRETS, scopes=SCOPES)
# flow.redirect_uri = 'https://test241201.onrender.com/callback'


# @app.route('/')
# def home():
#     """ホームページ"""
#     return 'Welcome! <a href="/google_login">Login with Google</a>'


# @app.route('/google_login')
# def google_login():
#     """Google認証開始"""
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true'
#     )
#     session['state'] = state
#     return redirect(authorization_url)


# @app.route('/callback')
# def callback():
#     """Google認証後のコールバック"""
#     # アクセストークン取得
#     flow.fetch_token(authorization_response=request.url)
#     credentials = flow.credentials

#     # アクセストークンでユーザー情報を取得
#     userinfo_endpoint = "https://www.googleapis.com/auth/userinfo.email"
#     token = credentials.token
#     user_info = fetch_user_info(userinfo_endpoint, token)

#     # ユーザー情報を表示
#     return f"User Info: {json.dumps(user_info, indent=2)}"


# def fetch_user_info(endpoint: str, access_token: str) -> dict:
#     """
#     Google APIを使ってユーザー情報を取得する。

#     :param endpoint: APIエンドポイントURL
#     :param access_token: アクセストークン
#     :return: ユーザー情報の辞書
#     """
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
#     response = OAuth2Session(token={"access_token": access_token}).get(endpoint, headers=headers)

#     # APIレスポンスを検証
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"Failed to fetch user info: {response.status_code}, {response.text}")


# ログ設定
logging.basicConfig(level=logging.INFO)  # 必要に応じてDEBUGに変更
logger = logging.getLogger(__name__)

# Renderの環境ログに出力
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Exception occurred: {e}", exc_info=True)  # 詳細なスタックトレースを含める
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
