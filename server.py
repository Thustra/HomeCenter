__author__ = 'Peter'

from waitress import serve
import os
from project import app

port = int(os.environ.get('PORT', 9999))
serve(app, host='0.0.0.0', port=port)