__author__ = 'Peter'
import os
# default configuration

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'p\xfa\xa6\x0fM\x7f\xb4o\xae\xb1\x1dv\x82\xacky\xd6\xe4\x93\x0b\x00\x86\xc6&'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
