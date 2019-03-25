import re


def is_valid_name(name):
    if not isinstance(name, str):
        return "Name should be a string of characters"
    if len(name.strip()) == 0:
        return "Name cannot be empty"
    if len(name.strip()) < 3:
        return "Name msut be at least 3 characters"
    patern = re.match('^[^.]*[a-zA-Z]$', name)
    if not patern:
        return "Name must not contain a special character"
    return "Valid"

def is_valid_email(email):
    is_valid = re.search(r"[\w-]+@[\w-]+\.+", email)
    if not is_valid:
        return "Email must be of format john123@gmail.com"
    return "Valid"

def is_valid_status(status):
    if status in ["sent", "read", "draft", "unread"]:
        return "Valid"
    return "Status must be either sent dreaft, unread or read"

def is_valid_password(password):
    if not isinstance(password, str):
        return "Password must be a string of characters"
    if len(password) < 6:
        return "Password must be at least 3 characters long"
    return "Valid"

def is_valid_id(id):
    if not isinstance(id, int) or id < 1:
        return "Id must be an integer greater than 0"
    return "Valid"

def is_valid_subject(subject):
    if not isinstance(subject, str):
        return "Subject must be a string of characters"
    return "Valid"

def is_valid_message(message):
    if not isinstance(message, str):
        return "Message must be a string of characters"
    if len(message.strip()) == 0:
        return "Message cannot be empty"
    return "Valid"
