from fastapi import APIRouter, Request, HTTPException, Body
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import StickerSendMessage, TextSendMessage, TextMessage, MessageEvent
from random import randint
from typing import Optional
from config.object_str import CutId
from features.flex_message import flex_iot
from bson import ObjectId
from config.db_pymongo import MongoDB
from config.db_firebase import Config_firebase
from config.heroku_environ import set_firebase
from routes.esp import obj
import datetime
import json
import os

router = APIRouter()

line_bot_api = LineBotApi(os.environ['line_bot_api'])
handler = WebhookHandler(os.environ['handler'])
config = Config_firebase(path_db=set_firebase)
fb = config.database_fb()

client = os.environ.get('MONGODB_URI')
db = MongoDB(database_name='Mango', uri=client)
collection = 'line_bot_iot'


def get_profile(user_id):
    profile = line_bot_api.get_profile(user_id)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    key = CutId(_id=ObjectId()).dict()['id']
    _d = datetime.datetime.now()
    date = _d.strftime("%d/%m/%y")
    time = _d.strftime("%H:%M:%S")
    result = {
        'display_name': displayName,
        'user_id': userId,
        'img': img,
        'status': status,
        'id': key,
        'date': date,
        'time': time,
    }
    return result


@router.post('/webhook')
async def callback_notify(
        request: Request,
        raw_json: Optional[dict] = Body(None)
):
    with open('static/line_log.json', 'w') as log_line:
        json.dump(raw_json, log_line)
    try:
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        events = raw_json['events'][0]
        _type = events['type']
        if _type == 'follow':
            userId = events['source']['userId']
            profile = get_profile(userId)
            db.insert_one(collection='line_follower', data=profile)
        elif _type == 'unfollow':
            userId = events['source']['userId']
            db.delete_one('line_follower', query={'userId': userId})
        elif _type == 'postback':
            event_postback(events)
        elif _type == 'message':
            message_type = events['message']['type']
            if message_type == 'text':
                try:
                    handler.handle(str(body, encoding='utf8'), signature)
                except InvalidSignatureError as v:
                    api_error = {'status_code': v.status_code, 'message': v.message}
                    raise HTTPException(status_code=400, detail=api_error)
            else:
                no_event = len(raw_json['events'])
                for i in range(no_event):
                    events = raw_json['events'][i]
                    event_handler(events)
    except IndexError:
        raise HTTPException(status_code=200, detail={'Index': 'null'})
    return raw_json


def event_handler(event):
    replyToken = event['replyToken']
    package_id = '446'
    stickerId = randint(1988, 2027)
    line_bot_api.reply_message(replyToken, StickerSendMessage(package_id, str(stickerId)))


def event_postback(event):
    postback = event['postback']
    replyToken = event['replyToken']
    userId = event['source']['userId']
    relay = postback['data']
    fb.child('p1').child('relays').set({'node': int(relay)})
    relay = int(relay)
    before_data = fb.child('p1').child('switch').get()
    fb.child('p1').child('relays').set({'node': relay})
    if relay == 1:
        pump1 = before_data.val()['pump1']
        pump2 = before_data.val()['pump2']
        res = obj(1, 1, pump1, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 2:
        pump1 = before_data.val()['pump1']
        pump2 = before_data.val()['pump2']
        res = obj(0, 0, pump1, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 3:
        pump1 = before_data.val()['pump1']
        pump2 = before_data.val()['pump2']
        ls2 = before_data.val()['ls2']
        res = obj(1, ls2, pump1, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 4:
        pump1 = before_data.val()['pump1']
        pump2 = before_data.val()['pump2']
        ls2 = before_data.val()['ls2']
        res = obj(0, ls2, pump1, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 5:
        pump1 = before_data.val()['pump1']
        pump2 = before_data.val()['pump2']
        ls1 = before_data.val()['ls1']
        res = obj(ls1, 1, pump1, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 6:
        pump1 = before_data.val()['pump1']
        pump2 = before_data.val()['pump2']
        ls1 = before_data.val()['ls1']
        res = obj(ls1, 0, pump1, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 7:
        pump2 = before_data.val()['pump2']
        ls1 = before_data.val()['ls1']
        ls2 = before_data.val()['ls2']
        res = obj(ls1, ls2, 0, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 8:
        pump2 = before_data.val()['pump2']
        ls1 = before_data.val()['ls1']
        ls2 = before_data.val()['ls2']
        res = obj(ls1, ls2, 1, pump2)
        fb.child('p1').child('switch').update(res)
    elif relay == 9:
        pump1 = before_data.val()['pump1']
        ls1 = before_data.val()['ls1']
        ls2 = before_data.val()['ls2']
        res = obj(ls1, ls2, pump1, 0)
        fb.child('p1').child('switch').update(res)
    elif relay == 10:
        pump1 = before_data.val()['pump1']
        ls1 = before_data.val()['ls1']
        ls2 = before_data.val()['ls2']
        res = obj(ls1, ls2, pump1, 1)
        fb.child('p1').child('switch').update(res)
    package_id = '6136'
    sticker_id = randint(10551376, 10551399)
    if relay == 3 or relay == 5:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='เปิดไฟแล้วครับ'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))
    elif relay == 4 or relay == 6:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='ปิดไฟแล้วครับ'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))
    elif relay == 10 or relay == 8:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='เปิดปั๊มแล้วครับ'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))
    elif relay == 9 or relay == 7:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='ปิดปั๊มแล้วครับ'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))


@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    replyToken = event.reply_token
    message_text = event.message.text
    if message_text == '#sensors':
        ref = fb.child('p1').child('sensors').get().val()
        text = 'อุณหภูมิมีค่า : {}\nระดับน้ำมีค่า : {}\n แสงมีค่า : {}'.format(ref['temperature'], ref['level_water'],
                                                                               ref['lux'])
        line_bot_api.reply_message(replyToken, TextSendMessage(text=text))
    if message_text == '#control':
        line_bot_api.reply_message(replyToken, flex_iot())
