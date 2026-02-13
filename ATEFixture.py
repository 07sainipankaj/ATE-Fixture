import tkinter as tk
import json
from tkinter import messagebox
from tkinter import *
import os
from tkinter import ttk
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
JSON_FILE = os.path.join(DATA_DIR, "projects.json")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as f:
        json.dump({}, f)   # empty json


def load_json():
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
fixture = load_json()


new_entry = {"1152 or 123": ["33333", "44444"]}

# Update existing data with new entry
fixture.update(new_entry)  # adds or replaces the key


with open(JSON_FILE, "w") as f:
    json.dump(fixture, f, indent=4)

fixture = load_json()

root = tk.Tk()
root.title("ATE Fixture")
root.geometry("400x220")
style = ttk.Style()

def submit():
    searchvalue= entry.get().lower()
    print(searchvalue.upper())
    fixture = load_json()
    

    for key, value in fixture.items():
       
        if searchvalue in value:
            label2.config(text=f"Proj:{searchvalue}\n\nATE Fixture#: {key}" )
            break
        else:
            label2.config(text="Not found")


label= tk.Label(root, text="Enter Poject/Part Number", font=("Arial", 12))
label.grid(row=0, column=0, padx=100, pady=10)

entry= tk.Entry(root, font=("Arial", 12))
entry.grid(row=1, column=0, padx=100, pady=10)

search= tk.Button(root, text= "Search",font=("Arial", 12), command=submit)
search.grid(row=2, column=0, padx=100, pady=10) 

label2= tk.Label(root, text="", font=("Arial", 12))
label2.grid(row=3, column=0, padx=100, pady=10)

root.mainloop()