import pandas as pd
from pathlib import Path
import src.config as cfg

RAW_DIR = Path('data/raw/eeaOzoneMeasurements')
OUT_DIR = Path('data/processed/eeaOzone')

def MDA8(hourly: pd.Series) -> pd.Series:
    """
        Daily maximum 8-hour mean ozone (MDA8) for a single station.

        hourly: complete hourly series (index = Start time, UTC), NaN for invalid hours
        returns: daily MDA8; NaN if a day has fewer than 18 valid 8-hour means
                    (an 8-hour mean needs at least 6 valid hours)
    """

    run8 = hourly.rolling('8h', min_periods=6).mean()
    daily = run8.resample('1D')

    return daily.max().where(daily.count()>=18)

if __name__ == '__main__':
    results = []

    for file in RAW_DIR.iterdir():
        df = pd.read_parquet(file)

        #Make it normal float type
        df['Value'] = df['Value'].astype(float)

        #Make the start date as the index so the rolling window can understand how to proceed.
        df = df.set_index('Start').sort_index()

        #We do not want to remove the rows with invalid values, as these lower the MDA8 for otherwise valid days.
        v = df['Value'].where(df['Validity']>0)

        #Just as a safety net, in case the file simply didn't have the row for an hour.
        v = v.asfreq('h')

        #Keep the name of the columns as just the stations name
        results.append(MDA8(v).rename(file.stem.split('-')[1][:7]))

    #Put the result as a table
    table = pd.concat(results, axis = 1, sort=False)

    #Filter the years
    table = table[table.index.year.isin(cfg.YEARS)]

    #Filter the months
    table = table[table.index.month.isin(cfg.SUMMER_MONTHS)]


    #For those stations that have weird values (were delivered in the 27 August 2026 Batch), set the
    #values to NaN
    for station, year in cfg.EXCLUSION_TABLE_MDA_AVERAGE:
        table.loc[table.index.year == year, station] = float('NaN')

    #See how much of the summer days are valid, and then set those who aren't valid to NaN
    coverage = table.notna().groupby(table.index.year).mean()
    for year in cfg.YEARS:
        for column in coverage.columns:
            if coverage.loc[year, column] < cfg.MIN_MDA_VALIDITY:
                table.loc[table.index.year == year, column] = float('NaN')

    station_to_city = {station: city for city, stations in cfg.STATIONS.items() for station in stations}

    #Reformat the table so each row represents the mda8 value for a station on a specific day.
    long = table.stack().rename("mda8").reset_index()

    #Do not keep invalid measurements
    long = long.dropna(subset=['mda8'])

    long = long.rename(columns={'Start': 'date', 'level_1': 'station'})

    #Map each station to a city
    long['city'] = long['station'].map(station_to_city)

    #Though not useful now, we will do a comparison with CAMS, and that will help us then.
    long['source'] = 'station'

    print(long)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / 'eeaOzoneMeasurements.parquet'
    long.to_parquet(out_file, index=False)



