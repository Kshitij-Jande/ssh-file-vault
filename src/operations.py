import os
import uuid
from cryptography.fernet import Fernet


class Operations:
    def __init__(self, key_path):
        self.key = None
        self.key_path = key_path
        self.key_check()

    def key_check(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                self.key = f.read()
            return

        self.key = Fernet.generate_key()

        with open(self.key_path, "wb") as f:
            f.write(self.key)

    def encrypt_file(self, file):
        with open(file, "rb") as f:
            data = f.read()

        encrypted_data = Fernet(self.key).encrypt(data)
        random_file_name = str(uuid.uuid4())

        # with open(temp + os.sep + file_path + ".testing", "wb") as f:
        #     f.write(data)

        with open("temp" + os.sep + random_file_name, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        return random_file_name

    def decrypt_file(self, file, original):
        path = "temp" + os.sep + file

        with open(path, "rb") as f:
            data = f.read()

        decrypted = Fernet(self.key).decrypt(data)

        # with open(file, "wb") as f:
        #     f.write(data)

        with open("downloads" + os.sep + original, "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        os.remove(path)
