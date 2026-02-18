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
    #Gets a list of Team keys that competed in the given event.
    team_keys = load_data(api_key, f"/event/{event_key}/teams")
    OPRS = load_data(api_key, f"/event/{event_key}/oprs")["oprs"]
    rankings = load_data(api_key, f"/event/{event_key}/rankings")

    data = {
        "team_keys": team_keys,
        "OPRS": OPRS,
        "rankings": rankings,

    }
    save_to_json(data, event_key)
    return data


def data_exists(event_key):
    path = Path(f"data/{event_key}.json")
    return path.exists()


#Always use this, it checks if exist, else loads it.
def fetch_data(api_key, event_key):
    path = Path(f"data/{event_key}.json")
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    else:
        return load_all_data(api_key, event_key)


def save_to_json(data, event_key):
    Path("data").mkdir(exist_ok=True)
    with open(f"data/{event_key}.json", "w") as f:
        json.dump(data, f, indent=2)


def reload_data(api_key, event_key):
    load_all_data(api_key, event_key)