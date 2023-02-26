import os
import paramiko


class Mover:
    def __init__(self, host, user, key, passphrase):
        self.host = host
        self.user = user
        self.key = key
        self.passphrase = passphrase

    def upload(self, file, server_file_path):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # for unknown host key(s), don't remove this line
        ssh.connect(self.host, username=self.user,
                    key_filename=self.key, passphrase=self.passphrase)
        sftp = ssh.open_sftp()
        path = "temp" + os.sep + file
        # print(os.getcwd())
        sftp.put(path, server_file_path + file)
        sftp.close()
        ssh.close()
        os.remove("temp" + os.sep + file)

    def download(self, server_file_path, file):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # don't remove this line
        ssh.connect(self.host, username=self.user,
                    key_filename=self.key, passphrase=self.passphrase)
        sftp = ssh.open_sftp()
        sftp.get(server_file_path, "temp" + os.sep + file)
        sftp.close()
        ssh.close()
