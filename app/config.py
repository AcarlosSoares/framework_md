import os


class Config(object):
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    PERMANENT_SESSION_LIFETIME =  1800 # 30 minutos
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/db_framework'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_USERNAME = 'acls.soares@gmail.com'
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_PASSWORD = 'Antoleite26'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
