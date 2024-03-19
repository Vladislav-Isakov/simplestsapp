import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret-secret-key"
    BASE_SITE_URL = "https://apiproxy.telphin.ru/"
    BASE_API_URL = "https://apiproxy.telphin.ru/api/ver1.0/"
    REDIRECT_AUTHORIZED_URL = "http://127.0.0.1:5055/authorized"
    APP_CLIENT_ID = os.environ.get('APP_CLIENT_ID')
    APP_CLIENT_SECRET = os.environ.get('APP_CLIENT_SECRET')