FROM python:3.8-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

RUN mkdir /app && mkdir /app/images
COPY app.py /app
COPY entrypoint.sh /app

WORKDIR /app

CMD /app/entrypoint.sh
