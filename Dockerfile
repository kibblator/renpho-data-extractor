FROM python:3.12-slim-bullseye

COPY . /renpho-extractor/
RUN pip install -r ./renpho-extractor/requirements.txt && mkdir -p ./renpho-extractor/images

CMD ["python", "-u", "./renpho-extractor/main.py"]