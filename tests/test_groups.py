import unittest
from flask import json
from app import app
from app.model.db import Database


class Testgroups(unittest.TestCase):
    """
    This tests the endpoints for groups
    """
    def setUp(self):
        self.app = app.test_client()
        self.db = Database()
        self.db.create_tables()


    def tearDown(self):
        self.db.delete_tables()

    def user1_token(self):

        response = self.app.post('/api/v2/auth/signup',content_type = 'json/application',\
         data=json.dumps({
            "firstName": "eubule",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
    
        token = json.loads(response.data)
        return token

    def user2_token(self):
    
        response = self.app.post('/api/v2/auth/signup',content_type = 'json/application',\
         data=json.dumps({
            "firstName": "malaba",
            "lastName": "Mashauri",
            "email": "malaba@gmail.com",
            "password": "malaba"
        }))
        response = self.app.post('/api/v2/auth/login',content_type = 'json/application',\
         data=json.dumps({
            "email": "malaba@gmail.com",
            "password": "malaba"
        }))
    
        token = json.loads(response.data)
        return token

    def test_create_group_returns_error_if_request_missing_fields(self):
    
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '\
        + token1['token']},content_type="application/json", data=json.dumps({
            "groupName": "greeting"
        }))
        self.assertEqual(response.status_code, 400);

    def test_create_group_with_too_many_fields(self):
    
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '\
        + token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software development",
            "other": "eubule@gmail.com",
        }))
        self.assertIn("Too many arguments", str(response.data))

    def test_if_user_tries_to_create_group_providing_non_json_data(self):
    
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '\
        + token1['token']},content_type="application/json", data=json.dumps([]))
        self.assertIn("Your request should be in json format", str(response.data))

    def test_if_user_tries_to_create_group_with_field_typos(self):
        
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']},content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRol": "Software development"
        }))
        self.assertIn("groupName or groupRole is missing. Check the spelling",\
         str(response.data))
    
    def test_if_user_tries_to_create_group_providing_improper_data(self):
    
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']},content_type="application/json", data=json.dumps({
            "groupName": "E",
            "groupRole": "Software development"
        }))
        self.assertIn("Name msut be at least 3 characters", str(response.data))

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": 1,
            "groupRole": "Software development"
        }))
        self.assertIn("Name should be a string of characters", str(response.data))

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": ""
        }))
        self.assertIn("Group Role cannot be empty",\
        str(response.data));

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": 1
        }))
        self.assertIn("Group Role must be a string of characters", str(response.data))

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))
        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))
        self.assertEqual(response.status_code, 409)

    def test_if_user_can_fetch_all_groups(self):
        
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))

        self.assertEqual(response.status_code, 201)

    def test_if_user_can_fetch_all_groups(self):
    
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))

        response = self.app.get("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']})
        self.assertEqual(response.status, '200 OK')

    def test_if_user_can_edit_group_name(self):

        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))

        response = self.app.patch("/api/v2/groups/1/name", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneer"
        }))
        
        self.assertEqual(response.status_code, 200)

    def test_if_user_group_name_edit_with_invalid_data(self):

        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))

        response = self.app.patch("/api/v2/groups/3/name", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneer"
        }))
        self.assertEqual(response.status_code, 404)

        response = self.app.patch("/api/v2/groups/1/name", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers"
        }))
        self.assertEqual(response.status_code, 409)

        token2 = self.user2_token()

        response = self.app.patch("/api/v2/groups/1/name", headers = {'Authorization': 'Bearer '+\
         token2['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneer"
        }))
        self.assertEqual(response.status_code, 401)

    def test_if_user_can_delete_a_group(self):

        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))
        response = self.app.delete("/api/v2/groups/1", headers = {'Authorization': 'Bearer '+\
         token1['token']})
        self.assertEqual(response.status_code, 200)
    
    def test_if_user_tries_to_delete_group_unsuccessfully(self):

        token1 = self.user1_token()

        response = self.app.delete("/api/v2/groups/3", headers = {'Authorization': 'Bearer '+\
         token1['token']})
        self.assertEqual(response.status_code, 404)

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))

        token2 = self.user2_token()

        response = self.app.delete("/api/v2/groups/1", headers = {'Authorization': 'Bearer '+\
         token2['token']})
        self.assertEqual(response.status_code, 401)

    def test_if_user_can_create_add_a_group_member(self):
        
        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))
        
        response = self.app.post("/api/v2/groups/1/users", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "userId": 1,
            "userRole": "admin"
        }))

        self.assertEqual(response.status_code, 201)

    def test_if_user_tries_to_add_user_to_group_with_invalid_credentials(self):

        token1 = self.user1_token()

        response = self.app.post("/api/v2/groups/3/users", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "userId": 1,
            "userRole": "admin"
        }))
        self.assertEqual(response.status_code, 404)

        response = self.app.post("/api/v2/groups", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "groupName": "Engeneers",
            "groupRole": "Software Developers"
        }))

        response = self.app.post("/api/v2/groups/1/users", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "userId": 3,
            "userRole": "admin"
        }))
        self.assertEqual(response.status_code, 404)

        response = self.app.post("/api/v2/groups/1/users", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "userId": 1,
            "userRole": "admini"
        }))
        self.assertEqual(response.status_code, 417)

        token2 = self.user2_token()

        response = self.app.post("/api/v2/groups/1/users", headers = {'Authorization': 'Bearer '+\
         token2['token']}, content_type="application/json", data=json.dumps({
            "userId": 2,
            "userRole": "admin"
        }))
        self.assertEqual(response.status_code, 401)

        response = self.app.post("/api/v2/groups/1/users", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "userId": 1,
            "userRole": "admin"
        }))
        response = self.app.post("/api/v2/groups/1/users", headers = {'Authorization': 'Bearer '+\
         token1['token']}, content_type="application/json", data=json.dumps({
            "userId": 1,
            "userRole": "admin"
        }))
        self.assertEqual(response.status_code, 409)
