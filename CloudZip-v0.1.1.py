#alle modules
import webbrowser

import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

from pathlib import Path
import zipfile
import os

import json
import requests

import datetime
import pyperclip

#open configuration API-token google drive
url = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&access_type=offline&flowName=GeneralOAuthFlow'
firefox = webbrowser.Mozilla(r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe')
firefox.open(url)

#input token
application_window = tk.Tk()

token = simpledialog.askstring("Token", "Token:", parent=application_window)

#save file for token
x = datetime.datetime.now()

pyperclip.copy('{}'.format(token))
token = pyperclip.paste()

f = open('Token', 'w')
f.write('{}\n{}'.format(token, x))

#open explorertab
exp = tk.Tk()
exp.withdraw()

file_path = filedialog.askdirectory()

#change the path for filecompression(= path where the zip file will be made)
os.chdir(file_path)

#make a zip file from the whole directory
def _walk(path: Path) -> []:
    all_files = []
    for x in path.iterdir():
        if x.is_dir():
            all_files.extend(_walk(x))
        else:
            all_files.append(x)
    return all_files

top = file_path
exclude = set(['myzipfile.zip'])
for root, dirs, files in os.walk(top, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]

def zip_files(path: Path, archive_name: str):
    all_files = _walk(path)
    with zipfile.ZipFile(f'{archive_name}', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in all_files:
            zipf.write(f)
        zipf.close()


def zip_this_folder():
    print('compressing...')
    zip_files(Path.cwd(), 'myzipfile.zip')
    print('...compression done!')
    

if __name__ == "__main__":
    zip_this_folder()

#upload zip file to GoogleDrive
headers = {"Authorization": "Bearer {}".format(token)}
para = {
    "name": "myzipfile.zip"
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open("./myzipfile.zip", "rb")
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)

print(r.text)