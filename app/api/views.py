from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.validation.validation import *
from app.validation.view_helper import *
from app.controller.controller import *
import datetime


mod = Blueprint('api', __name__)
userControl = UserController()
msgControl = MessageController()
helper = ViewHelper()

@mod.route('/api/v2/auth/signup', methods = ['POST'])
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
    if not "firstName" in data or not "lastName" in data or not "email" in data or not "password" in data:
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

@mod.route("/api/v2/auth/login", methods = ["POST"])
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

@mod.route("/api/v2/messages", methods= ["POST"])
@jwt_required
def create_message():
    """
    This endpoint allows the creation of a message
    """
    user_id = get_jwt_identity()["userid"]
    user_id = int(user_id)
    print(user_id)
    
    try:
        json.loads(request.get_data())
    except(ValueError, TypeError):
        return jsonify({
            "status": 400,
            "error": "Json data missing"
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
            "error": "Missing fields. Either subject, receiverId, message and status missing"
            }),400
    if len(data) > 4:
        return jsonify({
            "status": 414,
            "error": "Too many arguments. Only subject, receiverId, message and status missing are required"
            }),414
    if not "subject" in data or not "receiverId" in data or not "message" in data or not "status" in data:
        return jsonify({
            "status": 400,
            "error": "subject, receiverId, message or status missing is missing. Check the spelling"
        }), 400

    valid_message = helper.message_validation(data['subject'], user_id, data['receiverId'], data['message'], data['status'])

    if valid_message != "Valid":
        return jsonify({
            "status": 417,
            "error": valid_message
        }), 417

    message = msgControl.create_message(data['subject'], user_id, data['receiverId'], data['message'], data['status'])

    return jsonify({
        "status": 201,
        "data": data
    }), 201

@mod.route("/api/v2/messages", methods=["GET"])
@jwt_required
def fetch_received_messages():
    """
    This endpoint allows the user to view all messages
    """
    user_id = get_jwt_identity()["userid"]

    return jsonify({
        "status": 200,
        "data": msgControl.fetch_received_messages(user_id)
    }), 200

@mod.route("/api/v2/messages/unread", methods=["GET"])
@jwt_required
def fetch_unread_messages():
    """
    This endpoint allows the user to view all the unread messages
    """
    user_id = get_jwt_identity()["userid"]

    return jsonify({
        "status": 200,
        "data": msgControl.fetch_unread_messages(user_id)
    }), 200

@mod.route("/api/v2/messages/sent", methods=["GET"])
@jwt_required
def fetch_sent_messages():
    """
    This endpoint allows the user to view all the unread messages
    """
    user_id = get_jwt_identity()["userid"]

    return jsonify({
        "status": 200,
        "data": msgControl.fetch_sent_messages(user_id)
    }), 200

@mod.route("/api/v2/messages/<id>", methods=["GET"])
@jwt_required
def fetch_specific_message(id):
    """
    This endpoint allows the user to fetch a specific message
    """
    user_id = get_jwt_identity()["userid"]

    try:
        id = int(id)
    except(ValueError, TypeError):
        return jsonify({
            "status": 405,
            "error": "Message Id should be an integer"
        }), 405

    message_exists = msgControl.is_existing_message_id(id)
    if not message_exists:
        return jsonify({
            "status": 404,
            "error": "Message with Id {} not found".format(id)
        }), 404

    return jsonify({
        "status": 200,
        "data": msgControl.fetch_specific_message(user_id, id)
    }), 200

@mod.route("/api/v2/messages/<id>", methods=["DELETE"])
@jwt_required
def delete_message(id):
    """
    This endpoint allows the user to delete a message
    """
    user_id = get_jwt_identity()["userid"]

    try:
        id = int(id)
    except(ValueError, TypeError):
        return jsonify({
            "status": 405,
            "error": "Message Id should be an integer"
        }), 405

    print(id)
    validate_delete = helper.message_delete_validation(id)
    if validate_delete != "Valid":
        return jsonify({
            "status": 404,
            "error": validate_delete
        }), 404

    return jsonify({
        "status": 200,
        "deleted data": msgControl.delete_message(user_id, id)
    }), 200