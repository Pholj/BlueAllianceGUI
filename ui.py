import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import json
from load_data import fetch_data, reload_data, data_exists, save_to_json

class FRCGUI(tk.Tk):
    #Setting up the GUI, also in this case self=tk.Tk(), so self acts as a window
    def __init__(self, API_KEY):
        super().__init__()
        self.title("FRC Scouting GUI")
        self.minsize(1000, 600)
        self.maxsize(1000, 600)
        self.API_KEY = API_KEY
        self.frames = {}
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.event_key = None

        for Page in (GetEvent, MainMenu):
            frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        #Check if we have the event key stored, if so don't ask user for event
        if Path(f"data/event_key.json").exists():
            self.event_key = json.load(open(f"data/event_key.json", "r"))["event_key"]
            self.show_page(MainMenu)
        else:
            self.show_page(GetEvent)

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()


class GetEvent(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master
        #label is the text, entry is the box, button is the button
        self.label = tk.Label(self, text="Enter Event Key:")
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Submit", command=self.submit)

        #The scroll event list
        self.list_events = [
            "2024ohmv",
            "2025mosl",
            "2026ohmv"
        ]
        self.listbox = tk.Listbox(self)
        for event in self.list_events:
            self.listbox.insert(tk.END, event)

        #Layout of each item on the page
        #TODO: MAKE THIS PRETTY MANE!
        self.listbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.entry.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

    #A function for the button functionality
    def submit(self):
        event_key = self.entry.get()
        print(f"Event Key: {event_key}")

        #disable the button to prevent spammming
        self.button.config(state="disabled")
        self.button.update()
        try:
            fetch_data(self.controller.API_KEY, event_key)
            save_to_json({"event_key": event_key}, "event_key")
        except:
            messagebox.showerror("Event Load Failed", "Invalid event key.")
            self.button.config(state="normal")
            return
        self.controller.show_page(MainMenu)

class MainMenu(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.label = tk.Label(self, text="Main Menu")
        self.label.pack()
