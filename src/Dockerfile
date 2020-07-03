FROM python:3.8

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

CMD ["python", "main.py"]
