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
from ttkbootstrap.scrolled import ScrolledFrame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class Fixture:
    def __init__(self, root):
        self.JSON_FILE = os.path.join(BASE_DIR, "Fixture.json")
        self.standard_path =r"E:\standard routine"

        self.autofix=  self.load_json()
        self.all_keys = sorted(set(list(self.autofix.keys())))
        #print(self.all_keys)

        self.root = root
        self.root.title("ATE Fixture")
        self.window_width=450
        self.window_height=320
        # Get the screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Calculate the position for centering
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)

        # Set the geometry with position
        root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        root.resizable(False,False)


        self.GUI()
    def GUI(self):
        self.style = tb.Style()     
        self.custom_font = tkfont.Font(family= "Segoe UI", size=16, weight="bold")  #for label frame
        self.custom_font2 = tkfont.Font(family= "Segoe UI", size=14, weight="bold") #for label
        self.custom_font3 = tkfont.Font(family= "Segoe UI", size=12, weight="bold")  # for button
        self.custom_font4 = tkfont.Font(family= "Segoe UI", size=11, weight="bold")
        self.custom_font5 = tkfont.Font(family= "Segoe UI", size=10, weight="bold")
        
        self.style.configure("TLabelframe.Label", font= self.custom_font)
        self.style.configure("TLabel", font= self.custom_font2)
        self.style.configure("TButton", font= self.custom_font3) 

        self.mainFrame = tb.LabelFrame(self.root, text= r'Search ATE Fixture', padding=10, bootstyle="success")
        self.mainFrame.pack(fill="x", padx=10, pady=5,expand=True)

        '''self.searchEntry = tb.Entry(self.mainFrame,  font=self.custom_font5)
        self.searchEntry.grid(row=0, column=0, padx=10, pady=10,sticky="nsew")'''

        self.searchEntry = AutocompleteEntry(self.mainFrame, self.all_keys,placeholder="Enter or Scan Project/Part #", font=self.custom_font4)
        self.searchEntry.grid(row=0, column=0, padx=10, pady=10,sticky="ew")

        self.searchButton =  tb.Button(self.mainFrame, text="Submit", width=15, bootstyle= "outline-warning", command=self.search_fix)
        self.searchButton.grid(row=1, column=0, padx=10, pady=10,sticky="nsew")
        self.searchButton =  tb.Button(self.mainFrame, text="Refresh", width=15, bootstyle= "outline-success", command=self.refresh)
        self.searchButton.grid(row=2, column=0, padx=10, pady=10,sticky="nsew")

        self.projLabel =  tb.Label(self.mainFrame, text="") 
        self.projLabel.grid(row=3, column=0, padx=10, pady=5,sticky="nsew")
        self.fixLabel =  tb.Label(self.mainFrame, text="")
        self.fixLabel.grid(row=4, column=0, padx=10, pady=5,sticky="nsew")

        #self.projLabel.config(text='Peoj#: CCT-19006-01')
        #self.fixLabel.config(text='Fixture #: CC1')

        self.mainFrame.columnconfigure((0), weight=1)


    def search_fix(self):
        enteredProj = self.searchEntry.get()
        if not enteredProj or enteredProj=="Enter or Scan Project/Part #":
                messagebox.showerror("Error", "Entry cannot be empty.")
                return
        
       # print(enteredProj)
        self.json_fix = self.load_json()
        #print(json_fix)

        for key, value in self.json_fix.items():
            if enteredProj in key:
                self.fixLabel.config(text=f'ATE Fixture #: {value}')
                self.projLabel.config(text=f'Proj#: {enteredProj.upper()}')
                self.searchEntry.delete(0, "end")
                break
            else:
                self.fixLabel.config(text=f'ATE Fixture #: Not Found')
                self.projLabel.config(text=f'Proj#: {enteredProj.upper()}')
                self.searchEntry.delete(0, "end")
                
    def  refresh(self):
        if os.path.exists(self.standard_path):
            proj= list(os.listdir(self.standard_path))
            #print(proj) # list files inside
        else:
            messagebox.showerror("Error", "Entry cannot be empty.")

        json_fix = self.load_json()   # load json file
        json_list=[]
        json_list= list(json_fix.keys())
        #print(json_list)

        self.difference= list(set(proj)-set(json_list))
        if self.difference ==[]:
            messagebox.showinfo("Update Status", "All entries are up to date")
        else:
            self.updatefixture()
            

    def updatefixture(self):
        if hasattr(self, "top") and self.top.winfo_exists():
            self.top.focus()
            self.top.lift()
            return
        self.top = tb.Toplevel(self.root)  # ttkbootstrap top-level
        self.top.title("Update Window")
        self.window_width=400
        self.window_height=400
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)
        self.top.geometry(f"{self.window_width}x{self.window_height}+{x+450}+{y-10}")

        tb.Label(self.top, text="Enter Fixture Number",
                 font=("Segoe UI", 14, "bold")).pack(pady=10)
        self.entry_widgets = {}
        # Scrollable frame
        sf = ScrolledFrame(self.top, autohide=True)
        sf.pack(fill="both", expand=True,padx=10, pady=10)

        container = sf
        container.columnconfigure((0,1), weight=1)
        for i ,item in enumerate(self.difference):
            row = tb.Frame(container)
            row.grid(row=i, column= 0,sticky="ew", pady=0)
            row.columnconfigure(1, weight=1)
            # label (column 0)
            tb.Label(row, text=item,  font=("Segoe UI", 12, "bold"), anchor="w").grid(
                row=0, column=0, padx=10, sticky="w", pady=5
            )
            # entry (column 1)
            entry = tb.Entry(row, font=self.custom_font5)
            entry.grid(row=0, column=1, padx=10,pady=5, sticky="e")
            self.entry_widgets[item] = entry

        saveb= tb.Button(self.top, text="Save", command=self.save_values, bootstyle= "outline-success", )
        saveb.pack(fill="x", padx=20, pady=10)

        quitb= tb.Button(self.top, text="Exit", command=self.exit, bootstyle= "outline-warning", )
        quitb.pack(fill="x", padx=20, pady=10)

    def exit(self):
        self.top.destroy()

    def save_values(self):
        new_data = {}
        for key, entry in self.entry_widgets.items():
            value = entry.get()
            if value:
                new_data[key] = value

        if not new_data:
            messagebox.showwarning("Warning", "No fixture numbers entered.")
            return

        entries_text = "\n".join([f"{key} : {value}" for key, value in new_data.items()])
        confirm = messagebox.askyesno("Confirm Save",
                f"Do you want to save:\n{entries_text}?")
        if not confirm:
            return
                
        existing_data=self.load_json()   
        existing_data.update(new_data)      
        with open(self.JSON_FILE, "w") as f:
                    json.dump(existing_data, f, indent=4)

        self.autofix = self.load_json()
        self.all_keys = sorted(self.autofix.keys())
        self.searchEntry.suggestion_list = self.all_keys
        self.top.destroy()
        messagebox.showinfo("Success", "Fixture file updated successfully") 
        self.refresh()
        


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
            self.delete(0, tk.END)
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


