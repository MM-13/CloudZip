#alle modules
import webbrowser

import tkinter as tk
from tkinter import filedialog

from pathlib import Path
import zipfile
import os

import json
import requests

#Kies de naam van je Zipbestand
#naam = input('Geef je bestand een naam:'.zip)

#openen configuratie API-token google drive
url = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&access_type=offline&flowName=GeneralOAuthFlow'
firefox = webbrowser.Mozilla(r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe')
firefox.open(url)

#verkennertab openen
root = tk.Tk()
root.withdraw()

file_path = filedialog.askdirectory()

#pad voor bestanden compressen veranderen(= pad waar zipfile wordt gemaakt)
os.chdir(file_path)

#zipbestand maken van alle bestanden in dat pad
def _walk(path: Path) -> []:
    all_files = []
    for x in path.iterdir():
        if x.is_dir():
            all_files.extend(_walk(x))
        else:
            all_files.append(x)
    return all_files


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

#zipfile uploaden naar GoogleDrive
headers = {"Authorization": "Bearer ya29.a0ARrdaM8QtgvtoV8jfq7zm92OMO-lnP1J4kTfvKLb05xCI6el4cFAJJU8RYcufIKEql4f5Tkj2WCCuaTm5gkFwz0uwIfQXBW_o2KQ6AnV5Ij5kR95i9uPZGw_HDWKoKXBNMxB6s2K86dg9rVSz2UkOotONnBB"}
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