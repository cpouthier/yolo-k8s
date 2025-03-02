# YOLOv8 Object Detection with Kubernetes on `pouthier.fr/yolo`

This project deploys **YOLOv8** for **image and video analysis** using **FastAPI** as the backend and **Streamlit** as the frontend. The deployment is configured to run on **Kubernetes** with a **PersistentVolumeClaim (PVC)** for model storage and is accessible at ``.

## **Features**

✅ Image and video object detection using **YOLOv8**\
✅ **FastAPI** backend with endpoints for image and video processing\
✅ **Streamlit** frontend for uploading and viewing detections\
✅ **Persistent Storage (PVC)** for model persistence\
✅ **Ingress configured for **``

---

## **1. Project Structure**

```
yolo-k8s/
│── backend/
│   ├── app.py                 # FastAPI backend
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend Dockerfile
│── frontend/
│   ├── interface.py            # Streamlit frontend
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Frontend Dockerfile
│── k8s/
│   ├── pvc.yaml                # Persistent Volume Claim (PVC)
│   ├── backend-deployment.yaml # Backend Deployment
│   ├── backend-service.yaml    # Backend Service
│   ├── frontend-deployment.yaml# Frontend Deployment
│   ├── frontend-service.yaml   # Frontend Service
│   ├── ingress.yaml            # Ingress for `pouthier.fr/yolo`
│── README.md                   # Documentation
```

---

## **2. Backend API (FastAPI)**

The **backend** is responsible for processing images and videos with YOLOv8.

### **Endpoints**

| Method | Endpoint           | Description                |
| ------ | ------------------ | -------------------------- |
| `POST` | `/yolo/api/image/` | Detect objects in an image |
| `POST` | `/yolo/api/video/` | Detect objects in a video  |

### **Persistent Storage (PVC)**

- The **YOLOv8 model is stored** in a **PersistentVolumeClaim (PVC)**.
- The backend **mounts **`` to use the stored model.

---

## **3. Frontend (Streamlit)**

The **Streamlit frontend** provides an **interface for uploading images and videos**.

### **Access the Web Interface**

Once deployed, access **YOLOv8 Object Detection** at:

🔗 [http://pouthier.fr/yolo](http://pouthier.fr/yolo)

### **Usage**

1. Upload an image → Objects detected and displayed.
2. Upload a video → Processed video with annotations returned.

---

## **4. Kubernetes Deployment**

The project is fully containerized and deployed in **Kubernetes**.

### **4.1 Create Persistent Volume Claim (PVC)**

```bash
kubectl apply -f k8s/pvc.yaml
```

### **4.2 Deploy Backend**

```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

### **4.3 Deploy Frontend**

```bash
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

### **4.4 Deploy Ingress for **``

```bash
kubectl apply -f k8s/ingress.yaml
```

This will configure an **Ingress Controller** to route requests to:

- `http://pouthier.fr/yolo/api/` → Backend API
- `http://pouthier.fr/yolo/` → Frontend Web UI

---

## **5. Model Storage & Video Processing**

### **5.1 Copy YOLOv8 Model to PVC**

Since the backend mounts `/app/models/`, we need to manually upload the model:

```bash
kubectl get pods
kubectl cp yolov8n.pt backend-pod:/app/models/yolov8n.pt
```

Replace `backend-pod` with the actual pod name.

### **5.2 Video Processing**

- The backend **stores videos temporarily** in an **emptyDir volume**.
- The video is **processed frame-by-frame** and annotated.
- The final **video is returned via FastAPI**.

---

## **6. Testing the API**

### **6.1 Test Image Detection**

```bash
curl -X POST "http://pouthier.fr/yolo/api/image/" -F "file=@test.jpg"
```

### **6.2 Test Video Detection**

```bash
curl -X POST "http://pouthier.fr/yolo/api/video/" -F "file=@test.mp4"
```

---

## **7. Future Improvements**

- 📌 **Add GPU acceleration** for faster inference.
- 📌 **Automate model download** from a cloud storage.
- 📌 **Add database storage** for detected results.

---

## **8. Conclusion**

This project enables **scalable object detection** for images and videos using **Kubernetes, FastAPI, and Streamlit**. The **PVC ensures model persistence**, and the **emptyDir storage handles video processing efficiently**.

🚀 **Ready to scale and deploy on **``**!**

