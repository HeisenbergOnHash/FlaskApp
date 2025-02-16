import logging, os
from app import Flask_App
from waitress import serve
from logging.handlers import RotatingFileHandler


app = Flask_App()

logging.basicConfig(level=logging.NOTSET, format='%(levelname)s - %(message)s')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.getenv('PORT', 8080)),threads=8)

