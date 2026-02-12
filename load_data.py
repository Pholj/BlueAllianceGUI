import requests
import json
from pathlib import Path

def load_data(api_key, endpoint):
    baseURL = "https://www.thebluealliance.com/api/v3"
    headers = {
        'X-TBA-Auth-Key': api_key
    }
    response = requests.get(baseURL + endpoint, headers=headers)
    #200 is good
    if response.status_code == 200:
        #Returns the json as a list
        return response.json()
    else:
        response.raise_for_status()

def load_all_data(api_key, event_key):
    #decide what you need to do

    #Gets a list of Team keys that competed in the given event.
    team_keys = load_data(api_key, f"/event/{event_key}/teams")
    OPRS = load_data(api_key, f"/event/{event_key}/oprs")["oprs"]

    save_to_json(OPRS, event_key)
    return OPRS

def fetch_data():
    path = Path("data/2025mosl.json")


def save_to_json(data, event_key):
    Path("data").mkdir(exist_ok=True)
    with open(f"data/{event_key}.json", "w") as f:
        json.dump(data, f, indent=2)