FROM repo.kibblator.co.uk/dg-python-tesseract-ocr:3.12-slim-bullseye

COPY . /dg.weighttool/
RUN pip install -r ./dg.weighttool/requirements.txt && mkdir -p ./dg.weighttool/images

CMD ["python", "-u", "./dg.weighttool/main.py"]