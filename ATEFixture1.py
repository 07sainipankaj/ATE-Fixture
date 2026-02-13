import ttkbootstrap as tb
import tkinter as tk
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
         
        self.autofix=  self.load_fix()
        self.all_keys = sorted(set(list(self.autofix.keys())))
        print(self.all_keys)

        self.root = root
        self.root.title("ATE Fixture")
        self.window_width= 350
        self.window_height=260
        # Get the screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Calculate the position for centering
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)

        # Set the geometry with position
        root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")


         
        self.GUI()
    def load_fix(self):
        reverse_map = {}
        if os.path.exists(self.JSON_FILE):
            try:
                with open(self.JSON_FILE, "r") as f:
                    raw_fix = json.load(f)
                    for key, values in raw_fix.items():
                        for value in values:
                            reverse_map[value]=key
                            #print(reverse_map)
                        
            except json.JSONDecodeError:
                    messagebox.showerror("Error", "file is corrupted.")
            return reverse_map


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
        self.Label.grid(row=0, column=0, padx=50, pady=10, sticky="ew")

        self.searchEntry = AutocompleteEntry(self.root, self.all_keys,placeholder="for ex. 9006", font=self.custom_font4)
        self.searchEntry.grid(row=1, column=0, padx=50, pady=10,sticky="ew")

        #self.searchentry = tb.Entry(self.root,font=self.custom_font4)
        #self.searchentry.grid(row=1, column=0, padx=100, pady=10, sticky="ew")

        self.search = tb.Button(self.root,width=24, text="Submit", command=self.submit)
        self.search.grid(row=2, column=0, padx=50, pady=10, sticky="ew")

        self.Label1 = tb.Label(self.root, text="")
        self.Label1.grid(row=3, column=0, padx=50, pady=10, sticky="ew")

    def submit(self):
        fix_to_search= self.searchEntry.get().lower()
        #print(fix_to_search)
        fixtures= self.load_json()
        #print(fixtures)

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
    



class AutocompleteEntry(tb.Entry):
    def __init__(self, master, suggestion_list, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.suggestion_list = suggestion_list
        self.placeholder = placeholder
        self.placeholder_color = "grey"
        self.default_fg_color = self.cget("foreground")
        self.listbox= None
        self.current_matches=[]
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._show_placeholder)

        # Insert placeholder initially
        self._show_placeholder()

        self.bind("<KeyRelease>", self.on_keyrelease)
        self.bind("<Down>", self.focus_listbox)
        self.bind("<Return>", self.on_return)

    def on_keyrelease(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return
        
        typed = self.get().lower() #getting valeu form entry
        self.current_matches = [word for word in self.suggestion_list if typed in word.lower()]
    

        if not typed or not self.current_matches:
            self.hide_listbox()
            return
        self.show_listbox()
        
    def show_listbox(self):
        if self.listbox:
            self.listbox.destroy()
        root = self.winfo_toplevel()

        self.listbox = tk.Listbox(root, height=min(6, len(self.current_matches)), 
                                  font=("Segoe UI", 10),
                                  bg="#1f1f1f", fg="#00ffff", 
                                  highlightbackground="#00ffff", 
                                  selectbackground="#005f5f")
        
        for word in self.current_matches:
            self.listbox.insert(tk.END, word)
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()

        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()

        # Position relative to root window:
        rel_x = x - root_x
        rel_y = y - root_y

       # print(f"Placing listbox at relative coords: {rel_x}, {rel_y}"
        self.listbox.place(x=rel_x, y=rel_y, width=self.winfo_width())
        self.listbox.lift()
       # print("Showing listbox with matches:", self.current_matches)
        self.listbox.bind("<ButtonRelease-1>", self.on_listbox_click)
        self.listbox.bind("<Up>", self.on_listbox_updown)
        self.listbox.bind("<Down>", self.on_listbox_updown)
        self.listbox.bind("<Return>", self.on_listbox_enter)

    def on_listbox_click(self,event):
        self.select_current_listbox_item()
        return "break"

    def on_listbox_enter(self,event):
        self.select_current_listbox_item()
        return "break"


    def select_current_listbox_item(self):
        if self.listbox and self.listbox.curselection():
            selection = self.listbox.get(self.listbox.curselection())
            self.delete(0, tb.END)
            self.insert(0, selection)
            self.hide_listbox()
            self.focus_set()

    def focus_listbox(self, event):
        if self.listbox:
            self.listbox.focus_set()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return "break"

    def on_return(self, event):
        if self.listbox and self.listbox.curselection():
            self.hide_listbox()  # Hide the list even if not selecting
            self.focus_set()
            self.select_current_listbox_item()
        else:
            self.hide_listbox()  # Hide the list even if not selecting
            self.focus_set()     # Keep focus on Entry
        return "break"
    
    
    def on_listbox_updown(self, event):
        cur = self.listbox.curselection()
        if not cur:
            index= 0
        else:
            index= cur[0]
            if event.keysym=="Up" and index>0:
                index-=1
            elif event.keysym =="Down" and index <self.listbox.size() - 1:
                index+=1
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)
        self.listbox.activate(index)
        return "break"
    
    def hide_listbox(self):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None
            
    def _show_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(foreground=self.placeholder_color)

    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(foreground=self.default_fg_color)










if __name__=="__main__":
    root = tb.Window(themename="darkly")
   
    app= Fixture(root)
    root.mainloop()

