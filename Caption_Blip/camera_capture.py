from picamera2 import Picamera2
from time import sleep

picam2 = Picamera2()

# Set full-resolution capture config
config = picam2.create_still_configuration(main={"size": (4608, 2592)})
picam2.configure(config)
picam2.start()

sleep(1)  # Let camera adjust
picam2.capture_file("image.jpg")
print("Captured full-res image.jpg")

picam2.stop()
