# Backend BLE Scanner

## Pre Requirements
- Python 3.8 or higher;
- Pip
- Pipenv 
- DBMS (MySQL, PostgreSQL or some other) or SQLite
  
## Configure environment 
- install dependencies for backend:
  ```
  pipenv install 
  ```
- install DBMS (MySQL, PostgreSQL or some other) or use SQLite and create database;
- create file `.env` with environment variables, for example:
  ```
  DATABASE_URL=mysql+pymysql://root:YOUR_ROOT_PASSWORD.@localhost/YOUR_DB_NAME
  SECRET_KEY=YOUR_SECRET_KEY
  ```
- or add variables from command line interface: 
    - in Linux:
    ```
    $ export DATABASE_URL=mysql+pymysql://root:YOUR_ROOT_PASSWORD.@localhost/YOUR_DB_NAME
    $ export SECRET_KEY=YOUR_SECRET_KEY
    ```
    - in Windows CMD:
    ```
    > set DATABASE_URL=mysql+pymysql://root:YOUR_ROOT_PASSWORD.@localhost/
    > set SECRET_KEY=YOUR_SECRET_KEY
    ```
    - in Windows PowerShell:
    ```
    > $env:DATABASE_URL = "mysql+pymysql://root:YOUR_ROOT_PASSWORD.@localhost/"
    > $env:SECRET_KEY = "YOUR_SECRET_KEY"
    ```

## Run backend
- run backend with command:
  ```
  pipenv run python3 run.py
  ```
- create tables in DB from other window:
  ```
  pipenv run db init
  pipenv run db migrate
  pipenv run db upgrade
  ```
- upload bledata to database:
  - change address if not default in [file](https://github.com/NaWindows-Inc/backend/blob/main/upload_data.py):
    ```
    6  address = "127.0.0.1:5000"
    ```
  - run script:
    ```
    pipenv run upload_data.py
    ```

## Run tests
- run tests without coverage:
  ```
  pipenv run test
  ```