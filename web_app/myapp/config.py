import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ndolokajwang8@gmail.com']
    LANGUAGES = ['en-US', 'en-GB', 'en-CA', 'es']
