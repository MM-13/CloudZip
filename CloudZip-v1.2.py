import webbrowser
import tkinter as tk
from tkinter import filedialog, simpledialog
import os
import json
import requests
import datetime
import pyperclip
import shutil
import time

# Open configuration API-token Google Drive
url = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&access_type=offline&flowName=GeneralOAuthFlow'
webbrowser.open(url)

# Input token
application_window = tk.Tk()
token = simpledialog.askstring("Token", "Token:", parent=application_window)

# Save file for token
ti = datetime.datetime.now()
pyperclip.copy(token)
token = pyperclip.paste()

with open('Token.txt', 'w') as t:
    t.write(f'{token}\n{ti}')

# Open explorer tab
exp = tk.Tk()
exp.withdraw()
file_path = filedialog.askdirectory()

# Define the name and path of the zip file
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
zip_filename = os.path.join(downloads_folder, 'CloudZip.zip')

# Make zip file
def zip_directory(path, zip_name):
    base_name = zip_name.split('.')[0]
    shutil.make_archive(base_name, 'zip', path)
    zip_path = f"{base_name}.zip"
    if os.path.exists(zip_path):
        shutil.move(zip_path, zip_name)

zip_directory(file_path, zip_filename)

# Upload zip file to Google Drive
headers = {"Authorization": f"Bearer {token}"}
print('- File compressed!')
print('\n- uploading...')

para = {"name": os.path.basename(zip_filename)}

files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open(zip_filename, "rb")
}

r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)

print(r.text)
print('\n- File uploaded!')

# Deleting file
files['file'].close()
os.remove(zip_filename)
print('\n- File deleted!')

time.sleep(2)
