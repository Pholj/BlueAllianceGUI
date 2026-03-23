from load_data import load_all_data, save_to_json
from ui import FRCGUI


def main():
    #PUT IN YOUR API KEY HERE
    #heres mine it gen don't matter but in good concious use yours maybe idk!
    #API_KEY = "4rXpqraPjCb0brzrrSRzqqDhXuHn1lr8cMhP33iEtpiu06xVQwoNm3yQe1PW5pm8"
    API_KEY = "4rXpqraPjCb0brzrrSRzqqDhXuHn1lr8cMhP33iEtpiu06xVQwoNm3yQe1PW5pm8"

    #Runs the GUI
    root = FRCGUI(API_KEY)
    root.mainloop()

if __name__ == "__main__":
    main()