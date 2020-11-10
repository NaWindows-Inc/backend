# Backend BLE Scanner


pipenv install 

pip3 install -r requirements.txt

pipenv run db init

pipenv run db migtare

pipenv run db update


export FLASK_ENV=development
export DATABASE_URL=mysql+pymysql://nane_user:password@localhost/db_name