import os
import sys
from urllib.parse import parse_qs, urlencode

# Add root directory to python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app

# Restores the exact URL path and HTTP method for Flask
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get('QUERY_STRING', '')
        if '__path' in qs:
            params = parse_qs(qs, keep_blank_values=True)
            if '__path' in params and params['__path']:
                environ['PATH_INFO'] = '/' + params['__path'][0].lstrip('/')
            else:
                environ['PATH_INFO'] = '/'
            params.pop('__path', None)
            environ['QUERY_STRING'] = urlencode(params, doseq=True)
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
