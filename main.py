from kernel.speech.record import save_to_wav, record_audio
from kernel.speech.recognize import recognize_audio
from kernel.text.entity import recognize_entities


def main():
    audio = record_audio()
    print(f"Recorded {len(audio) / 16000:.2f}s")
    recognised = recognize_audio(audio)
    save_to_wav(audio)
    print(f"Recognised: {recognised}")
    recognize_entities(recognised)


def train_sentiment():
    from kernel.text.sentiment.train import train
    train()


if __name__ == "__main__":
    train_sentiment()