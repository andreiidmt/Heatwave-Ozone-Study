import pandas as pd
from pathlib import Path
import src.config as cfg

def daily_threshold(tmax:pd.Series, percentile: float) -> pd.Series:
    study_year_start, study_year_end = cfg.BASELINE_CLIMATE

    #Must use to get the DateTimeIndex for the window
    window = pd.Timedelta(days=cfg.HEATWAVE_WINDOW_DAYS//2)

    thresholds = {}

    for date in pd.date_range('2017-01-01', '2017-12-31'):
        day = date.day
        month = date.month
        #We are simply going to store all the values for the windows in these 30 years and then do
        # a 90th percentile filter on it.
        values = []
        for year in range(study_year_start, study_year_end+1):
            centre = pd.Timestamp(year, month, day)
            date_start = centre-window
            date_end = centre+window
            values.extend(tmax.reindex(pd.date_range(date_start, date_end)))
        thresholds[(month,day)] = pd.Series(values).quantile(percentile/100)

    return pd.Series(thresholds)


def flag_heatwaves(is_hot: pd.Series, min_days: int)->pd.Series:
    changed = is_hot != is_hot.shift()
    run_id = changed.cumsum()
    run_length = is_hot.groupby(run_id).transform('count')
    return is_hot & (run_length >= min_days)





if __name__ == '__main__':
    file = Path('data/processed/openMeteoTemperatures/openMeteoTemperatures.parquet')
    table = pd.read_parquet(file)
    table = table.set_index('date')

    results = []

    for city, temps in table.groupby('city')['tmax']:
        thresholds = daily_threshold(temps, percentile=cfg.HEATWAVE_PERCENTILE)

        keys = [(2, 28) if (d.month, d.day) == (2, 29) else (d.month, d.day)
                for d in temps.index]

        threshold_per_day = pd.Series([thresholds[k] for k in keys], index=temps.index)
        is_hot = temps > threshold_per_day
        is_heatwave = flag_heatwaves(is_hot, cfg.HEATWAVE_MIN_DAYS)

        results.append(pd.DataFrame({
            'city': city,
            'tmax': temps,
            'threshold': threshold_per_day,
            'is_hot': is_hot,
            'is_heatwave': is_heatwave,
        }))

    heatwaves = pd.concat(results).reset_index()
    DER_DIR = Path('data/derived')
    DER_DIR.mkdir(parents=True, exist_ok=True)

    OUT_FILE = DER_DIR / 'heatwaves.parquet'
    OUT_FILE.write_bytes(heatwaves.to_parquet())





