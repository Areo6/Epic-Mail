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
        data = request.get_json(force=True)
    except(ValueError, TypeError):
        return jsonify({
            "status": 400,
            "error": "Your request should be a dictionary"
        }), 400
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
        "data": access_token
    }), 201 

@mod.route("/api/v1/auth/login", methods = ["POST"])
def login():
    """
    This endpoint allows the user to login
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
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
    print(len(data))
    if len(data) < 2:
        return jsonify({
            "status": 400,
            "error": "Missing fields. Please make sure email and password are provided"
            }),400
    if len(data) > 2:
        return jsonify({
            "status": 414,
            "error": "Too many arguments. Only email and password are required"
            }),414
    if not "email" in data or not "password" in data:
        return jsonify({
            "status": 400,
            "error": "email or password is missing. Please check the spelling"
        }), 400

    user_login = helper.user_can_login(data["email"], data["password"])
    if user_login != "Valid":
        return jsonify({
            "status": 417,
            "error": user_login
        }), 417
    user = userControl.login(data["email"], data["password"])
    if user:
        access_token = create_access_token(identity=user, expires_delta=datetime.timedelta(days=1))
        return jsonify({
            "status": 200,
            "data": access_token
        }), 200
    return jsonify({
            "status": 401,
            "error": "email or password incorrect. Please try again"
        }), 401

@mod.route("/api/v1/messages", methods= ["POST"])
def create_message():
    """
    This endpoint allows the creation of a message
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
            "error": "Your request should be in json format"
        }), 400
    if len(data) < 4:
        return jsonify({
            "status": 400,
            "error": "Missing fields. Either subject, message, sentTo and status missing"
            }),400
    if len(data) > 4:
        return jsonify({
            "status": 414,
            "error": "Too many arguments. Only subject, message, sentTo and status missing are required"
            }),414
    if not "subject" in data or not "message" or not "sendTo" in data or not "status" in data:
        return jsonify({
            "status": 400,
            "error": "subject, message, sentTo and status missing is missing. Check the spelling"
        }), 400

    valid_message = helper.message_validation(data['subject'], data['message'], data['sendTo'], data['status'])
    if valid_message != "Valid":
        return jsonify({
            "status": 417,
            "error": valid_message
        }), 417
    message = msgControl.create_message(data['subject'], data['message'], data['sendTo'], data['status'])
    return jsonify({
        "status": 201,
        "data": data
    }), 201

@mod.route("/api/v1/messages", methods=["GET"])
def fetch_received_messages():
    """
    This endpoint allows the user to view all messages
    """
    return jsonify({
        "status": 200,
        "data": msgControl.fetch_received_messages()
    }), 200

@mod.route("/api/v1/messages/unread", methods=["GET"])
def fetch_unread_messages():
    """
    This endpoint allows the user to view all the unread messages
    """
    return jsonify({
        "status": 200,
        "data": msgControl.fetch_unread_messages()
    }), 200

@mod.route("/api/v1/messages/sent", methods=["GET"])
def fetch_sent_messages():
    """
    This endpoint allows the user to view all the unread messages
    """
    return jsonify({
        "status": 200,
        "data": msgControl.fetch_sent_messages()
    }), 200

@mod.route("/api/v1/messages/<id>", methods=["GET"])
def fetch_specific_message(id):
    """
    This endpoint allows the user to fetch a specific message
    """
    try:
        id = int(id)
    except(ValueError, TypeError):
        return jsonify({
            "status": 405,
            "error": "Id should be an integer"
        }), 405
    message_exists = meth.is_existing_message_id(id)
    if not message_exists:
        return jsonify({
            "status": 404,
            "error": "Id {} not found".format(id)
        }), 404
    return jsonify({
        "status": 200,
        "data": msgControl.fetch_specific_message(id)
    }), 200

@mod.route("/api/v1/messages/<id>", methods=["DELETE"])
def delete_message(id):
    """
    This endpoint allows the user to delete a message
    """
    try:
        id = int(id)
    except(ValueError, TypeError):
        return jsonify({
            "status": 405,
            "error": "Id should be an integer"
        }), 405
    validate_delete = helper.message_delete_validation(id)
    if validate_delete != "Valid":
        return jsonify({
            "status": 404,
            "error": validate_delete
        }), 404
    return jsonify({
        "status": 200,
        "deleted data": msgControl.delete_message(id)
    }), 200