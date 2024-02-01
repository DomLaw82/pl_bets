FROM python:3.11.7-bookworm

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

COPY ../database/ingestion/data_intake ./remote_data_intake

COPY ../database/ingestion/__init__.py ./remote_data_intake.py

# Replace "data_intake" with "remote_data_intake" in the script
# Updating import and file paths for api directory
RUN sed -i 's/data_intake/remote_data_intake/g' ./remote_data_intake.py
RUN sed -i 's/data_intake/remote_data_intake/g' ./remote_data_intake/country_competition.py
RUN sed -i 's/data_intake/remote_data_intake/g' ./remote_data_intake/player.py
RUN sed -i 's/data_intake/remote_data_intake/g' ./remote_data_intake/season_schedule.py
RUN sed -i 's/data_intake/remote_data_intake/g' ./remote_data_intake/team_ref_match.py
RUN sed -i 's/data_intake/remote_data_intake/g' ./remote_data_intake/per_90_stats.py


RUN sed -i 's/..\/data/.\/data/g' ./remote_data_intake/download_latest_data.py

RUN mkdir ./remote_data_intake/data

EXPOSE 8080

CMD ["python3", "-u", "api.py"]