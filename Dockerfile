FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-devel

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# TODO: Optimize
COPY ./*.py /app
COPY ./api ./app/api
COPY ./payloads ./app/payloads

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "0"]