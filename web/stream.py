import cv2
from flask import Flask, Response, render_template

from misukasu.measure import Measurer

app = Flask(__name__)

mes = Measurer()
mes.run()

def get_camera_frame():
      while True:
            frame = mes.latest_camera.data
            if frame.shape != (0,):
                  _, frame = cv2.imencode('.jpg', frame)
                  frame = frame.tobytes()
                  yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_radar_frame():
      while True:
            frame = mes.latest_radar.data
            if frame.shape != (0,):
                  _, frame = cv2.imencode('.jpg', frame[:, :, 0:3])
                  frame = frame.tobytes()
                  yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/camera_feed')
def camera_feed():
      return Response(get_camera_frame(), mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/radar_feed')
def radar_feed():
      return Response(get_radar_frame(), mimetype='multipart/x-mixed-replace;boundary=frame')

if __name__ == '__main__':
      app.run(debug = False)