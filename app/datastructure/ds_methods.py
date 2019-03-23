from datetime import datetime as dt
# from werkzeug.security import generate_hash_password, check_password_hash


users = []
messages = []
class DSMethods:
    """
    This class contains methods to query the datastructure
    """
    def signup(self, firstName, lastName, email, password):
        """
        This methods create a new user
        """
        #Automaticaly generates user id
        id = len(users) + 1

        user = {
            'id': id,
            'email': email,
            'fistName': firstName,
            'lastName': lastName,
            'password': password
        }
        users.append(user)
        return user

    def is_existing_user(self, email):
        """
        Checks if a user already exists
        """
        user = [user for user in users if user['email'] == email]
        if len(user) != 0:
            return user[0]

    def is_existing_user_id(self, id):
        """
        Checks if the user id exists
        """
        user = [user for user in users if users['id'] == id]
        if len(user) != 0:
            return True

    def is_genuine_password(self, email, password):
        """
        Checks if user password is correct
        """
        user = [user for user in users if user['email'] == email and user['password'] == password]
        if user:
            return True

    def login(self, email, password):
        """
        This logs the user in given email and password
        """
        user = [user for user in users if user['email'] == email and user['password'] == password]
        return user

    def is_existing_message_id(self, id):
        """
        This checks if a message id exists
        """
        message = [message for message in messages if message['id'] == id]
        if len(message) != 0:
            return message

    def create_message(self, subject, message, sendTo, status):
        """
        Creates a new message
        """
        id = len(messages) + 1
        
        #Picks the current date and time
        createdOn = '{:%Y-%m-%d %H:%M}'.format(dt.now())

        msg = {
            'id': id,
            'subject': subject,
            'message': message,
            'sendTo': sendTo,
            'status': status,
            'createdOn': createdOn
        }

        messages.append(msg)
        return msg

    def fetch_received_messages(self):
        """
        This method fetch all mesages in the inbox
        """
        if len(messages) == 0:
            return "Oops! It's lonely here. No messages Yet"
        return messages

    def fetch_unread_messages(self):
        """
        Fetches all the unread messages
        """
        message = [message for message in messages if message['status'] == 'unread']
        if len(message) != 0:
            return message
        return "Oops! There are no unread Messages here"

    def fetch_sent_messages(self):
        """
        To fetch all sent messages
        """
        message = [message for message in messages if message['status'] == 'sent']
        if len(message) != 0:
            return message
        return "Oh oh! There are no sent messages yet"

    def fetch_specific_message(self, id):
        """
        Fetches a specific email given the message id
        """
        message = [message for message in messages if message['id'] == id]
        if len(message) != 0:
            return message

    def delete_message(self, id):
        """
        This method deletes an email even the the email id
        """
        message = [message for message in messages if message['id'] == id]
        if len(message) != 0:
            messages.remove(message[0])
            return message[0]  