from app.model.data_model import *
from app.validation.validation import *


class ViewHelper:
    """
    This class helps the view to for some validaions
    """
    def __init__(self):
        self.meth = DataModel()

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
            return "User with email {} already exist".format(email)
        return "Valid"

    def user_can_login(self, email, password):
        """
        This method checks if user can login
        """
        if is_valid_email(email) != "Valid":
            return is_valid_email(email)
        if is_valid_password(password) != "Valid":
            return is_valid_password(password)
        return "Valid"

    def message_validation(self, subject, senderId, receiverId, message, status):
        """
        This method Validates the message creation
        """
        if is_valid_subject(subject) != "Valid":
            return is_valid_subject(subject)
        if is_valid_message(message) != "Valid":
            return is_valid_message(message)
        if is_valid_id(receiverId) != "Valid":
            return is_valid_id(receiverId)
        if is_valid_status(status) != "Valid":
            return is_valid_status(status)

        if not self.meth.is_existing_user_id(receiverId):
            return "User with id {} does not exist".format(receiverId)
        return "Valid"

    def message_delete_validation(self, messageId):
        """
        This method checks if message with given id can be deleted
        """

        if not self.meth.is_existing_message_id(messageId):
            return "Message with id {} not found".format(messageId)
        return "Valid"

    def group_creation_validation(self, groupName, groupRole):
        """
        This checks if the data provided is valid before group creation
        """

        if is_valid_name(groupName) != "Valid":
            return is_valid_name(groupName)
        if is_valid_group_role(groupRole) != "Valid":
            return is_valid_group_role(groupRole)

        if self.meth.is_existing_group_name(groupName):
            return "Group with name {} already exist".format(groupName)
        return "Valid"
    
    def group_name_editing_validation(self, userId, groupId, groupName):
        """
        This checks if the data provided is valid before group name editing
        """

        if is_valid_name(groupName) != "Valid":
            return is_valid_name(groupName)

        if not self.meth.is_existing_group_id(groupId):
            return "Group with id {} does not exist".format(groupId)
        if not self.meth.is_group_owner(userId, groupId):
            return "You cannot edit a group you do not own"
        if self.meth.is_existing_group_name(groupName):
            return "Group with name {} already exist".format(groupName)
        return "Valid"