import httpx

covid_data_JSON = {}
with httpx.Client() as client:
    covid_data_JSON = client.get("https://data.covid19.go.id/public/api/update.json").json()