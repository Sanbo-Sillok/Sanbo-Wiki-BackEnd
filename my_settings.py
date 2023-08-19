from pathlib import Path
import os
import json
from django.core.exceptions import *

BASE_DIR = Path(__file__).resolve().parent.parent

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'sanbo_RDS',
        'USER' : 'admin',
        'PASSWORD' : get_secret("DB_PASSWORD"),
        'HOST' : get_secret("DB_HOST"),
        'PORT' : '3306',
    }
}
