import json
import hashlib
import os
from datetime import datetime as dt


class Tracker:
    def __init__(self, original):
        self.original_file_name = original
        self.temp_folder = "temp"
        self.file_info = None

    def set_encrypted_file(self, path):
        self.encrypted_file_name = path
        self.file_info = {
            "original_file_name": self.original_file_name,
            "date_uploaded": self.current_timestamp(),
            "remote_file_name": path,
            "sha256": self.calculate_hash()
        }

    def calculate_hash(self):
        return hashlib.sha256(
            (self.temp_folder + os.sep + self.encrypted_file_name).encode('UTF-8')).hexdigest()

    def current_timestamp(self):
        return round(dt.now().timestamp())

    def save(self):
        try:
            with open("config" + os.sep + "storage.json", "r") as s:
                storage_data = json.load(s)
        except:
            storage_data = []

        storage_data.append(self.file_info)

        with open("config" + os.sep + "storage.json", "w") as storage_file:
            json.dump(storage_data, storage_file, indent=4)

    def exists(self):
        try:
            with open("config" + os.sep + "storage.json", "r") as s:
                storage_data = json.load(s)
        except:
            storage_data = []

        # print(storage_data)

        if len(storage_data) == 0:
            return False

        for file_info in storage_data:
            if file_info.get('original_file_name') == self.original_file_name:
                self.file_info = file_info
                return True
        return False

    def get_info(self):
        if self.exists() or self.file_info != None:
            return self.file_info
        return {}
