from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes import esp, callback
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
template = Jinja2Templates(directory='templates')

app.include_router(
    esp.router,
    prefix='/esp',
    tags=['esp'],
    responses={418: {'description': "I'm a teapot"}}
)

app.include_router(
    callback.router,
    prefix='/callback',
    tags=['Callback'],
    responses={418: {'description': "I'm a teapot"}}
)


@app.get('/index')
async def index(request: Request):
    return template.TemplateResponse('index.vue', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app:app', port=8050, debug=True)