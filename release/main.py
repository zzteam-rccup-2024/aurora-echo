from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from kernel.camera.manager import CameraManager
from kernel.provider import AuroraEchoConfig, AuroraEchoProvider
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'],
                   allow_headers=['*'])
camera = CameraManager()
config = AuroraEchoConfig(mosaic=True)
provider = AuroraEchoProvider(camera, config)


@app.get("/")
def read_root():
    return {"app_name": "Aurora Echo"}


@app.get("/camera/{mosaic}")
async def camera_feed(mosaic: str = 'blur'):
    return StreamingResponse(camera.video_frame(mosaic=mosaic), media_type='multipart/x-mixed-replace; boundary=frame')


@app.post('/record')
async def record():
    provider.start_recognize()


@app.get('/text')
async def text():
    return {'status': 'error', 'message': 'record is not completed'} if provider.recognizing else {'status': 'success',
                                                                                                   'data': provider.text}


@app.get('/sentiment')
async def sentiment():
    return {'status': 'error', 'message': 'record is not completed'} if provider.recognizing else {'status': 'success',
                                                                                                   'data': provider.sentiment}


@app.get('/named_entities')
async def named_entities():
    return {'status': 'error', 'message': 'record is not completed'} if provider.recognizing else {'status': 'success',
                                                                                                   'data': provider.named_entities}


@app.post('/llm/{model}')
async def llm(model: str):
    provider.start_llm('object', model)
    provider.start_llm('subject', model)
    provider.start_llm('json', model)


@app.get('/llm/object')
async def llm_object():
    return {'status': 'error', 'message': 'generation is not completed'} if provider.generating else {
        'status': 'success', 'data': provider.get_object_analysis()}


@app.get('/llm/subject')
async def llm_subject():
    return {'status': 'error', 'message': 'generation is not completed'} if provider.generating else {
        'status': 'success', 'data': provider.get_subject_analysis()}


class Product(BaseModel):
    product: str


class Mosaic(BaseModel):
    mosaic: bool


@app.post('/mosaic')
async def config_mosaic(mosaic: Mosaic):
    provider.set_mosaic(mosaic.mosaic)
    print(provider.apply_mosaic)


@app.get('/emotion')
async def get_emotion():
    emotion = provider.camera.get_emotion_percents()
    return emotion


@app.get('/thumb')
async def get_thumb():
    thumbs = provider.camera.thumbs
    total = thumbs['up'] + thumbs['down'] if thumbs['up'] + thumbs['down'] > 0 else 1
    return [('thumb up', thumbs['up'] / total), ('thumb down', thumbs['down'] / total)].sort(key=lambda x: x[1], reverse=True)
