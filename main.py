from kernel.speech.record import save_to_wav, record_audio
from kernel.speech.recognize import recognize_audio
from kernel.text.entity import recognize_entities
from kernel.text.sentiment.train import load_sentiment_model
from kernel.text.sentiment.predict import predict_sentiment
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from kernel.camera.manager import CameraManager

app = FastAPI()
camera = CameraManager()


@app.get("/")
def read_root():
    return {"app_name": "Aurora Echo"}


@app.get("/camera")
async def camera_feed():
    return StreamingResponse(camera.video_frame(), media_type='multipart/x-mixed-replace; boundary=frame')


def main():
    audio = record_audio()
    print(f"Recorded {len(audio) / 16000:.2f}")
    recognised = recognize_audio(audio)
    save_to_wav(audio)
    print(f"Recognised: {recognised}")
    recognize_entities(recognised)
    load_sentiment_model()
    sentiment = predict_sentiment(recognised)


if __name__ == "__main__":
    main()