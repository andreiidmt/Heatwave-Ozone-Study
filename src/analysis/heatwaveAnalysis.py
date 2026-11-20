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


def flag_heatwaves(df: pd.DataFrame, min_days: int)->pd.DataFrame:
    pass

if __name__ == '__main__':
    # daily_threshold(None, percentile=90)
    pass

