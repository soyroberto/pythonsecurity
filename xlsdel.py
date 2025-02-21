#Sample code exemplying a bad actor running as a daemon to delete files with .xls extension in a folder as they are created
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory to monitor
directory_to_watch = "/Users/xfolders/xls"

# Handler for file system events
class DocxDeletionHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the created file has a .docx extension
        if event.is_directory:
            return
        if event.src_path.endswith(".xls"):
            print(f"Found .XLS file: {event.src_path}")
            self.delete_file(event.src_path)

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Function to start the daemon
def start_daemon():
    event_handler = DocxDeletionHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=False)
    observer.start()

    print(f"Started monitoring {directory_to_watch} for .xls files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_daemon()