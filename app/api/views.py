from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.validation.validation import *
from app.validation.view_helper import *
from app.controller.controller import *
from app.datastructure.ds_methods import *
import datetime


mod = Blueprint('api', __name__)
userControl = UserController()
msgControl = MessageController()
helper = ViewHelper()
meth = DSMethods()

@mod.route('/api/v1/auth/signup', methods = ['POST'])
def signup():
    """
    This endpoint allows the user to create an account
    """
    try:
        json.loads(request.get_data())
    except(ValueError, TypeError):
        return jsonify({
            "status": 400,
            "error": "Your request should be a dictionary"
        }), 400
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "status": 400,
            "error": "Your request must be in json format"
        }), 400
    if len(data) < 4:
        return jsonify({
            "status": 400,
            "error": "Missing fields. Please make sure firstName, lastName, email and password are provided"
            }),400
    if len(data) > 4:
        return jsonify({
            "status": 414,
            "error": "Too many arguments. Only firstName, lastName, email and password are required"
            }),414
    if not "firstName" in data or not "lastName" or not "email" in data or not "password" in data:
        return jsonify({
            "status": 400,
            "error": "firstName, lastName, email or password is missing. Please check the spelling"
        }), 400

    validate_user = helper.user_signup_validation(data['firstName'], data['lastName'], data['email'], data['password'])
    if validate_user != "Valid":
        return jsonify({
            "status": 417,
            "error": validate_user
        }), 417
    user = userControl.signup(data['firstName'], data['lastName'], data['email'], data['password'])
    access_token = create_access_token(identity=user, expires_delta=datetime.timedelta(days=1))
    return jsonify({
        "status": 201,
        "token": access_token
    }), 201

