from kernel.speech.record import save_to_wav, record_audio
from kernel.speech.recognize import recognize_audio
from kernel.text.entity import recognize_entities
from kernel.text.sentiment.train import load_sentiment_model
from kernel.text.sentiment.predict import predict_sentiment


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