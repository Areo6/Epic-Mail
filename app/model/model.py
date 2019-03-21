class User:
    """This class provides model for Users"""
    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

class Message:
    """This class provides model for Messages"""
    def __init__(self, subject, message, sendTo, status):
        self.subject = subject
        self.message = message
        self.sendTo = sendTo
        self.status = status