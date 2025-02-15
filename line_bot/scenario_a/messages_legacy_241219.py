from linebot.models import PostbackAction,ButtonsTemplate,TemplateSendMessage,TextSendMessage,QuickReply,MessageAction,QuickReplyButton,URIAction

from data_management.redis_client import RedisClient
redis=RedisClient()
redis_client=redis.client

# def get_step_2_message():
#     step_2_message=TemplateSendMessage(
#         alt_text='Buttons template',
#         template=ButtonsTemplate(
#             text='Googleスプレッドシートと連携しますか？',
#             actions=[
#                 URIAction(
#                     label='はい',
#                     uri='https://test241201.onrender.com/google_login'
#                 ),
#                 PostbackAction(
#                     label='いいえ',
#                     display_text='いいえ',
#                     data='action=buy&itemid=1'
#                 )
#             ]
#         )
#     )
#     return step_2_message

# def get_step_3_message():
#     reply_message=TextSendMessage(
#             text='あなたのGoogleスプレッドシートと連携しました'
#     )
#     return reply_message

def get_step_4_1_message():
    reply_message=TextSendMessage(
            text='成分表示の画像を送信してください\n-----\n※正確に認識できない場合は、画像をトリミングして再度お試しください'
    )
    return reply_message

# def get_demo_step_4_1_2_message():
#     text="成分表示の画像を送信してください\n※現在、未設定のためボタンで遷移分け"
#     items=["成分表示の画像送信","それ以外の画像送信"]
#     quick_reply_buttons=[]

#     for item in items:
#         quick_reply_buttons.append(QuickReplyButton(action=MessageAction(label=item,text=item)))

#     quick_reply=QuickReply(items=quick_reply_buttons)
#     reply_message=TextSendMessage(text=text,quick_reply=quick_reply)
#     return reply_message


def get_step_4_2_message(event):
    gram_per_unit=redis_client.hget(event.source.user_id,'gram_per_unit')
    measurement_unit=redis_client.hget(event.source.user_id,'measurement_unit')
    calories=redis_client.hget(event.source.user_id,'calories')
    protein=redis_client.hget(event.source.user_id,'protein')
    fat=redis_client.hget(event.source.user_id,'fat')
    carbohydrates=redis_client.hget(event.source.user_id,'carbohydrates')
    sodium=redis_client.hget(event.source.user_id,'sodium')

    text=f"登録内容をチェックしてください\n-----\n〇〇g当たり: {gram_per_unit}\n〇〇当たり（任意）: {measurement_unit}\n熱量（kcal）: {calories}\nたんぱく質（g）: {protein}\n脂質（g）: {fat}\n炭水化物（g）: {carbohydrates}\n食塩相当量（g）: {sodium}\n-----\n※「〇〇当たり（任意）」の例：小さじ1杯、1個、1食 など"

    items=["確定して進む","画像を送信し直す","〇〇g当たりを修正","〇〇当たり（任意）を修正","熱量を修正","たんぱく質を修正","脂質を修正","炭水化物を修正","食塩相当量を修正"]
    quick_reply_buttons=[]

    for item in items:
        quick_reply_buttons.append(QuickReplyButton(action=MessageAction(label=item,text=item)))

    quick_reply=QuickReply(items=quick_reply_buttons)
    reply_message=TextSendMessage(text=text,quick_reply=quick_reply)
    return reply_message


def get_step_4_3_message():
    reply_message=TextSendMessage(
            text='修正内容を入力してください'
    )
    return reply_message


def get_step_5_message():
    text="種類を教えてください"
    items=["インスタント麺","缶づめ","しょうゆ","ソース","鍋の素","ふりかけ","粉末・固形だし","ぽん酢","みそ","めんつゆ","その他"]
    quick_reply_buttons=[]

    for item in items:
        quick_reply_buttons.append(QuickReplyButton(action=MessageAction(label=item,text=item)))

    quick_reply=QuickReply(items=quick_reply_buttons)
    reply_message=TextSendMessage(text=text,quick_reply=quick_reply)
    return reply_message


def get_step_6_message():
    reply_message=TextSendMessage(
            text='メーカーを教えてください。\n-----\n例：AJINOMOTO、star select 明星食品'
    )
    return reply_message


def get_step_7_message():
    reply_message=TextSendMessage(
            text='商品名を教えてください。\n-----\n例：CookDo 熟成豆板醤'
    )
    return reply_message


def get_step_8_message(event):
    category=redis_client.hget(event.source.user_id,'category')
    manufacturer=redis_client.hget(event.source.user_id,'manufacturer')
    product_name=redis_client.hget(event.source.user_id,'product_name')
    gram_per_unit=redis_client.hget(event.source.user_id,'gram_per_unit')
    measurement_unit=redis_client.hget(event.source.user_id,'measurement_unit')
    calories=redis_client.hget(event.source.user_id,'calories')
    protein=redis_client.hget(event.source.user_id,'protein')
    fat=redis_client.hget(event.source.user_id,'fat')
    carbohydrates=redis_client.hget(event.source.user_id,'carbohydrates')
    sodium=redis_client.hget(event.source.user_id,'sodium')

    text=f"下記の内容でよろしいですか？\n----------\n種類：{category}\nメーカー：{manufacturer}\n商品名：{product_name}\n----------\n〇〇g当たり：{gram_per_unit}\n〇〇当たり（任意）：{measurement_unit}\n熱量（kcal）：{calories}\nたんぱく質（g）：{protein}\n脂質（g）：{fat}\n炭水化物（g）：{carbohydrates}\n食塩相当量（g）：{sodium}\n----------\n※重量はグラムで統一\n※「任意の単位」以外は数字で入力\n例：300kcal→300　500mg→0.5\n※「〇〇当たり（任意）」の例：小さじ1杯、1個、1食 など"

    items=["Googleスプレッドシートに登録","商品情報を修正する","画像を送信し直す"]
    quick_reply_buttons=[]

    for item in items:
        quick_reply_buttons.append(QuickReplyButton(action=MessageAction(label=item,text=item)))

    quick_reply=QuickReply(items=quick_reply_buttons)
    reply_message=TextSendMessage(text=text,quick_reply=quick_reply)
    return reply_message

# def get_step_2_message():
#     step_2_message=TemplateSendMessage(
#         alt_text='Buttons template',
#         template=ButtonsTemplate(
#             text='Googleスプレッドシートと連携しますか？',
#             actions=[
#                 URIAction(
#                     label='はい',
#                     uri='https://test241201.onrender.com/google_login'
#                 ),
#                 PostbackAction(
#                     label='いいえ',
#                     display_text='いいえ',
#                     data='action=buy&itemid=1'
#                 )
#             ]
#         )
#     )
#     return step_2_message

def get_step_9_message():
    items=["続けて登録","終わる"]
    quick_reply_buttons=[]

    for item in items:
        quick_reply_buttons.append(QuickReplyButton(action=MessageAction(label=item,text=item)))

    quick_reply=QuickReply(items=quick_reply_buttons)
    reply_message=TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            text='Googleスプレッドシートに保存しました',
            actions=[
                URIAction(
                    label='Googleスプレッドシート',
                    uri='https://docs.google.com/spreadsheets/d/1OERAl_cuhH6JPs4stJsfL1L7BD5gfTOfYJR5RK-GBF4/edit?usp=sharing'
                )
            ]
        ),
        quick_reply=quick_reply
    )
    return reply_message


def get_scenario_end_message():
    reply_message=TextSendMessage(
        text="シナリオを終了しました"
        )
    return reply_message


def get_test():
    reply_message=TextSendMessage(
        text="画像を受信しました"
        )
    return reply_message
