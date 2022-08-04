FROM python:3.8.13-slim-buster

WORKDIR /app
COPY ./src/ ./
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ./start.sh
