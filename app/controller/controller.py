from app.model.model import Model


class UserController:
    """
    This class controls user model
    """
    def __init__(self):
        self.model = Model()

    def signup(self, firstName, lastName, email, password):
        """
        This method adds a new user
        """
        create = self.model.signup(firstName=firstName, lastName=lastName, email=email, password=password)
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
        This method helps the user to login
        """
        user = self.model.login(email=email, password=password)
        if user:
            return user

class MessageController:
    """
    This class controls the Message model
    """
    def __init__(self):
        self.model = Model()

    def create_message(self, subject, message, sendTo, status):
        """
        This controls the creation of a new message
        """
        create = self.model.create_message(subject=subject, message=message, sendTo=sendTo, status=status)
        return create

    def fetch_received_messages(self):
        """
        This method fetches all Received messages
        """
        emails = self.model.fetch_received_messages()
        return emails
    
    def fetch_unread_messages(self):
        """
        This method retrieves all the the unread emails
        """
        unread = self.model.fetch_unread_messages()
        return unread

    def fetch_sent_messages(self):
        """
        This method retrieves all the the sent emails
        """
        sent = self.model.fetch_sent_messages()
        return sent
    
    def fetch_specific_message(self, id):
        """
        This method fetches a specific email
        """
        msg = self.model.fetch_specific_message(id)
        return msg

    def is_existing_message_id(self, id):
        """
        This checks if a message id exists
        """
        msg = self.model.fetch_specific_message(id)
        return msg

    def delete_message(self, id):
        """
        This method deletes a message given a email id
        """
        message = self.model.delete_message(id=id)
        return message
