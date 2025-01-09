from flask import Flask, request, send_from_directory,abort,jsonify
from linebot.models import MessageEvent
from linebot.exceptions import InvalidSignatureError
import os

from line_bot.line_client import LineClient
from line_bot.scenario_a.steps import go_to_next_step
from liff import liff
from config import LIFF_ID

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
        # LINE Handlerでリクエストを処理
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        # 無効な署名エラーを記録し、HTTP 400を返す
        app.logger.error("Invalid signature. Please check your channel secret and signature.")
        abort(400)
    except Exception as e:
        # 重要なエラーをキャッチしログに記録する
        app.logger.error(f"Unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500  # エラー詳細をJSONで返す
    return "OK", 200  # 正常応答

@line_handler.add(MessageEvent)
def handle_message(event):
    try:
        # メッセージイベント処理
        go_to_next_step(event)
    except Exception as e:
        # メッセージ処理内のエラーをキャッチして記録
        app.logger.error(f"Error in message handling: {e}")
        # 処理続行のため、エラーを通知せずログのみに記録

@app.route('/get/<user_id>', methods=['GET'])
def get_redis_json(user_id):
    redis_json = liff(user_id)
    return redis_json

# # LIFFアプリ用データのAPIエンドポイント
# @app.route('/liff-data', methods=['POST'])
# def handle_liff_data():
#     data = request.json
#     user_id = data.get('userId')

#     if not user_id:
#         app.logger.error("userId is missing in the request.")
#         return jsonify({"error": "userId is required"}), 400

#     # 必要なデータを取得（例として 'current_scenario' など）
#     try:
#         user_data = redis_client.hgetall(user_id)
#         if not user_data:
#             app.logger.warning(f"No data found for user_id: {user_id}")
#             return jsonify({"error": "User data not found"}), 404

#         return jsonify(user_data), 200
#     except Exception as e:
#         app.logger.error(f"Error fetching data from Redis: {e}")
#         return jsonify({"error": "Internal server error"}), 500

# # LIFF IDを提供するエンドポイント
# @app.route('/api/liff-id', methods=['GET'])
# def get_liff_id():
#     return jsonify({"liffId": LIFF_ID})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
