# Backend News

News project

# How to Start:
  - Create Db(mySql) with this config:
    - `NAMEDB`: `news`,
    - `USER`: `root`,
    - `PASSWORD`: `monikasiahaan067`,
    - `HOST`: `127.0.0.1`
    - `PORT`: `3306`,
  - Activated python virtual env with this command `$ source env/bin/activate`
  - Move to directory `backend`
  - Install dependency library for project shark with run this command `pip install -r requirements.txt`
  - Run this command `python manage.py migrate`
  - Run this command to start server `python manage.py runserver 0.0.0.0:8000 --settings=config.settings.local`
  - Check your browser and type this address`http://localhost:8000`
  
  
  
 You can see list of endpoint from file `Backend.postman_collection.json`
