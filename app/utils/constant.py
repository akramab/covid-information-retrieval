import httpx
from datetime import date

covid_data_JSON = {}
with httpx.Client() as client:
    covid_data_JSON = client.get("https://data.covid19.go.id/public/api/update.json").json()

EARLIEST_YEAR_CASE = "2020"
EARLIEST_MONTH_CASE = "03"
EARLIEST_DAY_CASE = "02"

EARLIEST_YEAR_MONTH_CASE = EARLIEST_YEAR_CASE + "." + EARLIEST_MONTH_CASE
EARLIEST_DATE_CASE = EARLIEST_YEAR_MONTH_CASE + "." + EARLIEST_DAY_CASE

todays_date = date.today()

LATEST_YEAR_CASE = str(todays_date.year)
LATEST_MONTH_CASE = (str(int(todays_date.month))) if (int(todays_date.month) >= 10) else ("0" + str(int(todays_date.month)))
LATEST_DAY_CASE = (str(int(todays_date.day))) if (int(todays_date.day) >= 10) else ("0" + str(int(todays_date.day)))

LATEST_YEAR_MONTH_CASE = LATEST_YEAR_CASE + "." + LATEST_MONTH_CASE
LATEST_DATE_CASE = LATEST_YEAR_MONTH_CASE + "." + LATEST_DAY_CASE