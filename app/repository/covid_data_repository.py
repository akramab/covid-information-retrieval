from ..models import covid_data_model
from ..utils import utility_functions


def find_data_by_year(year):
    httpx_response_JSON = covid_data_model.covid_data_JSON
    year = str(year)

    result = {
        "year": year,
        "positive": 0,
        "recovered": 0,
        "deaths": 0,
        "active": 0
    }
    
    for daily_data in httpx_response_JSON["update"]["harian"]:
        if (year in daily_data["key_as_string"]):
            result["positive"] += daily_data["jumlah_positif"]["value"]
            result["recovered"] += daily_data["jumlah_sembuh"]["value"]
            result["deaths"] += daily_data["jumlah_meninggal"]["value"]
            result["active"] += daily_data["jumlah_dirawat"]["value"]
    
    return result

def find_data_by_year_month(year, month):
    httpx_response_JSON = covid_data_model.covid_data_JSON
    month = (str(int(month))) if (int(month) >= 10) else ("0" + str(int(month)))

    year_month = str(year) + "-" + month

    result = {
        "month": year_month,
        "positive": 0,
        "recovered": 0,
        "deaths": 0,
        "active": 0
    }
    
    for daily_data in httpx_response_JSON["update"]["harian"]:
        if (year_month in daily_data["key_as_string"]):
            result["positive"] += daily_data["jumlah_positif"]["value"]
            result["recovered"] += daily_data["jumlah_sembuh"]["value"]
            result["deaths"] += daily_data["jumlah_meninggal"]["value"]
            result["active"] += daily_data["jumlah_dirawat"]["value"]
    
    return result

def find_data_by_dates(since, upto):
    httpx_response_JSON = covid_data_model.covid_data_JSON
    result = []

    for daily_data in httpx_response_JSON["update"]["harian"]:
        if((utility_functions.is_date_greater_than(daily_data["key_as_string"][0:10], since)) and (utility_functions.is_date_lower_than(daily_data["key_as_string"][0:10], upto))):
            result.append({
                "date": daily_data["key_as_string"][0:10],
                "positive": daily_data["jumlah_positif"]["value"],
                "recovered": daily_data["jumlah_sembuh"]["value"],
                "deaths": daily_data["jumlah_meninggal"]["value"],
                "active": daily_data["jumlah_dirawat"]["value"]
            })
    
    return result