import unittest
from flask import json
from app import app
from app.model.model import Model


class TestMessages(unittest.TestCase):
    """
    This tests the User endpoints
    """
    def setUp(self):
        self.app = app.test_client()
        self.model = Model()


    def tearDown(self):
        self.model.clear_data()
    
    def test_create_message_returns_error_if_request_missing_fields(self):
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greeting",
            "message": "Hi Eubule",
            "sendTo": "eubule@gmail.com"
        }))
        self.assertEqual(response.status_code, 400);

    def test_create_message_with_too_many_fields(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "subject": "greeting",
            "message": "Hi Eubule",
            "sendTo": "eubule@gmail.com",
            "status": "sent",
            "other": "something"
        }))
        self.assertIn("Too many arguments", str(response.data))

    def test_if_user_tries_to_create_message_providing_non_json_data(self):
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps([]))
        self.assertIn("Your request should be in json format", str(response.data))

    def test_if_user_tries_to_create_user_with_field_typos(self):
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greeting",
            "message": "Hi Eubule",
            "sendTa": "eubule@gmail.com",
            "status": "sent"
        }))
        self.assertIn("subject, message, sentTo and status missing is missing", str(response.data))

    def test_if_user_tries_to_create_user_providing_improper_data(self):
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": 1,
            "message": "Hi Eubule",
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        self.assertEqual(response.status_code, 417);
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "",
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        self.assertIn("Message cannot be empty", str(response.data));
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubulegmail.com",
            "status": "sent"
        }))
        self.assertIn("Email must be of format john123@gmail.com", str(response.data));
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubule@gmail.com",
            "status": "send"
        }))
        self.assertIn("Status must be either sent dreaft, unread or read", str(response.data));
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": 1,
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        self.assertIn("Message must be a string of characters", str(response.data));
    
    def test_if_user_can_successfuly_create_message(self):
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        self.assertEqual(response.status_code, 201)

    def test_if_user_can_successfully_fetch_all_messages(self):
        response = self.app.get("/api/v1/messages")
        self.assertTrue("Oops! It iss lonely here. No messages Yet", str(response.data))
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        response = self.app.get("/api/v1/messages")
        self.assertEqual(response.status, '200 OK')
    
    def test_if_user_can_fetch_all_unread_messages(self):
        response = self.app.get("/api/v1/messages/unread")
        self.assertTrue("Oops! There are no unread Messages here", str(response.data))
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubule@gmail.com",
            "status": "unread"
        }))
        response = self.app.get("/api/v1/messages/unread")
        self.assertEqual(response.status_code, 200)

    def test_if_user_can_fetch_all_sent_messages(self):
        response = self.app.get("/api/v1/messages/sent")
        self.assertTrue("Oh oh! There are no sent messages yet", str(response.data))
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        response = self.app.get("/api/v1/messages/sent")
        self.assertEqual(response.status_code, 200)

    def test_if_user_tries_to_fetch_a_non_existing_message(self):
        response = self.app.get("/api/v1/messages/2")
        self.assertEqual(response.status_code, 404)

    def test_if_user_tries_to_fetch_a_message_with_invalid_id(self):
        response = self.app.get("/api/v1/messages/hg")
        self.assertTrue("Id should be an integer", str(response.data))
        response = self.app.get("/api/v1/messages/0")
        self.assertTrue("Id must be an integer greater than 0", str(response.data))

    def test_if_user_can_fetch_a_specific_message(self):
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        response = self.app.get("/api/v1/messages/1")
        self.assertEqual(response.status_code, 200)

    def test_if_user_tries_to_delete_message_with_invalid_if(self):
        response = self.app.delete("/api/v1/messages/one")
        self.assertEqual(response.status_code, 405)
    
    def test_if_user_tries_to_delete_message_that_does_not_exisT(self):
        response = self.app.delete("/api/v1/messages/1")
        self.assertEqual(response.status_code, 404)

    def test_if_user_can_successfully_delete_a_message(self):
        response = self.app.post("/api/v1/messages", content_type="application/json", data=json.dumps({
            "subject": "greetings",
            "message": "Hi Eric",
            "sendTo": "eubule@gmail.com",
            "status": "sent"
        }))
        response = self.app.delete("/api/v1/messages/1")
        self.assertEqual(response.status_code, 200)
    