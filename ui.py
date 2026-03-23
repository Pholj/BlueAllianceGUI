import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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

        if hasattr(frame, "refresh"):
            frame.refresh()


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
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.treeView = ttk.Treeview(self, show="headings")
        self.treeView.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.teamInfo = tk.Entry(self)
        self.teamInfo.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.teamButton = tk.Button(self, text="Get Team Info, put in number only above", command=self.on_team_click)
        self.teamButton.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        #then add a refresh button that calls self.refresh

    def refresh(self):
        self.data = fetch_data(self.controller.API_KEY, self.controller.event_key)
        self.treeView["columns"] = ("0", "1", "2")
        self.treeView.heading("0", text="Ranking")
        self.treeView.heading("1", text ="TeamName")
        self.treeView.heading("2", text ="OPR")

        #sorts by OPR I have no clue how that works but it works.
        OPR_data = self.data["OPRS"]
        OPR_data = dict(sorted(OPR_data.items(), key=lambda item: item[1], reverse=True))
        rank_lookup = {
            team["team_key"]: team["rank"]
            for team in self.data["rankings"]["rankings"]
        }
        for team in OPR_data:
            self.treeView.insert("", "end", values=(rank_lookup[team],
                                                    team, OPR_data[team]))
            
    def on_team_click(self):
        team = "frc" + str(self.teamInfo.get())
        TeamInfo(self, self.controller, team, self.data)

class TeamInfo(tk.Toplevel):
    def __init__(self, master, controller, team_key, data):
        super().__init__(master)
        self.controller = controller
        self.team_key = team_key
        self.data = data
        self.title(f"Team {team_key} Info")
        team = next((t for t in self.data["team_keys"] if t["key"] == team_key), None)
        if team:
            fields = [
                ("Nickname", team["nickname"]),
                ("Location", f"{team['city']}, {team['state_prov']}"),
                ("Rookie Year", team["rookie_year"]),
                ("School", team["school_name"]),
                ("Website", team["website"]),
            ]
            for label, value in fields:
                row = tk.Frame(self)
                row.pack(fill="x", padx=16, pady=2)
                tk.Label(row, text=f"{label}:", font=("Helvetica", 9, "bold"), width=12, anchor="w").pack(side="left")
                tk.Label(row, text=value or "N/A", anchor="w").pack(side="left")

    
