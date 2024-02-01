FROM python:3.11.7-bookworm

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

COPY ../database/ingestion/data_intake ./remote_data_intake

RUN mkdir ./remote_data_intake/data

EXPOSE 8080

CMD ["python3", "-u", "api.py"]