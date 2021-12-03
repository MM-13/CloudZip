import tkinter as tk
from tkinter import filedialog
import os

#Verkennertab openen
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
print(file_path)

#Pad voor bestanden compressen veranderen(= pad waar zipfile wordt gemaakt)
#os.chdir(file_path)

#Verwijderen bestand
os.remove(file_path)
print('Bestand verwijderd!')