FROM python:3.8-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

COPY app /app
COPY entrypoint.sh /app

WORKDIR /app
RUN mkdir /app/images

CMD /app/entrypoint.sh
