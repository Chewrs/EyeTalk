import time

from camera_handler import CameraHandler

import threading

# Init






camera = CameraHandler() #picamera2

def capture_image(image_path = "Images/image.jpg"):
    camera.capture_image(image_path)

threading.Thread(target=capture_image).start()

