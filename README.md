# Epic-Mail
[![Build Status](https://travis-ci.com/Eubule/Epic-Mail.svg?branch=ft-user-can-send-email-to-group-ch3-164879077)](https://travis-ci.com/Eubule/Epic-Mail)
[![Coverage Status](https://coveralls.io/repos/github/Eubule/Epic-Mail/badge.svg?branch=ch-test-endpoints-164848377)](https://coveralls.io/github/Eubule/Epic-Mail?branch=ch-test-endpoints-164848377)
[![Maintainability](https://api.codeclimate.com/v1/badges/39b05a4e7dc5545c7b14/maintainability)](https://codeclimate.com/github/Eubule/Epic-Mail/maintainability)

## DESCRIPTION

Epic Email is an email  web App that helps people share messages or information

## Link to Epic-mail on Github Pages

[Epic-Mail](https://eubule.github.io/Epic-Mail/)

## Link to Epic-Mail using data stuctures on Heroku

[Epic-Mail](https://epic-mail-malaba.herokuapp.com/api/v2/messages)

## Routes captured by Epic-Mail

 REQUEST | ROUTE | FUNCTIONALITY
 ------- | ----- | -------------
 **GET** | /api/v2/messages | Fetches all messages
 **POST** | /api/v2/messages | Posts a message
 **GET** | /api/v2/message/< messageId> | Fetches a specific message
 **GET** | /api/v2/messages/sent | Fetches all sent messages
 **GET** | /api/v2/messages/unread | Fetches all unread messages
 **DELETE** | /api/v2/message/< messageId> | Deletes a message
 **POST** | /api/v2/auth/signup | Creates a new User
 **POST** | /api/v2/auth/login | Logs in the user
 **POST** | /api/v2/groups | Creates a new group
 **GET** | /api/v2/groups | Fetches all groups
 **PATCH** | /api/v2/groups/< group-id>/nam | Edits group name
 **DELETE** | /api/v2/groups/< group-id> | Deletes a group
 **POST** | /api/v2/groups/< group-id>/users | Adds a user to a group
 **GET** | /api/v2/groups/< group-id>/users/< user-id> | Deletes a user from group
 **POST** | /api/v2/groups/< group-id>/emails | creates email for the group



## BUIT WITH

 * Flask-Python

## HOW TO RUN THE APPLICATION

 ### SETING UP THE ENVIRONMENT
 
 1. Clone this repository to your local PC

    **` git clone https://github.com/Eubule/Epic-Mail.git `** [here](https://github.com/Eubule/Epic-Mail)


 2. Create a virtual environment to run application specific dependencies

    **`$ virtualenv venv`**  To create a virtual environment separate from your system

    **`$ source venv/bin/activate`**   To activate you virtual environment

    **`$ pip install flask`**   To install the flask framework that will be used throughout

    **`$ pip freeze > requirements.txt`**   To install requirements useful when hosting the app on a remote server


 ### RUN THE APP

 1. To run the app

    **` python run.py `**

 2. To run tests

    **`  python -m pytest --cov app/ `**


## Author

**Malaba**

