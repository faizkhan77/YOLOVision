import os
from flask import Flask, render_template, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2
import numpy as np
import subprocess

app = Flask(__name__)

# Define paths for uploads and outputs
UPLOAD_FOLDER = "static/uploads/"
OUTPUT_FOLDER = "static/output/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")


# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")


# Route to handle file upload and detection
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Perform detection for image
        if file_path.endswith(("png", "jpg", "jpeg", "JPG", "JPEG")):
            img = cv2.imread(file_path)[..., ::-1]  # Convert BGR to RGB
            results = model.predict(img, save=True)
            output_image_path = os.path.join(
                app.config["OUTPUT_FOLDER"], "images", filename
            )
            cv2.imwrite(output_image_path, results[0].plot()[..., ::-1])  # Save as BGR

            return redirect(url_for("display_image", filename=filename))

        # Perform detection for video
        elif file_path.endswith(("mp4")):
            cap = cv2.VideoCapture(file_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Path for processed video
            output_video_path = os.path.join(
                app.config["OUTPUT_FOLDER"], "videos", filename
            )
            output_video_path = os.path.normpath(output_video_path)  # Normalize path

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert the frame from BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = model.predict(rgb_frame)
                frame_with_detections = results[0].plot()
                out.write(
                    frame_with_detections[..., ::-1]
                )  # Convert RGB to BGR for saving

            cap.release()
            out.release()

            # --------------------------- RE-ENCODING using ffmpeg --------------------------------------
            """
            I need to re-encode the detected output video because after detection the output video has an
            unsupported video codec or encoding thats not supported on some browser, hence I'm using 
            "ffmpeg" to convert it to a more useable format then deleting the original output and just using the
            re-encoded video
            """

            # Define path for the re-encoded video
            reencoded_filename = "reencoded_" + filename
            reencoded_video_path = os.path.join(
                app.config["OUTPUT_FOLDER"], "videos", reencoded_filename
            )
            reencoded_video_path = os.path.normpath(
                reencoded_video_path
            )  # Normalize path (this is important)

            # Use FFmpeg command to re-encode the video
            ffmpeg_command = [
                "ffmpeg",
                "-y",  # Overwrite output file without asking
                "-i",
                output_video_path,
                "-vcodec",
                "libx264",
                "-acodec",
                "aac",
                reencoded_video_path,
            ]

            # Run the FFmpeg command
            subprocess.run(ffmpeg_command, check=True)

            # Optionally, remove the original processed video if no longer needed
            os.remove(output_video_path)

            # ----------------------------------------------------------------------------------------

            # Print paths for debugging
            # print(f"Output video path: {output_video_path}")
            # print(f"Reencoded video path: {reencoded_video_path}")

            return redirect(url_for("display_video", filename=reencoded_filename))

    return redirect(url_for("index"))


@app.route("/display/image/<filename>")
def display_image(filename):
    return render_template("display_image.html", filename=filename)


@app.route("/display/video/<filename>")
def display_video(filename):
    return render_template("display_video.html", filename=filename)


# --------------------------------------------- LIVE DETECTION CODE ---------------------------------------------


# Route to serve the live detection page
@app.route("/live_detection")
def live_detection():
    return render_template("live_detection.html")


# Route to handle the live camera stream
@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


def generate_frames():
    camera = cv2.VideoCapture(0)  # Use the webcam

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Perform detection
            results = model(frame)

            # Extract the first result and plot the detections on the frame
            result = results[0]  # Access the first element of the results list
            frame_with_detections = result.plot()  # Plot the detections on the frame

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode(".jpg", frame_with_detections)
            frame = buffer.tobytes()

            # Yield the frame to be used in the Response
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    camera.release()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
