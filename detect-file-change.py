# import the modules
import subprocess
import sys
import time

from rich.console import Console
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer

console = Console()


def on_event(func):
    def wrapped(self, event):
        event_method = getattr(super(self.__class__, self), func.__name__)
        self.has_change = True
        event_method(event)
        func(self, event)

    return wrapped


class MyHandler(RegexMatchingEventHandler):

    currentEvent = ""
    update = False

    def __init__(self):
        super().__init__(
            ignore_regexes=[
                r"\.git/.*",
                r"\.venv/.*",
                r".*/.mypy_cache/.*",
                r".*/__pycache__/.*",
                r".*\.tmp",
            ],
            ignore_directories=True,
        )
        self.observer = Observer()
        self.has_change = False

    @on_event
    def on_modified(self, event):
        console.log(f"[dim #e8fff8]modified {event.src_path}")

    @on_event
    def on_deleted(self, event):
        console.log(f"[#fa0068]deleted {event.src_path}")

    @on_event
    def on_created(self, event):
        console.log(f"[#7DEB34]created {event.src_path}")

    @on_event
    def on_moved(self, event):
        console.log(f"[#d1ca3b]moved {event.src_path} {event.dest_path}")

    def run(self):
        self.observer.schedule(self, path, recursive=True)
        console.log("File watcher started...")
        self.observer.start()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."

    # Initialize logging event handler
    handler = MyHandler()
    handler.run()

    try:
        while True:
            # Set the thread sleep time
            time.sleep(3)
            if handler.has_change:
                console.log("[#f5d47f]Synchronizing files...")
                subprocess.run(
                    "rsync -azP --exclude=__pycache__,.mypy_cache moddy aws-moddity:/app/ ",
                    shell=True,
                    stdout=subprocess.PIPE,
                )
                console.log("[green]Successfully completed synchronization")
                handler.has_change = False
    except KeyboardInterrupt:
        handler.observer.stop()
    handler.observer.join()
