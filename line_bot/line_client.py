from config import LINE_CHANNEL_ACCESS_TOKEN,LINE_CHANNEL_SECRET
from linebot import LineBotApi, WebhookHandler

import requests
import json

class LineClient:
    def __init__(self, access_token: str = None, channel_secret: str = None):
        """
        LINEクライアントの初期化
        :param access_token: チャネルアクセストークン
        :param channel_secret: チャネルシークレット
        """
        self.access_token = LINE_CHANNEL_ACCESS_TOKEN
        self.channel_secret = LINE_CHANNEL_SECRET

        if not self.access_token or not self.channel_secret:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN または LINE_CHANNEL_SECRET が設定されていません。")

        self.api = LineBotApi(self.access_token)
        self.handler = WebhookHandler(self.channel_secret)

def show_loading_animation(event):

    # URL
    url = 'https://api.line.me/v2/bot/chat/loading/start'

    # ヘッダー
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }

    # データ
    data = {
        "chatId": event.source.user_id,  # 実際のチャットIDに置き換えてください
        "loadingSeconds": 60
    }

    # POSTリクエストを送信
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 結果の確認
    if response.status_code == 200:
        print("リクエストが成功しました。")
    else:
        print(f"エラーが発生しました: {response.status_code} - {response.text}")



