import ttkbootstrap as tb
from tkinter import messagebox
import tkinter.font as tkfont
import os
from datetime import datetime
import json
from tkinter import messagebox
import sys 
from ttkbootstrap.constants import *
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class Fixture:
    def __init__(self, root):
        self.DATA_DIR = os.path.join(BASE_DIR, "data")
        self.JSON_FILE = os.path.join(self.DATA_DIR, "projects.json")
        self.root = root
        self.root.title("ATE Fixture")
        self.window_width= 450
        self.window_height=250
        # Get the screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Calculate the position for centering
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)

        # Set the geometry with position
        root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
         
        self.GUI()
    def GUI(self):

        self.style = tb.Style()     
        self.custom_font = tkfont.Font(family= "Segoe UI", size=16, weight="bold")  #for label frame
        self.custom_font2 = tkfont.Font(family= "Segoe UI", size=14, weight="bold") #for label
        self.custom_font3 = tkfont.Font(family= "Segoe UI", size=12, weight="bold")  # for button
        self.custom_font4 = tkfont.Font(family= "Segoe UI", size=11, weight="bold")
        
        self.style.configure("TLabelframe.Label", font= self.custom_font)
        self.style.configure("TLabel", font= self.custom_font2)
        self.style.configure("TButton", font= self.custom_font3)

        self.Label = tb.Label(self.root, text="Enter Project/Part Number")
        self.Label.grid(row=0, column=0, padx=100, pady=10, sticky="ew")

        self.entry = tb.Entry(self.root,font=self.custom_font4)
        self.entry.grid(row=1, column=0, padx=100, pady=10, sticky="ew")

        self.search = tb.Button(self.root,width=24, text="Submit", command=self.submit)
        self.search.grid(row=2, column=0, padx=100, pady=10, sticky="ew")

        self.Label1 = tb.Label(self.root, text="")
        self.Label1.grid(row=3, column=0, padx=100, pady=10, sticky="ew")

    def submit(self):
        fix_to_search= self.entry.get().lower()
        print(fix_to_search)
        fixtures= self.load_json()
        print(fixtures)

        for key,value in fixtures.items():
            if fix_to_search in value:
                self.Label1.config(text=f"Proj #: {fix_to_search}\nATE Fixture #: {key}")
                break
            else:
                self.Label1.config(text=f"Proj #: {fix_to_search}\nATE Fixture #: Not Found")


    
    def load_json(self):
        try:
            with open(self.JSON_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    














if __name__=="__main__":
    root = tb.Window(themename="darkly")
   
    app= Fixture(root)
    root.mainloop()

