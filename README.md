# SSH File Vault

A very simple Python project, which allows you to encrypt and safely store your files on a remote machine through SSH. You are then able to download and decrypt these files, whenever needed.


## Getting started
_Follow these steps to setup this project on your machine._

1. Clone this repository:
```sh
git clone https://github.com/Kshitij-Jande/ssh-file-vault.git
```
2. Navigate to the cloned directory:
```sh
cd ssh-file-vault
```
3. Install the required modules:
```sh
pip install -r requirements.txt
```
4. Open `config.json` file under the `config` folder, and put in the necessary information:
    - `remote_vault_folder_path`: Path to a folder on your remote server. Make sure this folder exists before you upload. Don't forget to add a `/` at the end (e.g. `/home/ubuntu/Uploads/`).
    - `private_key_path`: Path to your private key, which you use for SSH connection to your server.
    - `private_key_passphrase`: Your private key's passphrase. Leave this blank if you haven't set one.
    - `host_ip`: The IP address of your remote server.
    - `host_port`: The SSH port number of your remote server. Default value is 22.
    - `host_user`: The user to log into.
5. You can also configure through commands, like this:
    - `py main.py sethost 127.0.0.1`
    - `py main.py setkey C:\Users\(user)\.ssh\id_rsa`


## How it works
__The flow of this program is quite straightforward.__

- You configure details, such as your private key, host information, etc.
- When you wish to upload a file to the server:
    1. **File encryption**:
        1. A new Fernet key is generated, if one doesn't exist.
        2. This key is stored as `secret.key` under the `secret` folder.
        3. The file is encrypted using Fernet and the secret key from last step.
        4. This encrypted file is given a unique name and temporarily stored in `temp` folder.
    2. **File upload**:
        1. The encrypted file is accessed from the `temp` folder.
        2. An SSH connection is established with the server, using your private key.
        3. The file is transfered to the remote directory using SFTP.
        4. Once the transfer is completed, the temporary file is deleted from the `temp` folder.
    3. **File tracking**:
        1. Each file has details such as its original file name, upload timestamp, encrypted file name and its hash
        2. This information is used to download a file or get its information.
        3. All information is stored in `storage.json` under the `config` folder.
- When you wish to download a file from the server:
    1. **File download**:
        1. An SSH connection is established with the server, using your private key.
        2. Using SFTP, the program checks whether or not the file was actually uploaded to the server.
        3. The encrypted file is downloaded from the remote folder.
        4. This file is temporarily stored in the `temp` folder.
    2. **File decryption**:
        1. From `temp` folder, the encrypted file is accessed.
        2. A hash (SHA256) comparison is done to check the integrity of the file.
        3. If the hashes do not match, the user is notified.
        2. The key `secret.key` stored inside the `secret` folder is accessed.
        3. The encrypted file is decrypted using Fernet and the secret key from last step.
        4. The encrypted file is then deleted from the `temp` folder.


## Wishlist
_These are a few enhancements that I wish to make in the future._

- **Good error handling**: There isn't any type of error handling mechanism right now, which makes the program less user-friendly.
- **File handling**: Currently, only one file can be uploaded at a time and directories are not supported.
- **File metadata storage**: The exact file metadata isn't obtained after downloading a file, which means that integrity is broken.
- **CRUD**: Some options are missing (such as delete and update), while the other options aren't quite flexible (such as read and create).
- **Organize and optimize**: This program isn't quite organized and optimized. A lot of things could be improved in terms of optimization.
- **User-friendly and interactive**: A lot of things could be made more interactive (e.g. adding a file upload/download progress bar).


## Contributing
_Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**._

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
If you like this project, you can give it a star. Thanks.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature`)
3. Commit your Changes (`git commit -m 'Add some feature'`)
4. Push to the Branch (`git push origin feature`)
5. Open a Pull Request


## License
_Distributed under the MIT License. See `LICENSE` for more information._


## Acknowledgements
_Resources, libraries and material I used to craft this project._

- [Mokgadi's blog on Paramiko module](https://medium.com/@keagileageek/paramiko-how-to-ssh-and-file-transfers-with-python-75766179de73)
- [Cryptography library for Fernet encryption and decryption](https://github.com/pyca/cryptography)
- [Paramiko library for SFTP via. SSH](https://github.com/paramiko/paramiko)