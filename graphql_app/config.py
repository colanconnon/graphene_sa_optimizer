import os


class Config(object):
    """Test configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    SQLALCHEMY_ECHO = True
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(PROJECT_ROOT, DB_NAME)
    DEBUG_TB_PROFILER_ENABLE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_RECORD_QUERIES = True
    SECRET_KEY = 'secret-key'  # TODO: Change me
    SQLALCHEMY_TRACK_MODIFICATIONS = False