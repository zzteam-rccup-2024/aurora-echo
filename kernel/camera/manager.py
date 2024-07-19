import asyncio
import cv2
from kernel.facial.predict import FacialEmotionRecognizer
from kernel.gesture.thumb import get_thumb
from kernel.facial.mosaic import PerformMosaic

transform = PerformMosaic()


class CameraManager:
    def __init__(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)
        self.face_recognizer = FacialEmotionRecognizer()
        self.facial_expressions = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'neutral': 0, 'sad': 0,
                                   'surprise': 0}
        self.hand_action = 'none'
        self.emotion = 'neutral'
        self.thumbs = {'up': 0, 'down': 0}

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            return None
        return frame

    def recognize_face(self):
        frame = self.get_frame()
        result = self.face_recognizer(frame)
        if result == 'others':
            return
        self.emotion = result
        self.facial_expressions[result] += 1
        return result

    def get_facial_list(self):
        return list(map(lambda x: x[0], sorted(self.facial_expressions.items(), key=lambda x: x[1], reverse=True)))

    def get_emotion_percents(self):
        total = sum(self.facial_expressions.values())
        result = [(k, v / total) for k, v in self.facial_expressions.items() if v > 0]
        return sorted(result, key=lambda x: x[1], reverse=True)

    def recognize_gesture(self):
        frame = self.get_frame()
        thumb = get_thumb(frame)
        if thumb == 'thumb up':
            self.thumbs['up'] += 1
        elif thumb == 'thumb down':
            self.thumbs['down'] += 1
        return thumb

    def video_frame(self, mosaic=False):
        _, frame = self.camera.read()
        while True:
            _, frame = self.camera.read()
            if not _:
                break
            thumb = self.recognize_gesture()
            if mosaic:
                frame = transform(frame)
            cv2.putText(frame, thumb, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            emotion = self.recognize_face()
            cv2.putText(frame, emotion, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            asyncio.sleep(0.1)
