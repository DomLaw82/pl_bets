import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from data_intake.per_90_stats import per_90_main
from db_connection import SQLConnection
from app_logger import FluentLogger

logger = FluentLogger("data_ingestion_monitor").get_logger()

pl_stats_connector = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        try:
            if 'data/historic_player_stats' in event.src_path:
                per_90_main(pl_stats_connector, single_season=event.src_path.split('/')[3])
        except Exception as e:
            logger.error(f'Error on upload: {e}')
            return f'Error on upload: {e}'
    
def monitor_files():
    path_to_watch = './data'
    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()