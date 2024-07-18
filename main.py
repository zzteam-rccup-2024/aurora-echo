# from kernel.speech.record import save_to_wav, record_audio
# from kernel.speech.recognize import recognize_audio
# from kernel.text.entity import recognize_entities
# from kernel.text.sentiment.train import load
# from kernel.text.sentiment.predict import predict_sentiment


# def main():
#     audio = record_audio()
#     print(f"Recorded {len(audio) / 16000:.2f}")
#     recognised = recognize_audio(audio)
#     save_to_wav(audio)
#     print(f"Recognised: {recognised}")
#     recognize_entities(recognised)
#     load()
#     sentiment = predict_sentiment(recognised)
#     print(sentiment)


def train_facial():
    from kernel.facial.dataset import load_data_loader
    from kernel.facial.model import fetch_model, save_model
    from kernel.facial.train import train_model

    train_loader, test_loader = load_data_loader()
    model, criterion, optimizer = fetch_model()
    train_model(model, criterion, optimizer, train_loader, test_loader, "facial.pth")


if __name__ == "__main__":
    train_facial()