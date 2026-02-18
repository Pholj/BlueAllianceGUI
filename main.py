from load_data import load_all_data, save_to_json
from ui import FRCGUI


def main():
    API_KEY = ""
    #last years event key: 2025mosl

    #Runs the GUI
    root = FRCGUI(API_KEY)
    root.mainloop()

main()