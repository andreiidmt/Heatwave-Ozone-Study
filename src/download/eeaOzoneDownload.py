import requests
from pathlib import Path
import src.config as cfg

#url of the API that we will make GET and POST requests.
API_URL = "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile/urls"

#JSON body that will be used to filter only the stations in Romania
body={
    "countries": ["RO"],
    "cities": [],
    "pollutants" : ["O3"],
    "dataset": 2,
    "dateTimeStart": "2019-01-01T00:00:00Z",
    "dateTimeEnd": "2025-12-31T23:59:59Z",
    "aggregationType": "hour",
    "email": "",
}

#Filter the stations. If the server doesn't respond in less than 5 seconds, sever the connection.
r = requests.post(API_URL, json=body, timeout=5)

#incase the POST request failed, stop the program.
r.raise_for_status()

RAW_DIR = Path("data/raw/eeaOzoneMeasurements")
RAW_DIR.mkdir(parents=True, exist_ok=True)

URLs = r.text.splitlines()
URLs = URLs[1:]

#Keep only the valid city codes (as seen in config.py)
valid_codes = [code for city_code in cfg.STATIONS.values() for code in city_code]

for url in URLs:
    #Check to see if it matches any of the valid codes
    if any(f"SPO-{code}_" in url for code in valid_codes):
        out_file = RAW_DIR / url.rsplit("/")[-1]
        if (out_file.exists()):
            continue
        #GET request for that specific URL
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        out_file.write_bytes(resp.content)





