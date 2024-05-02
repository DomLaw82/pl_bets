import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
		# Add action to run function based on the src path of the file
        print(f'File {event.src_path} has been modified')
    
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