from fastapi import APIRouter
from config.db_firebase import Config_firebase
from config.heroku_environ import set_firebase

config = Config_firebase(path_db=set_firebase)
fb = config.database_fb()
router = APIRouter()


@router.get('/')
async def esp_get():
    data = [
        {
            'elc': 'ไฟตัวที่ 1',
            'description': 'ยังไม่เปิด',
            'status': False,
            'sensor': 'Lux: NaN'
        },
        {
            'elc': 'ไฟตัวที่ 2',
            'description': 'ยังไม่เปิด',
            'status': False,
            'sensor': 'Lux: NaN'
        },
        {
            'elc': 'ปั้มตัวที่ 1',
            'description': 'ยังไม่เปิด',
            'status': False,
            'sensor': 'lv.water: NaN'
        },
        {
            'elc': 'ปั้มตัวที่ 2',
            'description': 'ยังไม่เปิด',
            'status': False,
            'sensor': 'Temperature: NaN'
        },
    ]
    return data
