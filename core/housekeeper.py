import pathlib
import typing
from threading import Lock

from core.config import Config


class Housekeeper:
    tracked_files: typing.List[pathlib.Path]
    file_list_lock: Lock

    def __init__(self):
        self.tracked_files = []
        self.file_list_lock = Lock()

    def add_file(self, path: pathlib.Path) -> None:
        self.tracked_files.append(path)

    def sweep(self, items_to_keep: int = Config.max_stored_files):
        self.file_list_lock.acquire()
        if len(self.tracked_files) > items_to_keep:
            for _ in range(len(self.tracked_files) - items_to_keep):
                processed_file = self.tracked_files.pop(0)
                print('deleting ' + str(processed_file))
        self.file_list_lock.release()

    def scan(self):
        files = pathlib.Path(Config.output_file_path).glob('*.mp3')
        file_stats = sorted([(filename, filename.stat()) for filename in files], key=lambda file: file[1].st_mtime)
        self.tracked_files = [file[0] for file in file_stats]
