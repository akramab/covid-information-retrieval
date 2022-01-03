# nodeflux-se-tech-assesment

## 📖  How to Run #1 (Non-Docker Version)

1. Install virtualenv if you haven't
```
pip install virtualenv
```
2. Create virtualenv
```
virtualenv venv
```

3. Activate the created virtualenv
```
venv\Scripts\activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Start the Server
```
uvicorn app.main:app --reload
```

6. Open the server
```
open "localhost:8000/docs" to check the API manually using Swagger UI
```

7. Run the Unit Tests
```
run "pytest" on terminal/CMD
```

## 📖  How to Run #2 (Using Docker Compose)
1. Make sure that you've got Docker installed on your device
2. Run the command "docker-compose up -d" in the same directory where the Dockerfile and docker-compose.yml is
3. Open "localhost:8000/docs", same as run method #1
4. If you've finished, don't forget to kill the docker process by running "docker-compose down"

## General Description

This app is built using FastAPI framework. The app works by using the data that's fetched from Indonesia Government APIs (https://documenter.getpostman.com/view/16605343/Tzm6nwoS).

This app first opens HTTP connection by calling the endpoint that will give JSON data that contains case number, recovery, death, hospitalitation/treatment (active cases), and historically daily data.

The JSON data will then be saved in the memory as long as the app is still running in the same session. This is done to make sure that the connection to the external API (Indonesia Government APIs) is only established once, because the rest of the operation that this app make can be done by using the saved JSON data. This will lead to more efficient performance and eliminate unnecessary HTTP request to the external API.

All of the GET operations that are implemented use the same JSON data. The difference is that each of the operation make a different 'query', depending on the specification of each endpoints.

This app also implements some basic error handling by making use of the HTTPException class that's provided by the FastAPI framework. There are still some corner cases that's still not covered by the error handling because of the limited amount of time to build this app.

## Project Structure
```
app/
├─ models/
│  ├─ __init__.py
│  ├─ covid_data_model.py
├─ repository/
│  ├─ __init__.py
│  ├─ covid_data_repository.py
├─ routers/
│  ├─ __init__.py
│  ├─ entrypoint_router.py
│  ├─ daily_router.py
│  ├─ monthly_router.py
│  ├─ yearly_router.py
├─ services/
│  ├─ __init__.py
│  ├─ entrypoint_service.py
│  ├─ daily_service.py
│  ├─ monthly_service.py
│  ├─ yearly_service.py
├─ schemas/
│  ├─ __init__.py
│  ├─ entrypoint_schema.py
│  ├─ daily_schema.py
│  ├─ monthly_schema.py
│  ├─ yearly_schema.py
├─ utils/
│  ├─ __init__.py
│  ├─ constant.py
│  ├─ utility_functions.py
├─ __init__.py
├─ main.py
test/
├─ test_main.py
├─ __init__.py
```

### app directory
The models directory contains the JSON data that's fetched from the external API. Schemas director is used to define the Pydantic Models that's being used as data validation for the whole FastAPI endpoints. The repository is there to supply the basic operations that are used to manipulate/query the data from models (JSON data). Most of the application logic reside in the service directory including the Exception Handling. The routes directory is used to map the each service to the endpoints to call the APIs. Finally, the utils folder is there to save constant information and also utility functions that are being used throughout the application.

### test directory
This directory only contains test_main.py file that's used to hold all the testing that's used in this app. All of the tests are done using pytest.


## Limitation, Potential Issues, and Future Ideations
Most of the limitation within this app came from my own inexperience from using Python and also FastAPI. This project is actually my first actual backend server that I made using Python and FastAPI (I came from Java Spring Boot background). So I am very sorry if the project structure kinda resembles Java project structure a lot, and doesn't really reflect how a Python project structure should really be.

Potential Issues in this app will mostly come from the unhandled corner cases Exception that haven't been implemented yed.

I think this app could have a lot of improvement. For example, by using more Object Oriented approach, all of the codes in this project could be more concisely and cleanly written. This app could also implement caching, by using Redis for example, to make sure that the repeted operations could be done faster. And last but not least this app could also implement some limiter to make sure that if the app is ran more than once in the same day, it will only fetch the API data once. Because as we all know, the APIs that's used to get all the COVID data is updated daily, so it's unnecessary to make a request everytime the app is ran.