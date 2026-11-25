from pathlib import Path

import pandas as pd

EEA_FILE = Path('data/processed/eeaOzone/eeaOzoneMeasurements.parquet')
CAMS_FILE = Path('data/processed/camsOzone/camsOzone.parquet')

if __name__ == '__main__':
    eeaTable = pd.read_parquet(EEA_FILE)
    camsTable = pd.read_parquet(CAMS_FILE)

    bigTable = pd.merge(eeaTable, camsTable, left_on=['station', 'date'], right_on=['point', 'date'],
                        suffixes=['_eea', '_cams'])

    bigTable=bigTable[['station', 'city_eea', 'date', 'year', 'kept', 'reason',
                         'mda8_eea', 'mda8_cams']].rename(columns={'city_eea': 'city'})

    bigTable['diff'] = bigTable['mda8_eea'] - bigTable['mda8_cams']
    bigTable['abs_error'] = bigTable['diff'].abs()
    bigTable['sq_error'] = bigTable['diff']**2
    bigTable = bigTable.groupby(['station', 'year'])

    summary = pd.DataFrame({
        'nr_days': bigTable.size(),
        'bias': bigTable['diff'].mean(),
        'mae': bigTable['abs_error'].mean(),
        'rmse': bigTable['sq_error'].mean() ** 0.5,
        'correlation': bigTable.apply(lambda grp: grp['mda8_eea'].corr(grp['mda8_cams'])),
        'kept': bigTable['kept'].first(),
        'reason': bigTable['reason'].first(),
    })

    RES_DIR = Path('results')
    RES_DIR.mkdir(parents=True, exist_ok=True)

    OUT_FILE = RES_DIR / 'eeaCamsComparison.csv'
    summary.reset_index().to_csv(OUT_FILE, index=False)