from flask import Flask, request, send_from_directory,abort,jsonify
from linebot.models import MessageEvent
from linebot.exceptions import InvalidSignatureError
import os

from line_bot.line_client import LineClient
from line_bot.scenario_a.steps import go_to_next_step
from liff.liff_module import get_context,set_context

from flask_cors import CORS

# 設定
app = Flask(__name__)
line_client = LineClient()
line_api=line_client.api
line_handler=line_client.handler

CORS(app)  # 全てのエンドポイントでCORSを許可
# フロントエンドからバックエンドにリクエストを送る際、CORS設定が不足しているとエラーが発生します。

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

# LIFFアプリにRedisデータをJSONで渡すAPIエンドポイント
@app.route('/get/<user_id>', methods=['GET'])
def get_redis_json(user_id):
    redis_json = get_context(user_id)
    return redis_json

# LIFFアプリから受け取ったJSONデータをRedisに渡すAPIエンドポイント
@app.route('/post/<user_id>', methods=['POST'])
def set_json_redis(user_id):
    try:
        # JSON データをリクエストから取得
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400

        # 必要な処理を実行 (例: Redis に保存)
        # redis_client.set(user_id, json.dumps(json_data))

        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)