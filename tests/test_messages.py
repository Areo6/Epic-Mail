import unittest
from flask import json
from app import app
from app.model.db import Database


class TestMessages(unittest.TestCase):
    """
    This tests the Message endpoints
    """
    def setUp(self):
        self.app = app.test_client()
        self.db = Database()
        self.db.create_tables()


    def tearDown(self):
        self.db.delete_tables()

    def user_token(self):

        response = self.app.post('/api/v2/auth/signup',content_type = 'json/application',\
         data=json.dumps({
            "firstName": "eubule",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
    
        token = json.loads(response.data)
        return token
    
    def test_create_message_returns_error_if_request_missing_fields(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '\
        + token['token']},content_type="application/json", data=json.dumps({
            "subject": "greeting",
            "message": "Hi Eubule",
            "receiverId": "eubule@gmail.com"
        }))
        self.assertEqual(response.status_code, 400);

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '\
        + token['token']},content_type="application/json",
         data=[])
        self.assertEqual(response.status_code, 400);

    def test_create_message_with_too_many_fields(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '\
        + token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greeting",
            "message": "Hi Eubule",
            "receiverId": "eubule@gmail.com",
            "status": "sent",
            "other": "something"
        }))
        self.assertIn("Too many arguments", str(response.data))

    def test_if_user_tries_to_create_message_providing_non_json_data(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '\
        + token['token']},content_type="application/json", data=json.dumps([]))
        self.assertIn("Your request should be in json format", str(response.data))

    def test_if_user_tries_to_create_message_with_field_typos(self):
    
        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']},content_type="application/json", data=json.dumps({
            "subject": "greeting",
            "message": "Hi Eubule",
            "receiverIt": 1,
            "status": "sent"
        }))
        self.assertIn("subject, receiverId, message or status missing is missing",\
         str(response.data))

    def test_if_user_tries_to_create_user_providing_improper_data(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']},content_type="application/json", data=json.dumps({
            "subject": 1,
            "message": "Hi Eubule",
            "receiverId": 1,
            "status": "sent"
        }))
        self.assertIn("Subject must be a string of characters", str(response.data))

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "",
            "receiverId": 1,
            "status": "sent"
        }))
        self.assertIn("Message cannot be empty", str(response.data))

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": "one",
            "status": "sent"
        }))
        self.assertIn("Id must be an integer greater than 0", str(response.data))

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "send"
        }))
        self.assertIn("Status must be either sent draft, unread or read",\
        str(response.data));

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": 1,
            "receiverId": 1,
            "status": "sent"
        }))
        self.assertIn("Message must be a string of characters", str(response.data))

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi",
            "receiverId": 4,
            "status": "unread"
        }))
        self.assertEqual(response.status_code, 404)
    
    def test_if_user_can_successfuly_create_message(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "unread"
        }))
        self.assertEqual(response.status_code, 201)

    def test_if_user_can_successfully_fetch_all_messages(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "unread"
        }))
        response = self.app.get("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status, '200 OK')
    
    def test_if_user_can_fetch_all_unread_messages(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "unread"
        }))
        response = self.app.get("/api/v2/messages/unread", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_fetch_all_sent_messages(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "unread"
        }))
        response = self.app.get("/api/v2/messages/sent", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_fetch_all_receiverd_messages(self):
    
        token = self.user_token()

        response = self.app.post('/api/v2/auth/signup',content_type = 'json/application',\
         data=json.dumps({
            "firstName": "malaba",
            "lastName": "Mashauri",
            "email": "malaba@gmail.com",
            "password": "malaba"
        }))
        tkn = json.loads(response.data)

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Malaba",
            "receiverId": 2,
            "status": "unread"
        }))

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         tkn['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "unread"
        }))
        response = self.app.get("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 200)

    def test_if_user_tries_to_fetch_a_non_existing_message(self):

        token = self.user_token()

        response = self.app.get("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertTrue("Oops! It iss lonely here. No messages Yet", str(response.data))

        response = self.app.get("/api/v2/messages/2", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 404)

        response = self.app.get("/api/v2/messages/unread", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertTrue("Oops! There are no unread Messages here", str(response.data))

        response = self.app.get("/api/v2/messages/sent", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertTrue("Oh oh! There are no sent messages yet", str(response.data))

    def test_if_user_tries_to_fetch_a_message_with_invalid_id(self):

        token = self.user_token()

        response = self.app.get("/api/v2/messages/hg", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertTrue("Id should be an integer", str(response.data))

        response = self.app.get("/api/v2/messages/0", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertTrue("Id must be an integer greater than 0", str(response.data))

    def test_if_user_can_fetch_a_specific_message(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "unread"
        }))
        response = self.app.get("/api/v2/messages/1", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 200)

    def test_if_user_tries_to_delete_message_with_invalid_if(self):

        token = self.user_token()

        response = self.app.delete("/api/v2/messages/one", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 405)
    
    def test_if_user_tries_to_delete_message_that_does_not_exisT(self):

        token = self.user_token()

        response = self.app.delete("/api/v2/messages/1", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 404)

    def test_if_user_can_successfully_delete_a_message(self):

        token = self.user_token()

        response = self.app.post("/api/v2/messages", headers = {'Authorization': 'Bearer '+\
         token['token']}, content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "receiverId": 1,
            "status": "unread"
        }))
        response = self.app.delete("/api/v2/messages/1", headers = {'Authorization': 'Bearer '+\
         token['token']})
        self.assertEqual(response.status_code, 200)
    