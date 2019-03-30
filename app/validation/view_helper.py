from app.model.data_model import *
from app.validation.validation import *


class ViewHelper:
    """
    This class helps the view to for some validaions
    """
    def __init__(self):
        self.meth = DataModel()
        self.status = 200

    def user_signup_validation(self, firstName, lastName, email, password):
        """
        This method helps validate the user
        """
        if is_valid_name(firstName) != "Valid":
            self.status = 417
            return is_valid_name(firstName)
        if is_valid_name(lastName) != "Valid":
            self.status = 417
            return is_valid_name(lastName)
        if is_valid_email(email) != "Valid":
            self.status = 417
            return is_valid_email(email)
        if is_valid_password(password) != "Valid":
            self.status = 417
            return is_valid_password(password)

        if self.meth.is_existing_user(email):
            self.status = 409
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
            self.status = 417
            return is_valid_subject(subject)
        if is_valid_message(message) != "Valid":
            self.status = 417
            return is_valid_message(message)
        if is_valid_id(receiverId) != "Valid":
            self.status = 417
            return is_valid_id(receiverId)
        if is_valid_status(status) != "Valid":
            self.status = 417
            return is_valid_status(status)

        if not self.meth.is_existing_user_id(receiverId):
            self.status = 404
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
            self.status = 417
            return is_valid_name(groupName)
        if is_valid_group_role(groupRole) != "Valid":
            self.status = 417
            return is_valid_group_role(groupRole)

        if self.meth.is_existing_group_name(groupName):
            self.status = 409
            return "Group with name {} already exist".format(groupName)
        return "Valid"
    
    def group_name_editing_validation(self, userId, groupId, groupName):
        """
        This checks if the data provided is valid before group name editing
        """

        if is_valid_name(groupName) != "Valid":
            self.status = 417
            return is_valid_name(groupName)

        if not self.meth.is_existing_group_id(groupId):
            self.status = 404
            return "Group with id {} does not exist".format(groupId)
        if not self.meth.is_group_owner(userId, groupId):
            self.status = 401
            return "You cannot edit a group you do not own"
        if self.meth.is_existing_group_name(groupName):
            self.status = 409
            return "Group with name {} already exist".format(groupName)
        return "Valid"

    def group_delete_validation(self, userId, groupId):
        """
        Checks if group with given id can be deleted
        """

        if not self.meth.is_existing_group_id(groupId):
            self.status = 404
            return "Group with id {} does not exist".format(groupId)
        if not self.meth.is_group_owner(userId, groupId):
            self.status = 401
            return "You cannot delete a group you do not own"
        return "Valid"

    def group_member_validation(self, ownerId, groupId, userId, userRole):
        """
        Validates a group member before adding him to a group
        """
        if not self.meth.is_existing_group_id(groupId):
            self.status = 404
            return "Group with id {} does not exist".format(groupId)

        if not self.meth.is_group_owner(ownerId, groupId):
            self.status = 401
            return "You cannot add a member to a group you do not own"

        if not self.meth.is_existing_user_id(userId):
            self.status = 404
            return "User with id {} does not exist".format(userId)

        if is_valid_user_role(userRole) != "Valid":
            self.status = 417
            return is_valid_user_role(userRole)  
        
        if self.meth.is_existing_member_id(userId):
            self.status = 409
            return "User with Id {} already exists".format(userId)

        return "Valid"  

    def delete_member_validation(self, ownerId, userId, groupId):
        """
        Checks if group with given id can be deleted
        """

        if is_valid_id(userId) != "Valid":
            self.status = 417
            return is_valid_id(userId)
        if is_valid_id(groupId) != "Valid":
            self.status = 417
            return is_valid_id(groupId)
        
        if not self.meth.is_existing_group_id(groupId):
            self.status = 404
            return "Group with id {} does not exist".format(groupId)
        if not self.meth.is_existing_member_id(userId):
            self.status = 404
            return "User with Id {} not found in the group".format(userId)
        if not self.meth.is_group_owner(ownerId, groupId):
            self.status = 401
            return "You cannot delete a group you do not own"

        return "Valid"

    def group_message_validation(self, subject, senderId, groupId, message, status):
        """
        This method Validates the group message creation
        """
        if is_valid_subject(subject) != "Valid":
            self.status = 417
            return is_valid_subject(subject)
        if is_valid_message(message) != "Valid":
            self.status = 417
            return is_valid_message(message)
        if is_valid_id(groupId) != "Valid":
            self.status = 417
            return is_valid_id(groupId)
        if is_valid_status(status) != "Valid":
            self.status = 417
            return is_valid_status(status)

        if not self.meth.is_existing_group_id(groupId):
            self.status = 404
            return "Group with id {} does not exist".format(groupId)
        return "Valid"