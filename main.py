from load_data import load_all_data, save_to_json
from ui import FRCGUI


def main():
    #PUT IN YOUR API KEY HERE
    API_KEY = ""

    #Runs the GUI
    root = FRCGUI(API_KEY)
    root.mainloop()

if __name__ == "__main__":
    main()