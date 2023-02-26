import sys
import json
import os
import hashlib
from datetime import datetime
from mover import Mover
from operations import Operations
from tracker import Tracker


def file_config_check():
    with open("config" + os.sep + "config.json", "r") as f:
        config = json.load(f)
    if not config.get("private_key_path") or not config.get("host_ip"):
        return False
    return True


def set_config_value(key, value):
    with open("config" + os.sep + "config.json", "r") as f:
        config = json.load(f)
    config[key] = value
    with open("config" + os.sep + "config.json", "w") as f:
        json.dump(config, f, indent=4)


def get_config_value(key):
    with open("config" + os.sep + "config.json", "r") as f:
        return json.load(f).get(key)


def invalid_command_msg(error, example):
    print(error)
    print("Example:")
    print("    py main.py", example)


o = Operations("secret" + os.sep + "secret.key")
m = Mover(get_config_value("host_ip"), get_config_value("host_user"), get_config_value(
    "private_key_path"), get_config_value("private_key_passphrase"))


def upload_command(file):
    print("Encrypting your file...")
    encrypted_file_name = o.encrypt_file(file)
    print("File encrypted.")

    t = Tracker(file)
    t.set_encrypted_file(encrypted_file_name)

    print("Uploading your file...")
    m.upload(encrypted_file_name, get_config_value(
        "remote_vault_folder_path"))
    t.save()
    print("File uploaded successfully.")


def download_command(file):
    t = Tracker(file)

    if not t.exists():
        print("File not found in storage tracker. You haven't uploaded that file yet.")
        return

    info = t.get_info()
    encrypted_file_name = info.get("remote_file_name")

    print("Downloading your file...")
    m.download(get_config_value("remote_vault_folder_path") +
               encrypted_file_name, encrypted_file_name)
    print("File downloaded.")

    hash = hashlib.sha256(
        ("temp" + os.sep + encrypted_file_name).encode('UTF-8')).hexdigest()

    if hash != info.get('sha256'):
        print("Warning: Hashes do not match. File on remote server may be modified.")

    print("Decrypting your file...")
    o.decrypt_file(encrypted_file_name, file)
    print("File decrypted successfully. Please check the 'downloads' folder to access your file.")


def help_menu():
    print("""
SSH File Vault

This is a very simple program which allows you to encrypt and safely store your files on a remote machine through SSH.

Usage:
    py main.py (sub-command) (argument)

Sub-commands:
    help                    Shows this menu
    setkey (path-to-key)    Set a private key to authenticate with server
    setkeypass (passphrase) Set your private key's passphrase (if it has one)
    sethost (host-ip)       Set IP address of server to store files on
    setport (host-port)     Set the SSH port number of server (default 22)
    setuser (username)      Set a server user you wish to use
    upload (file-name)      Upload a file to the server
    download (file-name)    Download a file you uploaded to the server
    info (file-name)        Shows information of an uploaded file
    list                    Displays a list of files you uploaded

Note: You can manually configure this by editing the config.json file in config folder.

Examples:
    py main.py setkey C:\\Users\\(user)\\.ssh\\id_rsa
    py main.py upload some_file.zip
    py main.py download some_file.zip
    """)


if __name__ == "__main__":
    args = sys.argv[1:]
    valid_commands = ["help", "setkey", "setkeypass", "sethost",
                      "setport", "setuser", "upload", "download", "info", "list"]

    if len(args) == 0 or args[0] not in valid_commands or args[0] == "help":
        help_menu()
        exit()

    if not file_config_check():
        print("You've not configured yet. Please configure using sub-commands or open the config.json file in config folder to manually configure.")
        exit()

    if args[0] == "setkey":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide a valid path to your private key.", "setkey C:\\Users\\(user)\\.ssh\\id_rsa")
            exit()
        set_config_value("private_key_path", args[1])
        print("Successfully set the path to your private key.")
        exit()

    if args[0] == "setkeypass":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide a valid private key passphrase.", "setkeypass 1234")
            exit()
        set_config_value("private_key_passphrase", args[1])
        print("Successfully set your private key's passphrase.")
        exit()

    if args[0] == "sethost":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide a valid host address.", "sethost 127.0.0.1")
            exit()
        set_config_value("host_ip", args[1])
        print("Successfully set your host IP.")
        exit()

    if args[0] == "setport":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide a valid host port number.", "setport 22")
            exit()
        set_config_value("host_port", args[1])
        print("Successfully set your host port number.")
        exit()

    if args[0] == "setuser":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide a valid username, which exists on your server.", "setuser ubuntu")
            exit()
        set_config_value("host_user", args[1])
        print("Successfully set your username.")
        exit()

    if args[0] == "upload":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide path to the file you wish to upload.", "upload C:\\Path\\To\\File.zip")
            exit()
        upload_command(args[1])
        exit()

    if args[0] == "download":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide name of the file you wish to download. Use the 'list' sub-command to see a list of files you've uploaded.", "download File.zip")
            exit()
        download_command(args[1])
        exit()

    if args[0] == "info":
        if len(args) < 2:
            invalid_command_msg(
                "Please provide name of the file you need details of. Use the 'list' sub-command to see a list of files you've uploaded.", "info File.zip")
            exit()
        with open("config" + os.sep + "storage.json", "r") as f:
            config = json.load(f)
        for file in config:
            if file.get("original_file_name") == args[1]:
                print(f"Information for '{file.get('original_file_name')}':")
                print(
                    f"- Upload date & time: {datetime.fromtimestamp(file.get('date_uploaded'))}")
                print(f"- Encrypted file name: {file.get('remote_file_name')}")
                print(f"- Hash (SHA256): {file.get('sha256')}")
                exit()

        print("That file wasn't found. Please use the 'list' sub-command for a list of uploaded files.")
        exit()

    if args[0] == "list":
        with open("config" + os.sep + "storage.json", "r") as f:
            config = json.load(f)
        files = [file.get("original_file_name") for file in config]
        # for file in config:
        #     files.append(file.get("original_file_name"))
        print(f"There are {len(files)} file(s) on the server:")
        for f in files:
            print("-", f)
        print("\nPlease use the 'info' sub-command to see details of specific files.")
        exit()