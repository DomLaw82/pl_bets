FROM python:3.11.7-bookworm

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt


EXPOSE 8080

CMD ["python3", "api.py"]