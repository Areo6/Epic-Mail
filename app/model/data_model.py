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

    # def is_genuine_password(self, email, password):
    #     """
    #     Checks if user password is correct
    #     """
    #     query = ("""SELECT password FROM users WHERE email = '{}'""".format(email))
    #     self.cursor.execute(query)
    #     pass_code = self.cursor.fetchone()
    #     if pass_code == password:
    #         return True
    #     return False

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
        query = ("""SELECT * FROM messages WHERE (receiverId = '{}' OR senderId = '{}') AND messageId = '{}'""".format(userId, userId, messageId))
        self.cursor.execute(query)
        message = self.cursor.fetchone()
        if message:
            return message

    def delete_message(self, userId, messageId):
        """
        Deletes an email given the the email id
        """
        query = ("""DELETE FROM messages WHERE senderId = '{}' AND messageId = '{}'""".format(userId, messageId))
        self.cursor.execute(query)
        return "Message with id '{}' successfully deleted".format(messageId)

    def create_group(self, userId, groupName, groupRole):
        """
        Creates a group owned by the current user
        """
        query = ("""INSERT INTO groups (groupowner, groupName, groupRole) VALUES ('{}','{}','{}')""".format(userId, groupName, groupRole))
        self.cursor.execute(query)
        return "Successfully create a group"

    def fetch_all_groups(self):
        """
        Fetches all group records
        """
        query = ("""SELECT * FROM groups;""")
        self.cursor.execute(query)
        groups = self.cursor.fetchall()
        if not groups:
            return "Ooh! It is cold in here. No groups yet"
        return groups
    
    def edit_group_name(self, userId, groupId, groupName):
        """
        Edits a group name owned by the current user
        """
        query = ("""UPDATE groups SET groupName ='{}' WHERE groupId = '{}' AND groupowner = '{}'""".format(groupName, groupId, userId))
        self.cursor.execute(query)
        return "Successfully edited the group name"

    def is_group_owner(self, userId, groupId):
        """
        Checks if the user with given id is a group owner
        """
        query = ("""SELECT * FROM groups WHERE groupId = '{}' AND groupowner = '{}'""".format(groupId, userId))
        self.cursor.execute(query)
        group = self.cursor.fetchone()
        return group
    
    def is_existing_group_id(self, groupId):
        """
        This checks if a group id exists
        """
        query = ("""SELECT * FROM groups WHERE groupId = '{}'""".format(groupId))
        self.cursor.execute(query)
        group = self.cursor.fetchone()
        if group:
            return group

    def is_existing_group_name(self, groupName):
        """
        Checks if a group name already exists
        """
        query = ("""SELECT * FROM groups WHERE groupName = '{}'""".format(groupName))
        self.cursor.execute(query)
        group = self.cursor.fetchone()
        if group:
            return group

    def delete_group(self, userId, groupId):
        """
        Deletes group owned by userId
        """
        query = ("""DELETE FROM groups WHERE groupId = '{}' AND groupowner = '{}'""".format(groupId, userId))
        self.cursor.execute(query)
        return "Group with id '{}' successfully deleted".format(groupId)

    def add_group_member(self, groupId, userId, userRole):
        """
        Adds a member to the group
        """
        query = ("""INSERT INTO group_members (groupId, userId, userRole) VALUES ('{}','{}','{}')""".format(groupId, userId, userRole))
        self.cursor.execute(query)
        return "Successfully added member"
    
    def is_existing_member_id(self, userId):
        """
        Checks if a member exists given the id
        """
        query = ("""SELECT * FROM group_members WHERE userId = '{}'""".format(userId))
        self.cursor.execute(query)
        member = self.cursor.fetchone()
        if member:
            return member

    def delete_member(self, userId):
        """
        Deletes user from a group
        """
        query = ("""DELETE FROM group_members WHERE userId = '{}'""".format(userId))
        self.cursor.execute(query)
        return "Member with id '{}' successfully deleted".format(userId)

    def create_group_message(self, subject, senderId, groupId, message, status):
        """
        Creates a message and sends it to the group
        """
        createdOn = '{:%Y-%m-%d %H:%M}'.format(dt.now())
        query = ("""INSERT INTO group_messages (subject, senderId, groupId, message, status, createdOn) VALUES ('{}','{}','{}','{}','{}','{}')""".format(subject, senderId, groupId, message, status, createdOn))
        self.cursor.execute(query)
        return "Successfully create message"