from pathlib import Path
import os
import json
from django.core.exceptions import *

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'sanbo_RDS',
        'USER' : 'admin',
        'PASSWORD' : 'sanbo2023',
        'HOST' : 'sanbo-dev.c5qjl9gqdyjv.ap-northeast-2.rds.amazonaws.com',
        'PORT' : '3306',
    }
}

secret_file = os.path.join(BASE_DIR, 'Sanbo-Wiki-BackEnd/secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")