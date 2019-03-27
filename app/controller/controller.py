from app.model.data_model import DataModel


class UserController:
    """
    This class controls user model
    """
    def __init__(self):
        self.model = DataModel()

    def signup(self, firstName, lastName, email, password):
        """
        This method adds a new user
        """
        create = self.model.signup(firstName, lastName, email, password)
        return create
    
    def is_existing_user(self, email):
        """
        This method returns the user if he exists
        """
        user = self.model.is_existing_user(email=email)
        if user:
            return user

    def login(self, email, password):
        """
        Logs the user in
        """
        user = self.model.login(email=email, password=password)
        if user:
            return user

class MessageController:
    """
    Controls the Message model
    """
    def __init__(self):
        self.model = DataModel()

    def create_message(self, subject, senderId, receiverId, message, status):
        """
        This controls the creation of a new message
        """
        create = self.model.create_message(subject, senderId, receiverId, message, status)
        return create

    def fetch_received_messages(self, userId):
        """
        Fetches all Received messages
        """
        emails = self.model.fetch_received_messages(userId)
        return emails
    
    def fetch_unread_messages(self, userId):
        """
        Retrieves all the the unread emails
        """
        unread = self.model.fetch_unread_messages(userId)
        return unread

    def fetch_sent_messages(self, userId):
        """
        This method retrieves all the the sent emails
        """
        sent = self.model.fetch_sent_messages(userId)
        return sent
    
    def fetch_specific_message(self, userId, messageId):
        """
        Fetches a specific email
        """
        msg = self.model.fetch_specific_message(userId, messageId)
        return msg

    def is_existing_message_id(self, messageId):
        """
        This checks if a message id exists
        """
        msg = self.model.is_existing_message_id(messageId)
        return msg

    def delete_message(self, userId, messageId):
        """
        This method deletes a message given a email id
        """
        message = self.model.delete_message(userId, messageId)
        return message
