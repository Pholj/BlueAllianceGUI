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

        #Team info entry and button
        self.teamInfo = tk.Entry(self)
        self.teamInfo.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.teamButton = tk.Button(self, text="Get Team Info, put in number only above", command=self.on_team_click)
        self.teamButton.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        #Compare Bots
        self.compareLabel = tk.Label(self, text="Compare Bots (e.g. 1014, 254)")
        self.compareLabel.grid(row=4, column=0, padx=10, pady=(10,0), sticky="nsew")
        self.compareEntry = tk.Entry(self)
        self.compareEntry.grid(row=5, column=0, padx=10, pady=2, sticky="nsew")
        self.compareButton = tk.Button(self, text="Compare", command=self.on_compare_click)
        self.compareButton.grid(row=6, column=0, padx=10, pady=2, sticky="nsew")

        #Compare Alliances
        self.allianceLabel = tk.Label(self, text="Compare Alliances (3 teams each, e.g. 1014,254,118)")
        self.allianceLabel.grid(row=7, column=0, padx=10, pady=(10,0), sticky="nsew")
        self.allianceEntry1 = tk.Entry(self)
        self.allianceEntry1.grid(row=8, column=0, padx=10, pady=2, sticky="nsew")
        self.allianceEntry2 = tk.Entry(self)
        self.allianceEntry2.grid(row=9, column=0, padx=10, pady=2, sticky="nsew")
        self.allianceButton = tk.Button(self, text="Compare Alliances", command=self.on_alliance_click)
        self.allianceButton.grid(row=10, column=0, padx=10, pady=2, sticky="nsew")

        #TODO then add a refresh button that calls self.refresh later

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

    def on_compare_click(self):
        raw = self.compareEntry.get()
        teams = ["frc" + t.strip() for t in raw.split(",")]
        if len(teams) != 2:
            messagebox.showerror("Error", "Enter exactly 2 team numbers separated by a comma")
            return
        CompareBots(self, self.controller, teams[0], teams[1], self.data)

    def on_alliance_click(self):
        alliance1 = ["frc" + t.strip() for t in self.allianceEntry1.get().split(",")]
        alliance2 = ["frc" + t.strip() for t in self.allianceEntry2.get().split(",")]
        if len(alliance1) != 3 or len(alliance2) != 3:
            messagebox.showerror("Error", "Each alliance needs exactly 3 teams")
            return
        CompareAlliances(self, self.controller, alliance1, alliance2, self.data)

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

    
class CompareBots(tk.Toplevel):
    def __init__(self, master, controller, team1_key, team2_key, data):
        super().__init__(master)
        self.title(f"Compare {team1_key} vs {team2_key}")
        self.minsize(700, 400)

        team1 = next((t for t in data["team_keys"] if t["key"] == team1_key), None)
        team2 = next((t for t in data["team_keys"] if t["key"] == team2_key), None)

        opr1 = data["OPRS"].get(team1_key, 0)
        opr2 = data["OPRS"].get(team2_key, 0)
        predicted_winner = team1_key if opr1 > opr2 else team2_key

        # Header
        tk.Label(self, text=f"{team1_key} vs {team2_key}", font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, columnspan=3, pady=10)

        # Column headers
        tk.Label(self, text=team1_key, font=("Helvetica", 11, "bold"), fg="red").grid(row=1, column=0, padx=20)
        tk.Label(self, text="Field", font=("Helvetica", 11, "bold")).grid(row=1, column=1)
        tk.Label(self, text=team2_key, font=("Helvetica", 11, "bold"), fg="blue").grid(row=1, column=2, padx=20)

        fields = [
            ("Nickname",    team1["nickname"]    if team1 else "?",  team2["nickname"]    if team2 else "?"),
            ("City",        team1["city"]        if team1 else "?",  team2["city"]        if team2 else "?"),
            ("Rookie Year", team1["rookie_year"] if team1 else "?",  team2["rookie_year"] if team2 else "?"),
            ("OPR",         f"{opr1:.2f}",                           f"{opr2:.2f}"),
        ]

        for i, (field, val1, val2) in enumerate(fields, start=2):
            tk.Label(self, text=str(val1) or "N/A").grid(row=i, column=0, padx=20, pady=4)
            tk.Label(self, text=field, font=("Helvetica", 9, "bold")).grid(row=i, column=1)
            tk.Label(self, text=str(val2) or "N/A").grid(row=i, column=2, padx=20, pady=4)

        ttk.Separator(self, orient="horizontal").grid(row=99, column=0, columnspan=3, sticky="ew", pady=8)

        tk.Label(self, text=f"Predicted Winner: {predicted_winner}",
                 font=("Helvetica", 13, "bold"), fg="green").grid(row=100, column=0, columnspan=3, pady=6)

        tk.Button(self, text="Close", command=self.destroy).grid(row=101, column=0, columnspan=3, pady=8)

class CompareAlliances(tk.Toplevel):
    def __init__(self, master, controller, alliance1, alliance2, data):
        super().__init__(master)
        self.title("Alliance Comparison")
        self.minsize(800, 500)

        def get_team(key):
            return next((t for t in data["team_keys"] if t["key"] == key), None)

        def get_opr(key):
            return data["OPRS"].get(key, 0)

        opr1_total = sum(get_opr(t) for t in alliance1)
        opr2_total = sum(get_opr(t) for t in alliance2)
        predicted_winner = "Alliance 1" if opr1_total > opr2_total else "Alliance 2"

        # Header
        tk.Label(self, text="Alliance Comparison", font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, columnspan=3, pady=10)

        tk.Label(self, text="Alliance 1", font=("Helvetica", 12, "bold"), fg="red").grid(row=1, column=0, padx=30)
        tk.Label(self, text="Alliance 2", font=("Helvetica", 12, "bold"), fg="blue").grid(row=1, column=2, padx=30)

        # Per-team rows
        for i, (t1, t2) in enumerate(zip(alliance1, alliance2)):
            team1 = get_team(t1)
            team2 = get_team(t2)
            opr1  = get_opr(t1)
            opr2  = get_opr(t2)

            nick1 = team1["nickname"] if team1 else t1
            nick2 = team2["nickname"] if team2 else t2

            tk.Label(self, text=f"{t1}\n{nick1}\nOPR: {opr1:.2f}",
                     justify="center").grid(row=2+i, column=0, padx=20, pady=6)
            tk.Label(self, text=f"Bot {i+1}", font=("Helvetica", 9, "bold")).grid(row=2+i, column=1)
            tk.Label(self, text=f"{t2}\n{nick2}\nOPR: {opr2:.2f}",
                     justify="center").grid(row=2+i, column=2, padx=20, pady=6)

        # Totals
        ttk.Separator(self, orient="horizontal").grid(row=5, column=0, columnspan=3, sticky="ew", pady=8)
        tk.Label(self, text=f"Total OPR: {opr1_total:.2f}", font=("Helvetica", 11, "bold"), fg="red").grid(row=6, column=0)
        tk.Label(self, text="Total OPR", font=("Helvetica", 9, "bold")).grid(row=6, column=1)
        tk.Label(self, text=f"Total OPR: {opr2_total:.2f}", font=("Helvetica", 11, "bold"), fg="aqua").grid(row=6, column=2)

        ttk.Separator(self, orient="horizontal").grid(row=7, column=0, columnspan=3, sticky="ew", pady=8)
        tk.Label(self, text=f"Predicted Winner: {predicted_winner}",
                 font=("Helvetica", 13, "bold"), fg="green").grid(row=8, column=0, columnspan=3)

        tk.Button(self, text="Close", command=self.destroy).grid(row=9, column=0, columnspan=3, pady=10) 