from app.datastructure.ds_methods import *
from app.validation.validation import *


class ViewHelper:
    """
    This class helps the view to for some validaions
    """
    def __init__(self):
        self.meth = DSMethods()

    def user_signup_validation(self, firstName, lastName, email, password):
        """
        This method helps validate the user
        """
        if is_valid_name(firstName) != "Valid":
            return is_valid_name(firstName)
        if is_valid_name(lastName) != "Valid":
            return is_valid_name(lastName)
        if is_valid_email(email) != "Valid":
            return is_valid_email(email)
        if is_valid_password(password) != "Valid":
            return is_valid_password(password)
        if self.meth.is_existing_user(email):
            return "User with name {} already taken".format(email)
        return "Valid"

    def user_can_login(self, email, password):
        """
        This method checks if user can login
        """
        if is_valid_email(email) != "Valid":
            return is_valid_email(email)
        if is_valid_password(password) != "Valid":
            return is_valid_password(password)
        if not self.meth.is_existing_user(email):
            return "User with email {} does not exist".format(email)
        if not self.meth.is_genuine_password(email, password):
            return "Your password is incorrect. Please try again"
        return "Valid"

    def message_validation(self, subject, message, sendTo, status):
        """
        This method Validates the message creation
        """
        if is_valid_subject(subject) != "Valid":
            return is_valid_subject(subject)
        if is_valid_message(message) != "Valid":
            return is_valid_message(message)
        if is_valid_email(sendTo) != "Valid":
            return is_valid_email(sendTo)
        if is_valid_status(status) != "Valid":
            return is_valid_status(status)
        return "Valid"

    def message_delete_validation(self, id):
        """
        This method checks if message with given id can be deleted
        """
        if is_valid_id(id) != "Valid":
            return is_valid_id(id)
        if not self.meth.is_existing_message_id(id):
            return "Message with id {} not found".format(id)
        return "Valid"