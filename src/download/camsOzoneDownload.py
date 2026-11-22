import requests
from pathlib import Path
import src.config as cfg

RAW_DIR = Path('data/raw/camsOzone')
RAW_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

#** unpacks the key value pairs in the points dictionary
points = {**cfg.CITIES_COORDINATES, **cfg.STATIONS_COORDINATES}

for location, coordinates in points.items():
    params={
        "latitude": coordinates["lat"],
        "longitude": coordinates["lon"],
        "start_date": "2019-01-01",
        "end_date": "2025-12-31",
        "hourly": "ozone",
        "domains": "cams_europe",
        "timezone": "GMT",
    }
    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()
    out_file = RAW_DIR / f"{location}.json"
    if out_file.exists():
        continue
    out_file.write_bytes(response.content)


