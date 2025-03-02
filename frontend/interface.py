import streamlit as st
import requests
import io
from PIL import Image, ImageDraw

st.title("YOLOv8 - Détection d'objets sur Images et Vidéos")

# Sélection du type d'analyse
option = st.radio("Choisissez le type de fichier :", ["Image", "Vidéo"])

if option == "Image":
    uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Image chargée", use_column_width=True)

        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://backend:8000/predict/image/", files=files)

        if response.status_code == 200:
            result = response.json()
            detections = result.get("detections", [])

            draw = ImageDraw.Draw(image)
            for obj in detections:
                x1, y1, x2, y2 = obj["x1"], obj["y1"], obj["x2"], obj["y2"]
                confidence = obj["confidence"]
                cls = obj["class"]

                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                draw.text((x1, y1), f"{cls} ({confidence:.2f})", fill="red")

            st.image(image, caption="Résultat de la détection", use_column_width=True)
        else:
            st.error("Erreur dans la prédiction")

elif option == "Vidéo":
    uploaded_file = st.file_uploader("Choisissez une vidéo...", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        st.video(uploaded_file)

        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://backend:8000/predict/video/", files=files)

        if response.status_code == 200:
            result = response.json()
            video_data = result.get("video")

            st.video(io.BytesIO(video_data))
        else:
            st.error("Erreur dans l'analyse de la vidéo")