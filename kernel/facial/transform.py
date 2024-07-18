import mediapipe as mp
import cv2
from cv2.typing import MatLike
from PIL import Image
import numpy as np
from torchvision import transforms

mp_face_mesh = mp.solutions.face_mesh
face = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)


class ToNumpy:
    def __call__(self, image: Image):
        return np.array(image)


class CropToFace:
    def __call__(self, image: MatLike):
        results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            x_min = y_min = 0
            y_max, x_max, _ = image.shape
            for face_landmarks in results.multi_face_landmarks:
                for i in range(468):
                    if face_landmarks.landmark[i].visibility < 0 or face_landmarks.landmark[i].presence < 0:
                        continue
                    x, y = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x)
                    y_max = max(y_max, y)

            image = image[int(y_min):int(y_max), int(x_min):int(x_max)]
            # Resize the cropped hand image to 256x256
            image = cv2.resize(image, (256, 256))
        else:
            image = cv2.resize(image, (256, 256))
        return image


transform = transforms.Compose([
    ToNumpy(),
    CropToFace(),
    transforms.ToPILImage(),
    transforms.Resize((256, 256)),
    transforms.RandomRotation((-180, 180)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
