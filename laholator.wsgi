import sys
from os.path import dirname, abspath
from os import sep

PROJECT_DIR = abspath(dirname(__file__))
sys.path.append(PROJECT_DIR)

APP_NAME = PROJECT_DIR.split(sep)[-1].lower()

_app = __import__(APP_NAME,fromlist=['app'])
application = _app.app
