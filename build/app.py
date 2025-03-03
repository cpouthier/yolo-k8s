from flask import Flask, render_template, request, send_file
import os
from ultralytics import YOLO
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the latest YOLOv8 model
model = YOLO("yolov8n.pt")  # You can use yolov8s.pt, yolov8m.pt, etc.

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Run YOLOv8 detection
            results = model(filepath)

            # Save the output image
            output_image_path = os.path.join(OUTPUT_FOLDER, filename)
            results[0].save(output_image_path)  # Saves result image with detections

            return send_file(output_image_path, mimetype="image/jpeg")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
