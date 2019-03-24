from app.datastructure.ds_methods import DSMethods
from app.model.model import *


class UserController:
    """
    This class controls user model
    """
    def __init__(self):
        self.dsMeth = DSMethods()

    def signup(self, firstName, lastName, email, password):
        """
        This method adds a new user
        """
        user = User(firstName=firstName, lastName=lastName, email=email, password=password)
        create = self.dsMeth.signup(firstName=firstName, lastName=lastName, email=email, password=password)
        return create
    
    def is_existing_user(self, email):
        """
        This method returns the user if he exists
        """
        user = self.dsMeth.is_existing_user(email=email)
        if user:
            return user

    def login(self, email, password):
        """
        This method helps the user to login
        """
        user = self.dsMeth.login(email=email, password=password)
        if user:
            return user

class MessageController:
    """
    This class controls the Message model
    """
    def __init__(self):
        self.dsMeth = DSMethods()

    def create_message(self, subject, message, sendTo, status):
        """
        This controls the creation of a new message
        """
        msg = Message(subject=subject, message=message, sendTo=sendTo, status=status)
        create = self.dsMeth.create_message(subject=subject, message=message, sendTo=sendTo, status=status)
        return create

    def fetch_received_messages(self):
        """
        This method fetches all Received messages
        """
        emails = self.dsMeth.fetch_received_messages()
        return emails
    
    def fetch_unread_messages(self):
        """
        This method retrieves all the the unread emails
        """
        unread = self.dsMeth.fetch_unread_messages()
        return unread

    def fetch_sent_messages(self):
        """
        This method retrieves all the the sent emails
        """
        sent = self.dsMeth.fetch_sent_messages()
        return sent
    
    def fetch_specific_message(self, id):
        """
        This method fetches a specific email
        """
        msg = self.dsMeth.fetch_specific_message(id)
        return msg

    def delete_message(self, id):
        """
        This method deletes a message given a email id
        """
        message = self.dsMeth.delete_message(id=id)
        return message

