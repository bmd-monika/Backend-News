# Backend-News

Backend News
News project

How to Start:
Create database with this config:
        'NAMEDB': 'news',
        'USER': 'root',
        'PASSWORD': 'monikasiahaan067',
        'HOST': '127.0.0.1', # Or an IP Address that your DB is hosted on
        'PORT': '3306',
Move to directory backend
Install dependency library for project shark with run this command pip install -r requirements.txt
Run this command python manage.py migrate
Run this command to start server python manage.py runserver 0.0.0.0:8000 --settings=config.settings.local
Check your browser and type this address http://localhost:8000
