from flask import Flask, Response, request, redirect, url_for
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
import threading
import time
import io
import subprocess

# Set up Web Server
app = Flask(__name__)

# --- カメラ初期化 ---
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    controls={"FrameRate": 10}
)
picam2.configure(config)
picam2.start()
frame_buffer = io.BytesIO()
buffer_lock = threading.Lock()

class MJPEGBuffer(FileOutput):
    def outputframe(self, frame, *args, **kwargs):
        with buffer_lock:
            frame_buffer.seek(0)
            frame_buffer.truncate()
            frame_buffer.write(frame)

encoder = MJPEGEncoder()
output = MJPEGBuffer(frame_buffer)

picam2.start_recording(encoder, output)
camera_enabled = True


# --- MJPEG ストリーム ---
def generate_frames():
    global camera_enabled
    while True:
        if not camera_enabled:
            time.sleep(0.1)
            continue

        with buffer_lock:
            data = frame_buffer.getvalue()

        if data:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + data + b"\r\n"
            )
        time.sleep(0.01)


def memory_monitor(interval=5):
    while True:
        print("\n===== free -m =====")
        subprocess.run(["free", "-m"])
        time.sleep(interval)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['GET', 'POST'])
def index():
    return """
    <html>
        <body>
            <h1>Raspberry Pi Camera Live Stream</h1>
            <img src="/video_feed" width="640" height="480">
            <br>
            <form action='' method='post', novalidate="novalidate">
                <input type="submit", name="move", value="left"/>
            </form>
            <form action='' method='post', novalidate="novalidate">
                <input type="submit", name="move", value="right"/>
            </form>
        </body>
    </html>
    """

if __name__ == '__main__':
    t = threading.Thread(target=memory_monitor, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=8000, debug=False)
