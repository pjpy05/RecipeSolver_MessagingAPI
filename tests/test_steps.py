from linebot.models import TextMessage,TextSendMessage

from line_bot.line_client import LineClient,show_loading_animation
from line_bot.scenario_a.messages import (
    get_step_2_message,
    get_step_3_1_message,
    get_step_3_2_message,
    get_step_3_3_message,
    get_step_4_1_message,
    get_step_4_2_message,
    get_step_4_3_message,
    get_step_8_message,
    get_step_9_message,
    get_scenario_end_message
)
from data_management.redis_client import RedisClient

from config import GOOGLE_CREDENTIALS_JSON,USER_SPECIFIC_GOOGLE_SHEET_ID
from data_management.google_sheets_client import GoogleSheetsClient

from image_processing.vision_api import image_processing_a_step_3,image_processing_a_step_4

line_client = LineClient()
line_api=line_client.api
line_handler=line_client.handler
redis=RedisClient()
redis_client=redis.client
# scenario_a=ASteps(line_client)
seasonings_table=GoogleSheetsClient(GOOGLE_CREDENTIALS_JSON,USER_SPECIFIC_GOOGLE_SHEET_ID,"調味料")

# メッセージイベントの分岐設定
def test_steps(event):
    user_id=event.source.user_id
    reply_token=event.reply_token

    # # Redisから現在地を取得
    # current_scenario=redis_client.hget(event.source.user_id,'current_scenario')
    
    # ユーザーからの応答
    # if isinstance(event.message,TextMessage):
    #     request_text=event.message.text
    # else:
    #     request_text=""
    # redis_client.hset(user_id,'current_scenario','a_step_2')
    # line_api.reply_message(event.reply_token,get_step_2_message())
    
    redis_json=redis.get_hash_as_json(user_id)
    line_api.reply_message(reply_token,TextSendMessage(text=redis_json))

    # # a_step_2
    # elif current_scenario =="a_step_2":
    #     redis_client.hset(event.source.user_id,'category',request_text)
    #     # a_step_3_1
    #     redis_client.hset(event.source.user_id,'current_scenario','a_step_3_1')
    #     line_api.reply_message(event.reply_token,get_step_3_1_message())

    # # a_step_3_1
    # elif current_scenario =="a_step_3_1":
    #     show_loading_animation(event)
    #     # a_step_3_2
    #     redis_client.hset(event.source.user_id,'current_scenario','a_step_3_2')
    #     image_processing_a_step_3(event)
    #     is_food_package=redis_client.hget(event.source.user_id,'is_food_package').lower()=="true"
    #     if is_food_package is True:
    #         line_api.reply_message(event.reply_token,get_step_3_2_message(event))
    #     else:
    #         # a_step_3_1
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_3_1')
    #         line_api.reply_message(event.reply_token,get_step_3_1_message())

    # # a_step_3_2
    # elif current_scenario =="a_step_3_2":
    #     if request_text=="OK":
    #         # a_step_4_1
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
    #         line_api.reply_message(event.reply_token,get_step_4_1_message())
    #     elif request_text=="画像を送信し直す":
    #         # a_step_3_1
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_3_1')
    #         line_api.reply_message(event.reply_token,get_step_3_1_message())
    #     else: 
    #         redis_client.hset(event.source.user_id,'temp', request_text)
    #         # a_step_3_3
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_3_3')
    #         line_api.reply_message(event.reply_token,get_step_3_3_message())

    # # a_step_3_3
    # elif current_scenario =="a_step_3_3":
    #     temp=redis_client.hget(event.source.user_id,'temp')
    #     if temp=="メーカーを修正":
    #         redis_client.hset(event.source.user_id,'manufacturer',request_text)
    #     elif temp=="商品名を修正":
    #         redis_client.hset(event.source.user_id,'product_name',request_text)
    #     # a_step_3_2
    #     redis_client.hset(event.source.user_id,'current_scenario','a_step_3_2')
    #     line_api.reply_message(event.reply_token,get_step_3_2_message(event))

    # # a_step_4_1
    # elif current_scenario =="a_step_4_1":
    #     show_loading_animation(event)
    #     # a_step_4_2
    #     redis_client.hset(event.source.user_id,'current_scenario','a_step_4_2')
    #     image_processing_a_step_4(event)
    #     is_ingredient_list=redis_client.hget(event.source.user_id,'is_ingredient_list').lower()=="true"
    #     if is_ingredient_list is True:
    #         line_api.reply_message(event.reply_token,get_step_4_2_message(event))
    #     else:
    #         # a_step_4_1
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
    #         line_api.reply_message(event.reply_token,get_step_4_1_message())

    # # a_step_4_2
    # elif current_scenario =="a_step_4_2":
    #     if request_text=="OK":
    #         # a_step_8
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_8')
    #         line_api.reply_message(event.reply_token,get_step_8_message(event))
    #     elif request_text=="画像を送信し直す":
    #         # a_step_4_1
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
    #         line_api.reply_message(event.reply_token,get_step_4_1_message())
    #     else: 
    #         redis_client.hset(event.source.user_id,'temp', request_text)
    #         # a_step_4_3
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_4_3')
    #         line_api.reply_message(event.reply_token,get_step_4_3_message())

    # # a_step_4_3
    # elif current_scenario =="a_step_4_3":
    #     temp=redis_client.hget(event.source.user_id,'temp')
    #     if temp=="〇〇g当たりを修正":
    #         redis_client.hset(event.source.user_id,'gram_per_unit',request_text)
    #     elif temp=="g以外の単位を修正":
    #         redis_client.hset(event.source.user_id,'measurement_unit',request_text)
    #     elif temp=="熱量を修正":
    #         redis_client.hset(event.source.user_id,'calories',request_text)
    #     elif temp=="たんぱく質を修正":
    #         redis_client.hset(event.source.user_id,'protein',request_text)
    #     elif temp=="脂質を修正":
    #         redis_client.hset(event.source.user_id,'fat',request_text)
    #     elif temp=="炭水化物を修正":
    #         redis_client.hset(event.source.user_id,'carbohydrates',request_text)
    #     elif temp=="食塩相当量を修正":
    #         redis_client.hset(event.source.user_id,'sodium',request_text)
    #     # a_step_4_2
    #     redis_client.hset(event.source.user_id,'current_scenario','a_step_4_2')
    #     line_api.reply_message(event.reply_token,get_step_4_2_message(event))

    # # a_step_8
    # elif current_scenario =="a_step_8":
    #     show_loading_animation(event)
    #     # a_step_9
    #     if request_text=="Googleスプレッドシートに登録":
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_9')

    #         # Redisからデータ取得
    #         def get_redis_value(redis_client, user_id, key):
    #             value = redis_client.hget(user_id, key)
    #             return value.decode('utf-8') if isinstance(value, bytes) else value

    #         keys = ['category', 'manufacturer', 'product_name', 'gram_per_unit', 'measurement_unit', 'calories', 'protein', 'fat', 'carbohydrates', 'sodium']
    #         data = {key: (get_redis_value(redis_client, event.source.user_id, key) or "") for key in keys}

    #         new_data = [
    #             ["種類", "メーカー", "商品名", "〇〇g当たり", "g以外の単位", "熱量（kcal）", "たんぱく質（g）", "脂質（g）", "炭水化物（g）", "食塩相当量（g）"],
    #             [
    #                 data['category'],
    #                 data['manufacturer'],
    #                 data['product_name'],
    #                 data['gram_per_unit'],
    #                 data['measurement_unit'],
    #                 data['calories'],
    #                 data['protein'],
    #                 data['fat'],
    #                 data['carbohydrates'],
    #                 data['sodium']
    #             ]
    #         ]

    #         # Google Sheetsへデータ挿入
    #         seasonings_table.insert_seasonings_data(sheet_id=USER_SPECIFIC_GOOGLE_SHEET_ID, sheet_name="調味料", data=new_data)
    #         line_api.reply_message(event.reply_token, get_step_9_message())
    
    #     elif request_text=="やり直す":
    #         # a_step_2
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_2')
    #         line_api.reply_message(event.reply_token,get_step_2_message())

    # # a_step_9
    # elif current_scenario =="a_step_9":
    #     show_loading_animation(event)
    #     if request_text=="続けて登録":
    #         # a_step_2
    #         redis_client.hset(event.source.user_id,'current_scenario','a_step_2')
    #         line_api.reply_message(event.reply_token,get_step_2_message())
    #     elif request_text=="終わる":
    #         # シナリオ終了
    #         line_api.reply_message(event.reply_token,get_scenario_end_message())
    #         redis_client.delete(event.source.user_id)


