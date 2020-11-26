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

## Run tests
- run tests without coverage:
  ```
  pipenv run test
  ```
- run test with coverage:
  ```
  pipenv run nosetests --with-coverage --cover-package=app
  ```