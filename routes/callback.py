from fastapi import APIRouter, Request, HTTPException, Body
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import StickerSendMessage, TextSendMessage, TextMessage, MessageEvent
from random import randint
from typing import Optional
from config.object_str import CutId
from bson import ObjectId
from config.db_pymongo import MongoDB
import datetime
import json
import os


router = APIRouter()

line_bot_api = LineBotApi(os.environ['line_bot_api'])
handler = WebhookHandler(os.environ['handler'])

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


@router.post('/')
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
    pass


@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    replyToken = event.reply_token
    message_text = event.message.text
    line_bot_api.reply_message(replyToken, TextSendMessage(text=message_text))
