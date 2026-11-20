from pathlib import Path
import src.config as cfg
import requests

#The URL we'll use for the extraction.
API_URL = "https://archive-api.open-meteo.com/v1/archive"

RAW_DIR = Path("data/raw/openMeteoTemperatures")
RAW_DIR.mkdir(parents=True, exist_ok=True)

for city, coordinates in cfg.CITIES_COORDINATES.items():
    #The parameters we must send to retrieve only Cluj and Bucharest in JSON format to retrieve only the
    #data that's useful to us.
    params = {
        "latitude": coordinates["lat"],
        "longitude": coordinates["lon"],
        "start_date": "1991-01-01",
        "end_date": "2025-12-31",
        "daily": "temperature_2m_max",
        "models": "era5_land",
        "timezone": "GMT"
    }
    resp = requests.get(API_URL, params=params, timeout=20)
    resp.raise_for_status()
    out_file = RAW_DIR / f"{city}.json"
    out_file.write_bytes(resp.content)

    