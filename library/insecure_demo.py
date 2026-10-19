import subprocess


def jalankan(perintah):
    return subprocess.call(perintah, shell=True)
