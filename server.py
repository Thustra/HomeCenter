__author__ = 'Peter'

from waitress import serve
from app import app

serve(app, host='0.0.0.0')