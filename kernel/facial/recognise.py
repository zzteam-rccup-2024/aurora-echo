import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
