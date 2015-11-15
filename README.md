# Family Media Server

## Installation

```
sudo apt-get install libcurl4-openssl-dev libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev
virtualenv env
source env/bin/activate
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
