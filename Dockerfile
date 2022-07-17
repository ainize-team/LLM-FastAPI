FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-devel

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "0"]