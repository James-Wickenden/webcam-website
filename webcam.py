from flask import Flask, render_template, Response
import cv2

# Initialize the Flask app and camera object
app = Flask(__name__)
camera = cv2.VideoCapture(0)


# Flask index page route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def resize_frame(frame):
	scale_percent = 100 # percent of original size
	width = int(frame.shape[1] * scale_percent / 100)
	height = int(frame.shape[0] * scale_percent / 100)
	dim = (width, height)

	resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
	return resized


def generate_frames():
	while True:
		success, frame = camera.read()
		frame = resize_frame(frame)
		if not success:
			camera.release()
			cv2.destroyAllWindows()
			break
		else:
			ret, buffer = cv2.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		
		k = cv2.waitKey(1)
		if k != -1:
			# cv2.imwrite('testimage.jpg', frame)
			camera.release()
			cv2.destroyAllWindows()
			break


if __name__ == "__main__":
    app.run(debug=True)