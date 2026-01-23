from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from picamera2.outputs import MP4Output

import time

# setup for video
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (1280, 720), "format": "RGB888"}
)
picam2.configure(config)
encoder = H264Encoder(bitrate=2_000_000)  # 2Mbps
#output = FileOutput("video.h264")
output = MP4Output("video.mp4")

picam2.start_recording(encoder, output)
time.sleep(5)
picam2.stop_recording()

print("video.mp4 is saved")