import cv2
import os
import base64


class Client:
    def Capture(self):
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            path = os.path.join("Temp" , 'GPT-Image.jpg')
            cv2.imwrite(path, frame)
            return path
    def encode_image(self, path):
            with open(path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')