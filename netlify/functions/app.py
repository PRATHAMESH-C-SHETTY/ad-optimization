"""
Netlify Serverless Function Handler for Flask App
Converts Flask app to work with Netlify Functions
"""

import sys
import os
import json
from urllib.parse import parse_qs
from io import BytesIO

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Change to project directory for relative imports
os.chdir(project_root)

from app import app as flask_app


def handler(event, context):
    """
    Netlify Functions handler for Flask application
    Converts HTTP events to WSGI-compatible format
    """
    
    # Extract request details from event
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    headers = event.get('headers', {})
    query_string = event.get('queryStringParameters') or {}
    body = event.get('body', '')
    is_base64_encoded = event.get('isBase64Encoded', False)
    
    # Normalize headers to lowercase
    headers_lower = {k.lower(): v for k, v in headers.items()}
    
    # Decode body if base64 encoded
    if is_base64_encoded and body:
        import base64
        body = base64.b64decode(body).decode('utf-8')
    
    # Build WSGI environ dictionary
    environ = {
        'REQUEST_METHOD': http_method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': '&'.join([f'{k}={v}' for k, v in query_string.items()]) if query_string else '',
        'CONTENT_TYPE': headers_lower.get('content-type', ''),
        'CONTENT_LENGTH': headers_lower.get('content-length', '0'),
        'SERVER_NAME': headers_lower.get('host', 'localhost').split(':')[0],
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(body.encode('utf-8') if isinstance(body, str) else body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': True,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add custom headers to environ
    for key, value in headers_lower.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            environ[f'HTTP_{key_upper}'] = value
    
    # Response handling
    status_code = 200
    response_headers = {}
    response_body = []
    
    def start_response(status, headers_list):
        nonlocal status_code, response_headers
        status_code = int(status.split()[0])
        response_headers = dict(headers_list)
        return response_body.append
    
    try:
        # Call Flask app
        app_response = flask_app(environ, start_response)
        
        # Collect response body
        for data in app_response:
            if isinstance(data, bytes):
                response_body.append(data)
            else:
                response_body.append(data.encode('utf-8') if isinstance(data, str) else data)
        
        # Combine response body
        final_body = b''.join(response_body)
        
        # Handle content encoding
        content_type = response_headers.get('Content-Type', '')
        if 'application/json' in content_type or 'text/' in content_type or 'application/json' in content_type:
            body_output = final_body.decode('utf-8', errors='replace')
        else:
            body_output = final_body.decode('utf-8', errors='replace')
        
        # Add CORS headers
        if 'Access-Control-Allow-Origin' not in response_headers:
            response_headers['Access-Control-Allow-Origin'] = '*'
        
        return {
            'statusCode': status_code,
            'headers': response_headers,
            'body': body_output,
            'isBase64Encoded': False
        }
        
    except Exception as e:
        import traceback
        print(f"Error in handler: {str(e)}")
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal Server Error', 'message': str(e)}),
            'isBase64Encoded': False
        }

