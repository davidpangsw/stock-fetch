## Intro
- Only data before 2022-01-01

## Run
1. In `main.py`, set the configuration of downloading
2. In `database.py`, set the configuration of databse
3. Activate venv (See below)
4. Inside venv, `pip install -r requirements`
5. `python main.py`

## Activate venv
- Linux
```
source ./venv/bin/activate
```

- Windows:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

## Write requirements.txt
`pip3 freeze > requirements.txt`

## MySQL settings
