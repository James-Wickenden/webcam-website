from flask import Flask, render_template, Response
import cv2

# Initialize the Flask app and camera object
app = Flask(__name__)
camera = cv2.VideoCapture(0)
print(type(camera))
print(camera.isOpened())

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Unused
def resize_frame(frame, percent_to_reduce_to):
        scale_percent = percent_to_reduce_to # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        return resized


# Generate a buffered frame for /video_feed
def generate_frames():
        while True:
                success, frame = camera.read()
                #frame = resize_frame(frame, 100)
                if not success:
                        camera.release()
                        cv2.destroyAllWindows()
                        break
                else:
                        ret, buffer = cv2.imencode('.jpg', frame)
                        frame = buffer.tobytes()
                        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Run main
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
