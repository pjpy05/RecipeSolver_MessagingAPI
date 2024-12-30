from linebot.models import TextMessage,TextSendMessage

from line_bot.line_client import LineClient,show_loading_animation
from line_bot.scenario_a.messages import (
    get_step_4_1_message,
    get_step_4_2_message,
    get_step_4_3_message,
    get_step_5_message,
    get_step_6_message,
    get_step_7_message,
    get_step_8_message,
    get_step_9_message,
    get_scenario_end_message
)
from data_management.redis_client import RedisClient

from config import GOOGLE_CREDENTIALS_JSON,USER_SPECIFIC_GOOGLE_SHEET_ID
from data_management.google_sheets_client import GoogleSheetsClient

from image_processing.vision_api import handle_vision_api_message

line_client = LineClient()
line_api=line_client.api
line_handler=line_client.handler
redis=RedisClient()
redis_client=redis.client
# scenario_a=ASteps(line_client)
seasonings_table=GoogleSheetsClient(GOOGLE_CREDENTIALS_JSON,USER_SPECIFIC_GOOGLE_SHEET_ID,"調味料")

# メッセージイベントの分岐設定
def go_to_next_step(event):

    # Redisから現在地を取得
    current_scenario=redis_client.hget(event.source.user_id,'current_scenario')
    
    # ユーザーからの応答
    if isinstance(event.message,TextMessage):
        request_text=event.message.text
    else:
        request_text=""

    # # ユーザーごとのGoogleシートに分けるバージョン
    # if request_text=="scenario_a":
    #     scenario_a.handle_step_1(event)
    #     spreadsheet_id=redis_client.hget(event.source.user_id,'spreadsheet_id')
    #     if spreadsheet_id is None:
    #         scenario_a.handle_step_2(event)
    #     else:
    #         scenario_a.handle_step_4_1(event)

    # elif current_scenario =="a_step_2":
    #     # if request_text=="はい":
    #     #     scenario_a.handle_step_3(event)
    #     # elif request_text=="いいえ":
    #     #     scenario_a.handle_scenario_end(event)
    #     if request_text=="いいえ":
    #         scenario_a.handle_scenario_end(event)

    # elif current_scenario =="a_step_3":
    #         scenario_a.handle_step_4_1_2(event)
        
    if request_text=="調味料の登録":
        show_loading_animation(event)
        # a_step_4_1
        redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
        line_api.reply_message(event.reply_token,get_step_4_1_message())

    # a_step_4_1
    elif current_scenario =="a_step_4_1":
        show_loading_animation(event)
        # a_step_4_2
        redis_client.hset(event.source.user_id,'current_scenario','a_step_4_2')
        handle_vision_api_message(event)
        is_ingredient_list=redis_client.hget(event.source.user_id,'is_ingredient_list').lower()=="true"
        if is_ingredient_list is True:
            line_api.reply_message(event.reply_token,get_step_4_2_message(event))
        else:
            # a_step_4_1
            redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
            line_api.reply_message(event.reply_token,get_step_4_1_message())

    # a_step_4_2
    elif current_scenario =="a_step_4_2":
        if request_text=="確定して進む":
            # a_step_5
            redis_client.hset(event.source.user_id,'current_scenario','a_step_5')
            line_api.reply_message(event.reply_token,get_step_5_message())
        elif request_text=="画像を送信し直す":
            # a_step_4_1
            redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
            line_api.reply_message(event.reply_token,get_step_4_1_message())
        else: 
            redis_client.hset(event.source.user_id,'temp', request_text)
            # a_step_4_3
            redis_client.hset(event.source.user_id,'current_scenario','a_step_4_3')
            line_api.reply_message(event.reply_token,get_step_4_3_message())

    # a_step_4_3
    elif current_scenario =="a_step_4_3":
        temp=redis_client.hget(event.source.user_id,'temp')
        if temp=="〇〇g当たりを修正":
            redis_client.hset(event.source.user_id,'gram_per_unit',request_text)
        elif temp=="〇〇当たり（任意）を修正":
            redis_client.hset(event.source.user_id,'measurement_unit',request_text)
        elif temp=="熱量を修正":
            redis_client.hset(event.source.user_id,'calories',request_text)
        elif temp=="たんぱく質を修正":
            redis_client.hset(event.source.user_id,'protein',request_text)
        elif temp=="脂質を修正":
            redis_client.hset(event.source.user_id,'fat',request_text)
        elif temp=="炭水化物を修正":
            redis_client.hset(event.source.user_id,'carbohydrates',request_text)
        elif temp=="食塩相当量を修正":
            redis_client.hset(event.source.user_id,'sodium',request_text)
        # a_step_4_2
        redis_client.hset(event.source.user_id,'current_scenario','a_step_4_2')
        line_api.reply_message(event.reply_token,get_step_4_2_message(event))

    # a_step_5
    elif current_scenario =="a_step_5":
        redis_client.hset(event.source.user_id,'category',request_text)
        # a_step_6
        redis_client.hset(event.source.user_id,'current_scenario','a_step_6')
        line_api.reply_message(event.reply_token,get_step_6_message())

    # a_step_6
    elif current_scenario =="a_step_6":
        redis_client.hset(event.source.user_id,'manufacturer',request_text)
        # a_step_7
        redis_client.hset(event.source.user_id,'current_scenario','a_step_7')
        line_api.reply_message(event.reply_token,get_step_7_message())

    # a_step_7
    elif current_scenario =="a_step_7":
        redis_client.hset(event.source.user_id,'product_name',request_text)
        # a_step_8
        redis_client.hset(event.source.user_id,'current_scenario','a_step_8')
        line_api.reply_message(event.reply_token,get_step_8_message(event))

    # a_step_8
    elif current_scenario =="a_step_8":
        # a_step_9
        if request_text=="Googleスプレッドシートに登録":
            show_loading_animation(event)
            redis_client.hset(event.source.user_id,'current_scenario','a_step_9')
            # category=redis_client.hget(event.source.user_id,'category')
            # manufacturer=redis_client.hget(event.source.user_id,'manufacturer')
            # product_name=redis_client.hget(event.source.user_id,'product_name')
            # gram_per_unit=redis_client.hget(event.source.user_id,'gram_per_unit')
            # measurement_unit=redis_client.hget(event.source.user_id,'measurement_unit')
            # calories=redis_client.hget(event.source.user_id,'calories')
            # protein=redis_client.hget(event.source.user_id,'protein')
            # fat=redis_client.hget(event.source.user_id,'fat')
            # carbohydrates=redis_client.hget(event.source.user_id,'carbohydrates')
            # sodium=redis_client.hget(event.source.user_id,'sodium')
            # new_data = [
            #     ["種類","メーカー","商品名","〇〇g当たり","〇〇当たり（任意）","熱量（kcal）","たんぱく質（g）","脂質（g）","炭水化物（g）","食塩相当量（g）"],
            #     [category,manufacturer,product_name,gram_per_unit,measurement_unit,calories,protein,fat,carbohydrates,sodium]
            # ]

            # Redisからデータ取得
            def get_redis_value(redis_client, user_id, key):
                value = redis_client.hget(user_id, key)
                return value.decode('utf-8') if isinstance(value, bytes) else value

            keys = ['category', 'manufacturer', 'product_name', 'gram_per_unit', 'measurement_unit', 'calories', 'protein', 'fat', 'carbohydrates', 'sodium']
            data = {key: (get_redis_value(redis_client, event.source.user_id, key) or "") for key in keys}

            new_data = [
                ["種類", "メーカー", "商品名", "〇〇g当たり", "〇〇当たり（任意）", "熱量（kcal）", "たんぱく質（g）", "脂質（g）", "炭水化物（g）", "食塩相当量（g）"],
                [
                    data['category'],
                    data['manufacturer'],
                    data['product_name'],
                    data['gram_per_unit'],
                    data['measurement_unit'],
                    data['calories'],
                    data['protein'],
                    data['fat'],
                    data['carbohydrates'],
                    data['sodium']
                ]
            ]

            # Google Sheetsへデータ挿入
            try:
                seasonings_table.insert_seasonings_data(sheet_id=USER_SPECIFIC_GOOGLE_SHEET_ID, sheet_name="調味料", data=new_data)
                line_api.reply_message(event.reply_token, get_step_9_message())
            except Exception as e:
                error_message = f"データ送信時にエラーが発生しました: {str(e)}"
                line_api.reply_message(event.reply_token, TextSendMessage(text=error_message))
    
        elif request_text=="商品情報を修正する":
            # a_step_5
            redis_client.hset(event.source.user_id,'current_scenario','a_step_5')
            line_api.reply_message(event.reply_token,get_step_5_message())
        elif request_text=="画像を送信し直す":
            # a_step_4_1
            redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
            line_api.reply_message(event.reply_token,get_step_4_1_message())

    # a_step_9
    elif current_scenario =="a_step_9":
        show_loading_animation(event)
        if request_text=="続けて登録":
            # a_step_4_1
            redis_client.hset(event.source.user_id,'current_scenario','a_step_4_1')
            line_api.reply_message(event.reply_token,get_step_4_1_message())
        elif request_text=="終わる":
            # シナリオ終了
            redis_client.delete(event.source.user_id)
            line_api.reply_message(event.reply_token,get_scenario_end_message())


