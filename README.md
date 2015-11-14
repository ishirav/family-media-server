# Family Media Server

## Installation

```
sudo apt-get install libcurl4-openssl-dev
virtualenv env
pip install -U pip
pip install -r requirements.txt
touch fms/local_settings.py
mkdir media
python manage.py migrate
```

## Running

```
thumbor -c thumbor.conf &
python manage.py runserver
```

Icons from https://www.iconfinder.com/iconsets/flat-color-icons
