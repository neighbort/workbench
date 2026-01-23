from picamera2 import Picamera2
import time

# setup for single photo
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

picam2.start()
time.sleep(2)   # wait for sensor stable
picam2.capture_file("photo.jpg")
picam2.stop()

print("photo.jpg is saved")