from pathlib import Path
import pandas as pd

RAW_DIR = Path('data/raw/eurostatWeeklyDeaths')

#read the CSV, rename the geo column, and drop the useless stuff.
df = pd.read_csv(RAW_DIR / 'eurostatWeeklyDeaths.csv')
df = df.rename(columns={'geo\\TIME_PERIOD':'Region'})
df = df.drop(columns=['freq', 'sex', 'unit'])

#refactor the Dataframe such that we have lots of rows rather than lots of columns.
df = df.melt(id_vars='Region', var_name='Date', value_name='Value')

#because we also carry the flag, we separate these 2 into different fields
df[['Week','Kind']] = df['Date'].str.rsplit("_",n=1,expand=True)

#drop the old column
df = df.drop(columns=['Date'])

#opposite of melt, groups by region week
df = df.pivot(index=['Region', 'Week'], columns='Kind', values='Value')
df = df.reset_index()
df.columns.name = None

#drop the rows that have NaN value
df = df.dropna(subset=['value'], ignore_index=True)

#convert to week_start so we know the exact days (year, week, day)
df['week_start'] = pd.to_datetime(df['Week'] + '-1', format='%G-W%V-%u')
df['city'] = df['Region'].map({'RO113': 'cluj', 'RO321': 'bucharest'})
df = df.drop(columns=['Region', 'Week'])
df = df.rename(columns={'value': 'deaths'})

#make it so the value is int
df['deaths'] = pd.to_numeric(df['deaths']).astype(int)

#reorder the columns so it's city, week_start, deaths, flag
df = df.iloc[:, [3,2,1,0]]

#keep only 2015-2025
df = df[df['week_start'].dt.isocalendar().year <= 2025]

#sort for good measure
df = df.sort_values(['city', 'week_start'])

PRO_DIR = Path('data/processed/eurostatWeeklyDeaths')
PRO_DIR.mkdir(parents=True, exist_ok=True)

#save it as parquet
out_file = PRO_DIR / 'eurostatWeeklyDeaths.parquet'
df.to_parquet(out_file, index=False)