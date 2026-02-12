from load_data import load_all_data, save_to_json

def main():
    #Get event name and store that event
    API_KEY = ""
    event = "2025mosl"
    print("hi")
    print(load_all_data(API_KEY, event))

main()