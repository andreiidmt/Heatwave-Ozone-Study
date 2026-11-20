STATIONS = {
    "bucharest": ["RO0065A", "RO0071A", "RO0229A"],
    "cluj": ["RO0074A", "RO0075A", "RO0232A"],
}

# 2019 dropped: no Bucharest background station has valid 2019 ozone in EEA E1a.
YEARS = [2020, 2021, 2022, 2023, 2024, 2025]

SUMMER_MONTHS = [5, 6, 7, 8, 9]

#every faulty case (Bucharest 2024, Cluj 2024, Cluj 2025) is in the 2024–2025 data,
# which Romania delivered to the EEA in one batch on 27 August 2026. It’s all marked “verified”,
# but that batch looks less reliable than earlier years.

EXCLUSION_TABLE_MDA_AVERAGE = [('RO0065A', 2024), ('RO0071A', 2024), ('RO0075A', 2024)]

#Exclude summers with a MDA8 mean of less than 75%
MIN_MDA_VALIDITY = 0.75

CITIES_COORDINATES = {
    "cluj": {"lat": 46.77, "lon": 23.60},
    "bucharest": {"lat": 44.43, "lon": 26.10},
}

#For defining a heatwave, we'll look at the data from 1991 to 2020,
# using the Perkins & Alexander (2013), “CTX90pct” standard:
# - a heatwave must exceed the calendar-day 90th percentile for at least 3 consecutive days
# - the threshold for a given calendar day is calculated using a 15-day window centered on that day


BASELINE_CLIMATE = (1991,2020)
HEATWAVE_PERCENTILE = 90
HEATWAVE_WINDOW_DAYS = 15
HEATWAVE_MIN_DAYS = 3
