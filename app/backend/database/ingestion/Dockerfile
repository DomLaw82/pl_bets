FROM python:3.11.7-bookworm

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["python3", "-u", "__init__.py"]