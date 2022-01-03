from fastapi import status
from fastapi.testclient import TestClient

from app import main
from app.utils import constant

ENTRYPOINT = "/"
YEARLY_API = "/yearly"
MONTHLY_API = "/monthly"
DAILY_API = "/daily"

VALID_YEAR = 2021
VALID_MONTH = 10
VALID_DAY = 27

INVALID_YEAR_HIGHER = int(constant.LATEST_YEAR_CASE) + 1
INVALID_YEAR_LOWER = int(constant.EARLIEST_YEAR_CASE) - 1
INVALID_MONTH = 13
INVALID_DAY = 32
RANDOM_STRING = "RANDOM_STRING"

SUCCESS_MESSAGE = "success"

YEARLY_UPTO_MULTI_ERROR_MESSAGE = "Query parameters error! SINCE must be higher or equal than " + constant.EARLIEST_YEAR_CASE +" and UPTO can't be higher than " + constant.LATEST_YEAR_CASE +"!"
YEARLY_YEAR_SINGLE_ERROR_MESSAGE = "Value error! the provided YEAR must be higher or equal than 2020 and can't be higher than 2022!"
YEARLY_YEAR_SINGLE_INVALID_QUERY_ERROR_MESSAGE = "Value error! the provided YEAR must be an integer! with a value between " + constant.EARLIEST_YEAR_CASE +" and " + constant.LATEST_YEAR_CASE +"!"
YEARLY_SINCE_HIGHER_THAN_UPTO_ERROR_MESSAGE = "Query parameters error! SINCE can't be a higher value than UPTO!"

MONTHLY_MULTI_ERROR_MESSAGE = "Query parameter error! SINCE and UPTO must be a valid date in the format of 'YYYY.MM'. Valid values for YYYY are the value of integers between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE
MONTHLY_YEAR_MULTI_ERROR_MESSAGE = "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
MONTHLY_YEAR_MULTI_SINCE_UPTO_ERROR_MESSAGE = "Query parameter error! year in SINCE or UPTO must match with the provided YEAR!"
MONTHLY_YEAR_MULTI_SINCE_HIGHER_ERROR_MESSAGE = "Query parameter error! month in SINCE must be lower or equal to month in UPTO!" 
MONTHLY_YEAR_MULTI_SINCE_UPTO_INVALID_ERROR_MESSAGE = "Query parameter error! Invalid month value in SINCE or UPTO!"
MONTHLY_YEAR_MONTH_INTEGER_ERROR_MESSAGE = "YEAR and MONTH must be an integer!"
MONTHLY_YEAR_MONTH_INTEGER_INVALID_YEAR_ERROR_MESSAGE = "Invalid YEAR value! YEAR must be an integer with a value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
MONTHLY_YEAR_MONTH_INTEGER_INVALID_MONTH_ERROR_MESSAGE = "Invalid MONTH value! MONTH must be an integer with a value between 1 and 12!"

DAILY_MULTI_INVALID_ERROR_MESSAGE = "Query parameter error! SINCE and UPTO must be a valid date in the format of 'YYYY.MM.DD'. Valid values for YYYY are the value of integers between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE
DAILY_YEAR_MULTI_INVALID_ERROR_MESSAGE = "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"


client = TestClient(main.app)

#Positive
def test_get_entrypoint():
    response = client.get(f"{ENTRYPOINT}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_yearly_multi():
    response = client.get(f"{YEARLY_API}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert len(response.json()["data"]) > 1
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_yearly_single():
    response = client.get(f"{YEARLY_API}/{VALID_YEAR}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_monthly_multi():
    response = client.get(f"{MONTHLY_API}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert len(response.json()["data"]) > 1
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_monthly_year_multi():
    response = client.get(f"{MONTHLY_API}/{VALID_YEAR}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert len(response.json()["data"]) > 1
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_monthly_year_month_single():
    response = client.get(f"{MONTHLY_API}/{VALID_YEAR}/{VALID_MONTH}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_daily_multi():
    response = client.get(f"{DAILY_API}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert len(response.json()["data"]) > 1
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_daily_multi_year():
    response = client.get(f"{DAILY_API}/{VALID_YEAR}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert len(response.json()["data"]) > 1
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_daily_multi_year_month():
    response = client.get(f"{DAILY_API}/{VALID_YEAR}/{VALID_MONTH}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert len(response.json()["data"]) > 1
    assert response.json()["message"] == SUCCESS_MESSAGE

#Positive
def test_get_daily_single_year_month_date():
    response = client.get(f"{DAILY_API}/{VALID_YEAR}/{VALID_MONTH}/{VALID_DAY}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ok"] == True
    assert bool(response.json()["data"])
    assert response.json()["message"] == SUCCESS_MESSAGE

#Negative
def test_get_invalid_upto_yearly_multi():
    response = client.get(YEARLY_API + "?upto=" + str(INVALID_YEAR_HIGHER))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == YEARLY_UPTO_MULTI_ERROR_MESSAGE

#Negative
def test_get_invalid_since_yearly_multi():
    response = client.get(YEARLY_API + "?since=" + str(INVALID_YEAR_LOWER))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == YEARLY_UPTO_MULTI_ERROR_MESSAGE

#Negative
def test_get_invalid_since_higher_than_upto_yearly_multi():
    response = client.get(YEARLY_API + "?since=" + str(INVALID_YEAR_HIGHER))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == YEARLY_SINCE_HIGHER_THAN_UPTO_ERROR_MESSAGE

#Negative
def test_get_invalid_yearly_single():
    response = client.get(f"{YEARLY_API}/{INVALID_YEAR_HIGHER}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == YEARLY_YEAR_SINGLE_ERROR_MESSAGE

#Negative
def test_get_invalid_query_yearly_single():
    response = client.get(f"{YEARLY_API}/{RANDOM_STRING}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == YEARLY_YEAR_SINGLE_INVALID_QUERY_ERROR_MESSAGE

#Negative
def test_get_invalid_since_monthly_multi():
    response = client.get(MONTHLY_API + "?since=" + RANDOM_STRING)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_MULTI_ERROR_MESSAGE

#Negative
def test_get_invalid_upto_monthly_multi():
    response = client.get(MONTHLY_API + "?upto=" + RANDOM_STRING)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_MULTI_ERROR_MESSAGE

#Negative
def test_get_invalid_monthly_year_multi():
    response = client.get(f"{MONTHLY_API}/{RANDOM_STRING}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_YEAR_MULTI_ERROR_MESSAGE

#Negative
def test_get_invalid_monthly_year_since_invalid_multi():
    response = client.get(f"{MONTHLY_API}/{VALID_YEAR}" + "?since=" + str(INVALID_YEAR_LOWER))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_YEAR_MULTI_SINCE_UPTO_ERROR_MESSAGE

#Negative
def test_get_invalid_monthly_year_since_higher_invalid_multi():
    response = client.get(f"{MONTHLY_API}/{VALID_YEAR}" + "?since=" + str(VALID_YEAR) + ".13" )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_YEAR_MULTI_SINCE_HIGHER_ERROR_MESSAGE

#Negative
def test_get_invalid_monthly_year_upto_higher_invalid_multi():
    response = client.get(f"{MONTHLY_API}/{VALID_YEAR}" + "?upto=" + str(VALID_YEAR) + ".13" )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_YEAR_MULTI_SINCE_UPTO_INVALID_ERROR_MESSAGE

#Negative
def test_get_invalid_monthly_year_month_single():
    response = client.get(f"{MONTHLY_API}/{VALID_YEAR}/{RANDOM_STRING}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_YEAR_MONTH_INTEGER_ERROR_MESSAGE

#Negative
def test_get_invalid_monthly_year_higher_month_single():
    response = client.get(f"{MONTHLY_API}/{INVALID_YEAR_HIGHER}/{VALID_MONTH}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_YEAR_MONTH_INTEGER_INVALID_YEAR_ERROR_MESSAGE

#Negative
def test_get_invalid_monthly_year_month_higher_single():
    response = client.get(f"{MONTHLY_API}/{VALID_YEAR}/{INVALID_MONTH}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == MONTHLY_YEAR_MONTH_INTEGER_INVALID_MONTH_ERROR_MESSAGE

#Negative
def test_get_invalid_daily_multi():
    response = client.get(f"{DAILY_API}?since={RANDOM_STRING}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == DAILY_MULTI_INVALID_ERROR_MESSAGE

#Negative
def test_get_invalid_daily_year_multi():
    response = client.get(f"{DAILY_API}/{RANDOM_STRING}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == DAILY_YEAR_MULTI_INVALID_ERROR_MESSAGE