from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import os
import numpy as np
import cv2
import tempfile
from PIL import Image
import io

# Définition du chemin du modèle YOLOv8 stocké dans le PVC
MODEL_PATH = "/app/models/yolov8n.pt"

# Vérification si le modèle est disponible
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Le modèle {MODEL_PATH} est introuvable. Vérifiez le PVC.")

# Charger le modèle YOLOv8
model = YOLO(MODEL_PATH)

app = FastAPI()

@app.post("/predict/image/")
async def predict_image(file: UploadFile = File(...)):
    """Analyse une image et retourne les objets détectés."""
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image = np.array(image)

        results = model(image)

        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].tolist()
                cls = int(box.cls[0])
                detections.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2, "confidence": conf, "class": cls})

        return JSONResponse(content={"detections": detections})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/predict/video/")
async def predict_video(file: UploadFile = File(...)):
    """Analyse une vidéo et retourne un fichier vidéo annoté."""
    try:
        # Enregistrement temporaire de la vidéo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(await file.read())
            video_path = temp_file.name

        # Charger la vidéo avec OpenCV
        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(f"{video_path}_output.mp4", fourcc, 30.0, 
                              (int(cap.get(3)), int(cap.get(4))))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Détection d'objets
            results = model(frame)

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = box.conf[0].tolist()
                    cls = int(box.cls[0])

                    # Dessiner les rectangles autour des objets détectés
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{cls} ({conf:.2f})", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            out.write(frame)

        cap.release()
        out.release()

        # Lire la vidéo annotée
        with open(f"{video_path}_output.mp4", "rb") as f:
            video_data = f.read()

        os.remove(video_path)
        os.remove(f"{video_path}_output.mp4")

        return JSONResponse(content={"video": video_data})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)