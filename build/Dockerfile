FROM python:3.9

WORKDIR /app

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Create a virtual environment
RUN python3 -m venv /venv

# Activate virtual environment and install Python dependencies
RUN /venv/bin/pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN /venv/bin/pip install -r requirements.txt

# Copy application files
COPY . .

# Run the application
CMD ["/venv/bin/python", "app.py"]
