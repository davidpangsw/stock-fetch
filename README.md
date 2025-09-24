## Intro
- Set data range in `config.py`

## Run
1. In `config.py`, set the configuration of downloading
2. In `.env`, set the environment variables
3. Execute `./run.sh`, in the script, it automatically:
   1. Activates venv (See below)
   2. Inside venv, install dependencies using `pip install -r requirements`
   3. Executes `python main.py`

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
