# nodeflux-se-tech-assesment

## 📖  How to Run

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

## Notes

- Active cases
The number of confirmed cases minus the number of recovered cases and deaths. It is the number of cases still considered to be infectious.