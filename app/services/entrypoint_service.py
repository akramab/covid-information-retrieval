from ..utils import constant, utility_functions

def index():
    httpx_response_JSON = constant.covid_data_JSON
    response_body = utility_functions.create_single_REST_response()

    response_body["data"] = {
        "total_positive": httpx_response_JSON["update"]["total"]["jumlah_positif"],
        "total_recovered": httpx_response_JSON["update"]["total"]["jumlah_sembuh"],
        "total_deaths": httpx_response_JSON["update"]["total"]["jumlah_meninggal"],
        "total_active": httpx_response_JSON["update"]["total"]["jumlah_dirawat"],
        "new_positive": httpx_response_JSON["update"]["penambahan"]["jumlah_positif"],
        "new_recovered": httpx_response_JSON["update"]["penambahan"]["jumlah_sembuh"],
        "new_deaths": httpx_response_JSON["update"]["penambahan"]["jumlah_meninggal"],
        "new_active": httpx_response_JSON["update"]["penambahan"]["jumlah_dirawat"]
    }
    return response_body