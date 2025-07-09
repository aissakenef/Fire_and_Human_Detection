from flask import Flask, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("not open")
    exit()

def generate_frames():
    while True:
        suc, frame = camera.read()
        if not suc:
            print("erorr 1")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("erorr 2")
                break
            
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
            
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        print("Start...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        camera.release()
        print("Camera release")