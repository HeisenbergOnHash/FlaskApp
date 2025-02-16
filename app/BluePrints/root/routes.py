
from http import HTTPStatus
from . import root_blueprint
import datetime, logging, json
from app.utils.logic.backend import backend
from flask import jsonify, request, make_response
from app.middleware.auth import create_access_token
from app.utils.services.hardware.get_info import get_system_details

@staticmethod
@root_blueprint.route('/', methods=['GET'])
def public_info():
  return jsonify(message="Public Information version 1.0 from Flask HTTPOnly ", data=get_system_details()), HTTPStatus.OK

@staticmethod
@root_blueprint.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
  if role not in ['client', 'manager']:
      return jsonify(ErrorMessage="Invalid role"), HTTPStatus.BAD_REQUEST
  if request.method == 'GET':
    if request.args.get('phone_number'):
      fetch_function = backend.FetchAdminOrUser if role == 'client' else backend.FetchAdminOrUser
      msg, code = fetch_function(request.args.get('phone_number'), role);return jsonify(msg), code
    else:return jsonify(ErrorMessage="Phone Number Not Found in the Params"), HTTPStatus.NOT_FOUND
  elif request.method == 'POST': 
    if request.json.get('username') and request.json.get('password'):
      msg, code = backend.authenticate(request.json.get('username'), request.json.get('password'), role)
      if code == HTTPStatus.OK:
        token = create_access_token(request.json.get('username'), "user" if role == "client" else "admin")
        response = make_response(jsonify(message = 'Login successful'))
        response.set_cookie('token_cookie', token, httponly=True, secure=True, samesite=None)
        return response, code
      else:return jsonify(msg), code
    else:return jsonify({"ErrorMessage": "Username or password not provided"}), HTTPStatus.BAD_REQUEST

@staticmethod
@root_blueprint.route('/logout', methods=['POST'])
def logout():
  response = make_response(jsonify(message = 'Logout successful'))
  response.set_cookie('token_cookie', '', expires=int((datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=11)).timestamp()),httponly=True, secure=True, samesite='None')
  response.delete_cookie('token_cookie', path='/');return response, HTTPStatus.OK