FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install required dependencies for OpenCV
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp