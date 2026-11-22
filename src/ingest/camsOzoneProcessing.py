import json
from pathlib import Path
import pandas as pd
from src.ingest.eeaOzoneProcessing import MDA8
import src.config as cfg

RAW_DIR = Path('data/raw/camsOzone')

PRO_DIR = Path('data/processed/camsOzone')
PRO_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    results = []

    point_to_city = {station: city for city, stations in cfg.STATIONS.items() for station in stations}
    point_to_city.update({city: city for city in cfg.STATIONS.keys()})

    for file in RAW_DIR.iterdir():
        data = json.loads(file.read_text(encoding='utf-8'))
        table = pd.DataFrame(data['hourly'])
        table['time'] = pd.to_datetime(table['time'])
        table = table.set_index('time')
        hourly = table['ozone'].asfreq('h')
        daily = MDA8(hourly)
        daily = daily[daily.index.month.isin(cfg.SUMMER_MONTHS)]
        results.append(pd.DataFrame({
            'point': file.stem,
            'city': point_to_city[file.stem],
            'mda8': daily,
            'source': 'cams'

        }))

    table = pd.concat(results).reset_index()
    table = table.rename(columns={'time': 'date'})
    out_file = PRO_DIR / 'camsOzone.parquet'
    table.to_parquet(out_file, index=False)


