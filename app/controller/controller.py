from app.datastructure.ds_methods import DSMethods
from app.model.model import *


dsMeth = DSMethods()

class UserController:
    """
    This class controls user model
    """
    def signup(self, firstName, lastName, email, password):
        """
        This method adds a new user
        """
        user = User(firstName=firstName, lastName=lastName, email=email, password=password)
        create = dsMeth.signup(firstName=firstName, lastName=lastName, email=email, password=password)
        return create
    
    def is_existing_user(self, email):
        """
        This method returns the user if he exists
        """
        user = dsMeth.is_existing_user(email=email)
        if user:
            return user

    def login(self, email, password):
        """
        This method helps the user to login
        """
        user = dsMeth.login(email=email, password=password)
        if user:
            return user

class MessageController:
    """
    This class controls the Message model
    """
    def create_message(self, subject, message, sendTo, status):
        """
        This controls the creation of a new message
        """
        msg = Message(subject=subject, message=message, sendTo=sendTo, status=status)
        create = dsMeth.create_message(subject=subject, message=message, sendTo=sendTo, status=status)
        return create

    def fetch_received_messages(self):
        """
        This method fetches all Received messages
        """
        emails = dsMeth.fetch_received_messages()
        return emails
    
    def fetch_unread_emails(self):
        """
        This method retrieves all the the unread emails
        """
        unread = dsMeth.fetch_unread_messages()
        return unread
    
    def fetch_specific_message(self, id):
        """
        This method fetches a specific email
        """
        unread = dsMeth.fetch_specific_message()
        return unread

    def delete_message(self, id):
        """
        This method deletes a message given a email id
        """
        message = dsMeth.delete_message(id=id)
        return message

