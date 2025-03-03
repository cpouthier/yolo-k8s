FROM python:3.9

WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /venv

# Activate virtual environment and install dependencies
RUN /venv/bin/pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN /venv/bin/pip install -r requirements.txt

# Copy app files
COPY . .

# Set the default command using the virtual environment
CMD ["/venv/bin/python", "app.py"]
