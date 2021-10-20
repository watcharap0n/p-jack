from fastapi import APIRouter
from config.db_firebase import Config_firebase
from config.heroku_environ import set_firebase

config = Config_firebase(path_db=set_firebase)
fb = config.database_fb()
router = APIRouter()


def obj(sw1: int, sw2: int, sw3: int, sw4: int) -> dict:
    data = {
        'ls1': sw1,
        'ls2': sw2,
        'pump1': sw3,
        'pump2': sw4
    }
    return data


def num_boolean(num: int) -> bool:
    if num == 0:
        return False
    elif num == 1:
        return True


def num_description(num: int) -> str:
    if num == 0:
        return 'ยังไม่เปิด'
    elif num == 1:
        return 'เปิดแล้ว'


@router.get('/')
async def esp_get(relay: int = None):
    if relay:
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
    ref = fb.child('p1').get()
    data = [
        {
            'elc': 'ไฟตัวที่ 1',
            'description': num_description(ref.val()['switch']['ls1']),
            'status': num_boolean(ref.val()['switch']['ls1']),
            'sensor': ref.val()['sensors']['lux']
        },
        {
            'elc': 'ไฟตัวที่ 2',
            'description': num_description(ref.val()['switch']['ls2']),
            'status': num_boolean(ref.val()['switch']['ls2']),
            'sensor': ref.val()['sensors']['lux']
        },
        {
            'elc': 'ปั้มตัวที่ 1',
            'description': num_description(ref.val()['switch']['pump1']),
            'status': num_boolean(ref.val()['switch']['pump1']),
            'sensor': ref.val()['sensors']['level_water']
        },
        {
            'elc': 'ปั้มตัวที่ 2',
            'description': num_description(ref.val()['switch']['pump2']),
            'status': num_boolean(ref.val()['switch']['pump2']),
            'sensor': ref.val()['sensors']['temperature']
        },
    ]
    return data
