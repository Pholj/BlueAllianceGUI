import requests

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

def load_all_data(api_key, event):
    #decide what you need to do
