import requests

# Get Global Stats api-endpoint
from data.globalstats.create_globalstats import create_update_globalstats

URL = "https://covid19-update-api.herokuapp.com/api/v1/world"


def fetch_and_update(event, context):
    # sending get request and saving the response as response object
    r = requests.get(url=URL)
    # extracting data in json format
    data = r.json()
    create_update_globalstats(data)
