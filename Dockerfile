FROM python:3.7.11-slim
WORKDIR /app
COPY ./moddy /app/moddy
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
CMD ["python3", "-m", "moddy"]
