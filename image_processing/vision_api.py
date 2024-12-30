import base64
import io
from linebot.models import TextSendMessage
from openai import OpenAI

from line_bot.line_client import LineClient
from config import OPENAI_API_KEY

from pydantic import BaseModel, Field
from typing import Optional

from data_management.redis_client import RedisClient

line_client = LineClient()
line_api=line_client.api
open_ai_client = OpenAI(api_key=OPENAI_API_KEY)
redis=RedisClient()
redis_client=redis.client


class FoodInformation(BaseModel):
    """
    このクラスは食品の商品情報を管理します。
    """

    is_food_package: str = Field(..., description='画像が食品パッケージであるか（"True" または "False"）')
    manufacturer: Optional[str] = Field(
        None, description="例：AJINOMOTO、star select 明星食品"
    )
    product_name: Optional[str] = Field(
        None, description="例：CookDo 熟成豆板醤"
    )

def image_processing_a_step_3(event):
        # 受信した画像を取得
        message_id = event.message.id  # 画像のメッセージIDを取得
        image_content = line_api.get_message_content(message_id)

        # メモリ上に画像を保存
        image_bytes = io.BytesIO()
        for chunk in image_content.iter_content():
            image_bytes.write(chunk)
        image_bytes.seek(0)  # 読み取り位置を先頭にリセット

        # 画像をエンコードする関数
        def encode_image(image_stream):
            return base64.b64encode(image_stream.read()).decode('utf-8')

        # base64文字列の取得
        base64_image = encode_image(image_bytes)

        # OpenAI APIにリクエスト
        completion = open_ai_client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "食品パッケージの画像をJSON形式に変換してください。もし食品パッケージ以外の画像である場合はis_food_packageをFalseにし、各項目をすべてNoneにしてください。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            response_format=FoodInformation,
        )

        def to_str(value):
            if value is None:
                return ""
            elif isinstance(value, bool):
                return "True" if value else "False"
            else:
                return str(value)

        message = completion.choices[0].message.parsed
        redis_client.hset(event.source.user_id, 'is_food_package', to_str(message.is_food_package))
        redis_client.hset(event.source.user_id, 'manufacturer', to_str(message.manufacturer))
        redis_client.hset(event.source.user_id, 'product_name', to_str(message.product_name))


class Seasonings(BaseModel):
    """
    このクラスは調味料の成分情報を管理します。
    - 重量はすべてグラム換算すること。1000ミリグラム→1グラム、1ミリリットル→1グラム。       
    """

    is_ingredient_list: str = Field(..., description='画像が成分表示であるか（"True" または "False"）')
    gram_per_unit: Optional[float] = Field(
        None, description="できる限り入力。各成分が何g当たりの量を示しているのかわかるように、グラム（g）換算で統一すること。便宜上1mlは1gとして計算してください。例: 1000mg → 1g"
    )
    measurement_unit: Optional[str] = Field(
        None, description="例：大さじ1杯15ml→大さじ1杯 / 1袋25gあたり→1袋 / ひとつまみ3gあたり→ひとつまみ / 1食（97g）当たり→1食　※入力データは「小さじ1杯」「1個」「1食」「大さじ1杯」「1缶」「1袋」「1人前」「2人前」「1皿」「1/2袋」「1本」「1パック」などを想定。※重さとml以外の〇〇当たりの記載がある場合のみ入力。"
    )
    calories: Optional[float] = Field(
        None, description="熱量（kcal）"
    )
    protein: Optional[float] = Field(
        None, description="たんぱく質量（g）。グラム（g）換算で統一すること。例: 1000mg → 1g"
    )
    fat: Optional[float] = Field(
        None, description="脂質量（g）。グラム（g）換算で統一すること。例: 1000mg → 1g"
    )
    carbohydrates: Optional[float] = Field(
        None, description="炭水化物量（g）。グラム（g）換算で統一すること。例: 1000mg → 1g"
    )
    sodium: Optional[float] = Field(
        None, description="ナトリウム量または食塩相当量（g）。グラム（g）換算で統一すること。例: 1000mg → 1g"
    )


def image_processing_a_step_4(event):
        # 受信した画像を取得
        message_id = event.message.id  # 画像のメッセージIDを取得
        image_content = line_api.get_message_content(message_id)

        # メモリ上に画像を保存
        image_bytes = io.BytesIO()
        for chunk in image_content.iter_content():
            image_bytes.write(chunk)
        image_bytes.seek(0)  # 読み取り位置を先頭にリセット

        # 画像をエンコードする関数
        def encode_image(image_stream):
            return base64.b64encode(image_stream.read()).decode('utf-8')

        # base64文字列の取得
        base64_image = encode_image(image_bytes)

        # OpenAI APIにリクエスト
        completion = open_ai_client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "成分表示の画像をJSON形式に変換してください。もし成分表示以外の画像である場合はis_ingredient_listをFalseにし、各項目をすべてNoneにしてください。measurement_unitは、gとml以外に「〇〇当たり」の記載がある場合のみ入力。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            response_format=Seasonings,
        )

        def to_str(value):
            if value is None:
                return ""
            elif isinstance(value, bool):
                return "True" if value else "False"
            else:
                return str(value)

        message = completion.choices[0].message.parsed
        redis_client.hset(event.source.user_id, 'is_ingredient_list', to_str(message.is_ingredient_list))
        redis_client.hset(event.source.user_id, 'gram_per_unit', to_str(message.gram_per_unit))
        redis_client.hset(event.source.user_id, 'measurement_unit', to_str(message.measurement_unit))
        redis_client.hset(event.source.user_id, 'calories', to_str(message.calories))
        redis_client.hset(event.source.user_id, 'protein', to_str(message.protein))
        redis_client.hset(event.source.user_id, 'fat', to_str(message.fat))
        redis_client.hset(event.source.user_id, 'carbohydrates', to_str(message.carbohydrates))
        redis_client.hset(event.source.user_id, 'sodium', to_str(message.sodium))
    

