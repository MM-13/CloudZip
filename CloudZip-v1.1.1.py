#alle modules
import webbrowser

import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

import os

import json
import requests

import datetime
import pyperclip

import shutil

import time

#open configuration API-token google drive
url = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&access_type=offline&flowName=GeneralOAuthFlow'
firefox = webbrowser.Mozilla(r'C:\Program Files\Mozilla Firefox\firefox.exe')
firefox.open(url)

#input token
application_window = tk.Tk()

token = simpledialog.askstring("Token", "Token:", parent=application_window)

#save file for token
ti = datetime.datetime.now()

pyperclip.copy('{}'.format(token))
token = pyperclip.paste()

t = open('Token.txt', 'w')
t.write('{}\n{}'.format(token, ti))
t.close()

#open explorertab
exp = tk.Tk()
exp.withdraw()

file_path = filedialog.askdirectory()

#change the path for filecompression(= path where the zip file will be made)
os.chdir(file_path)

#make zip file
shutil.make_archive('CloudZip', 'zip', '{}'.format(file_path))

#upload zip file to GoogleDrive
headers = {"Authorization": "Bearer {}".format(token)}
print('- File compressed!')
print('\n- uploading...')

para = {
    "name": "CloudZip.zip"}

files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open("./CloudZip.zip", "rb")}

r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files)

print(r.text)
print('\n- File uploaded!')

#deleting file
files['file'].close()
os.remove('CloudZip.zip')
print('\n- File deleted!')

time.sleep(2)