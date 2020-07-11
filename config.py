import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-hidden-key'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://boodoo:pass1234@localhost/boodoo'
  SQLALCHEMY_TRACK_MODIFICATIONS = False