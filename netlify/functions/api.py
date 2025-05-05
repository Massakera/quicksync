from http.server import BaseHTTPRequestHandler
import json
import importlib.util
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from quicksync.src.main import app

from mangum import Mangum

handler = Mangum(app)