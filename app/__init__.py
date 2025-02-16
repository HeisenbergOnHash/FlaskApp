import logging
from http import HTTPStatus
from flask_cors import CORS
from flask import Flask, request, jsonify
from .BluePrints.root import root_blueprint
from .BluePrints.user import user_blueprint
from .BluePrints.admin import admin_blueprint
from app.middleware.auth import decode_access_token,extend_cookie_expiration


def Flask_App():
  app = Flask(__name__)
  CORS(app, resources={r"/*": {"origins": "*","supports_credentials": True,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]}})

  app.config['SESSION_COOKIE_HTTPONLY'] = True                # Set HttpOnly to True
  app.config['SESSION_COOKIE_SAMESITE'] = False               # Set SESSION_COOKIE_SAMESITE to True

  
  app.register_blueprint(root_blueprint)                      # Register Blueprints
  app.register_blueprint(user_blueprint, url_prefix='/user')
  app.register_blueprint(admin_blueprint, url_prefix='/admin')

  @app.before_request
  def before_request():
    if request.method == 'OPTIONS':return '', HTTPStatus.NO_CONTENT
    if 'admin' in request.url or 'user' in request.url:
      status = decode_access_token()
      if not status['valid']:
        return jsonify({'status': status['status'], 'message': status['message']}), HTTPStatus.UNAUTHORIZED
      if status['data']['role'] in request.url:return None
      else:return jsonify(ErrorMessage = 'Forbidden - role mismatch'), HTTPStatus.FORBIDDEN

  @app.after_request
  def after_request(response):
    if 'logout' not in request.url:
      response = extend_cookie_expiration(response)
    return response

  return app