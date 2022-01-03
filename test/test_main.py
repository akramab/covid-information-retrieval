from fastapi import status
from fastapi.testclient import TestClient

from app import main

ENTRYPOINT = "/"
YEARLY_API = "/yearly"
MONTHLY_API = "/monthly"
DAILY_API = "/daily"

VALID_YEAR = 2021
VALID_MONTH = 10
VALID_DAY = 27

INVALID_MONTH = 13
INVALID_DAY = 32

SUCCESS_MESSAGE = "success"

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