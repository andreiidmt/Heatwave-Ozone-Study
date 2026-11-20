from pathlib import Path
import pandas as pd
import json


RAW_DIR = Path('data/raw/openMeteoTemperatures')

PRO_DIR = Path('data/processed/openMeteoTemperatures')
PRO_DIR.mkdir(parents=True, exist_ok=True)

dataFrameList = []

for file in RAW_DIR.iterdir():
    data = json.loads(file.read_text(encoding='utf-8'))
    data['daily']['time'] = pd.to_datetime(data['daily']['time'])
    data['daily']['city'] = file.stem
    df = pd.DataFrame(data['daily'])
    dataFrameList.append(df)

bigTable = pd.concat(dataFrameList, ignore_index=True)
bigTable = bigTable.rename(columns={'time': 'date', 'temperature_2m_max': 'tmax'})
bigTable = bigTable[['city', 'date', 'tmax']]
bigTable.to_parquet(PRO_DIR / 'openMeteoTemperatures.parquet')
print(bigTable)
