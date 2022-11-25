import logging
import os
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

    async def sweep(self, items_to_keep: int = Config.max_stored_files):
        logging.info('Starting cleanup')
        deleted_files = 0
        self.file_list_lock.acquire()
        if len(self.tracked_files) > items_to_keep:
            deleted_files = len(self.tracked_files) - items_to_keep
            logging.debug('Cleaning %d files', deleted_files)
            for _ in range(len(self.tracked_files) - items_to_keep):
                processed_file = self.tracked_files.pop(0)
                logging.debug('deleting ' + str(processed_file))
                os.unlink(processed_file)
        self.file_list_lock.release()
        logging.info('Cleanup finished. Deleted %d files', deleted_files)

    def scan(self):
        logging.debug('Scanning %s for files to housekeep', Config.output_file_path)
        files = pathlib.Path(Config.output_file_path).glob('*.mp3')
        file_stats = sorted([(filename, filename.stat()) for filename in files], key=lambda file: file[1].st_mtime)
        self.tracked_files = [file[0] for file in file_stats]
        logging.debug('Found %d files to housekeep', len(self.tracked_files))
