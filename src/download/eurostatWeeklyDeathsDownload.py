import eurostat
from pathlib import Path

#path where we will store the csv with the raw data.
RAW_DIR = Path('data/raw/eurostatWeeklyDeaths')
RAW_DIR.mkdir(parents=True, exist_ok=True)

#retrieve only from Bucharest and Cluj, T is for both female and male.
df = eurostat.get_data_df('demo_r_mwk3_ts', flags=True,
                          filter_pars = {'geo': ['RO321', 'RO113'], 'sex': ['T']})


#save to a CSV file.
out_file = RAW_DIR / 'eurostatWeeklyDeaths.csv'
df.to_csv(out_file, index=False)
print('Eurostat data extraction complete, saved to eurostatWeeklyDeaths.csv.')
