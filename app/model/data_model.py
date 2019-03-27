from datetime import datetime as dt
from app.model.db import Database
# from werkzeug.security import generate_hash_password, check_password_hash


class DataModel:
    """
    This class contains methods to query the database
    """
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.cur

    def signup(self, firstName, lastName, email, password):
        """
        Creates a new user
        """
        #Automaticaly generates user id
        query = ("""INSERT INTO users (firstName, lastName, email, password) VALUES ('{}','{}','{}','{}')""".format(firstName, lastName, email, password))
        self.cursor.execute(query)
        return "Successfully created user with email {}".format(email)

    def is_existing_user(self, email):
        """
        Checks if a user already exists
        """
        query = ("""SELECT * FROM users WHERE email = '{}'""".format(email))
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        if user:
            return user

    def is_existing_user_id(self, userId):
        """
        Checks if the user id exists
        """
        query = ("""SELECT * FROM users WHERE userId = '{}'""".format(userId))
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        if user:
            return user

    def is_genuine_password(self, email, password):
        """
        Checks if user password is correct
        """
        query = ("""SELECT password FROM users WHERE email = '{}'""".format(email))
        self.cursor.execute(query)
        pass_code = self.cursor.fetchone()
        if pass_code == password:
            return True
        return False

    def login(self, email, password):
        """
        This logs the user in given email and password
        """
        query = ("""SELECT * FROM users WHERE email = '{}' AND password = '{}'""".format(email, password))
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def is_existing_message_id(self, messageId):
        """
        This checks if a message id exists
        """
        query = ("""SELECT * FROM messages WHERE messageId = '{}'""".format(messageId))
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        if user:
            return user

    def create_message(self, subject, senderId, receiverId, message, status):
        """
        Creates a new message
        """
        createdOn = '{:%Y-%m-%d %H:%M}'.format(dt.now())
        query = ("""INSERT INTO messages (subject, senderId, receiverId, message, status, createdOn) VALUES ('{}','{}','{}','{}','{}','{}')""".format(subject, senderId, receiverId, message, status, createdOn))
        self.cursor.execute(query)
        return "Successfully create message"

    def fetch_received_messages(self, userId):
        """
        Fetches all mesages in the user's inbox
        """
        query = ("""SELECT * FROM messages WHERE receiverId = '{}'""".format(userId))
        self.cursor.execute(query)
        inbox = self.cursor.fetchall()
        if not inbox:
            return "Huh! You have not received any messages yet"
        return inbox

    def fetch_unread_messages(self, userId):
        """
        Fetches all the unread messages
        """
        status = "unread"
        query = ("""SELECT * FROM messages WHERE receiverId = '{}' AND status = '{}'""".format(userId, status))
        self.cursor.execute(query)
        unread = self.cursor.fetchall()
        if not unread:
            return "Oops! There are no unread message"
        return unread

    def fetch_sent_messages(self, userId):
        """
        To fetch all sent messages
        """
        query = ("""SELECT * FROM messages WHERE senderId = '{}'""".format(userId))
        self.cursor.execute(query)
        sent = self.cursor.fetchall()
        if not sent:
            return "Oh oh! It is lonely here. No sent mesages"
        return sent

    def fetch_specific_message(self, userId, messageId):
        """
        Fetches a specific email given the message id
        """
        query = ("""SELECT * FROM messages WHERE receiverId = '{}' OR senderId = '{}' AND messageId = '{}'""".format(userId, userId, messageId))
        self.cursor.execute(query)
        message = self.cursor.fetchone()
        if message:
            return message

    def delete_message(self, userId, messageId):
        """
        Deletes an email given the the email id
        """
        query = ("""DELETE FROM messages WHERE receiverId = '{}' OR senderId = '{}' AND messageId = '{}'""".format(userId, userId, messageId))
        self.cursor.execute(query)
        return "Message with id '{}' successfully deleted".format(messageId)    