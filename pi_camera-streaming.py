from flask import Flask, Response, request, redirect, url_for
from picamera2 import Picamera2
import cv2
import subprocess
import threading
import time

# Set up Web Server
app = Flask(__name__)

def generate_frames():
    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()

        # Convert to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in byte format to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
# Initialize the camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    picam2.start()
    t = threading.Thread(target=memory_monitor, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=8000, debug=False)
