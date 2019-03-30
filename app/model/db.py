import os 
import psycopg2
import psycopg2.extras as ex
from pprint import pprint


class Database():
    """
    Creates a connection to the database
    """
    def __init__(self):
        try:
            if os.getenv("APP_SETTINGS") == "TESTING":
                con =  'epic_test'
                print("Connected to epic_test db")
            else:
                con = 'epicmail'
            self.conn = psycopg2.connect(database="d7fntpjgl69u3g", user="alsosjdguvcbxt", password="d0c79d416cead2f00b683f43036a4b897c0f94af3aa774078d8fb1cb44e073dd", host="ec2-54-197-232-203.compute-1.amazonaws.com", port="5432")

            self.conn.autocommit = True
            self.cur = self.conn.cursor(cursor_factory=ex.RealDictCursor)
        except Exception as exc:
            pprint("Database Connection error: "+str(exc))

    def create_tables(self):
        """
        This method creates the tables if they did not exist in the database
        """
        commands = (
            """CREATE TABLE IF NOT EXISTS users(
                userId SERIAL PRIMARY KEY,
                firstName VARCHAR(30) NOT NULL,
                lastName VARCHAR(30) NOT NULL,
                email VARCHAR(30) NOT NULL,
                password VARCHAR(30) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS messages(
                messageId SERIAL PRIMARY KEY,
                subject VARCHAR(50),
                senderId SMALLINT NOT NULL REFERENCES users(userId) ON UPDATE CASCADE ON DELETE CASCADE,
                receiverId SMALLINT NOT NULL REFERENCES users(userId) ON UPDATE CASCADE ON DELETE CASCADE,
                message VARCHAR NOT NULL,
                status VARCHAR(10) NOT NULL,
                createdOn VARCHAR(30)
            )""",
            """CREATE TABLE IF NOT EXISTS groups(
                groupId SERIAL PRIMARY KEY,
                groupowner SMALLINT NOT NULL REFERENCES users(userId) ON UPDATE CASCADE ON DELETE CASCADE,
                groupName VARCHAR(30) NOT NULL,
                groupRole VARCHAR(30) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS group_members(
                Id SERIAL PRIMARY KEY,
                groupId SMALLINT NOT NULL REFERENCES groups(groupId) ON UPDATE CASCADE ON DELETE CASCADE,
                userId SMALLINT NOT NULL REFERENCES users(userId) ON UPDATE CASCADE ON DELETE CASCADE,
                userRole VARCHAR(30) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS group_messages(
                messageId SERIAL PRIMARY KEY,
                subject VARCHAR(50),
                senderId SMALLINT NOT NULL REFERENCES users(userId) ON UPDATE CASCADE ON DELETE CASCADE,
                groupId SMALLINT NOT NULL REFERENCES groups(groupId) ON UPDATE CASCADE ON DELETE CASCADE,
                message VARCHAR NOT NULL,
                status VARCHAR(10) NOT NULL,
                createdOn VARCHAR(30)
            )""",
        )
        for command in commands:
            try:
                self.cur.execute(command)
            except(Exception, psycopg2.DatabaseError) as error:
                pprint(error)

    def delete_tables(self):
        """
        This method is used to drop all the tables in the database
        """
        queries = ("""DROP TABLE IF EXISTS group_messages CASCADE""",
            """DROP TABLE IF EXISTS group_members CASCADE""",
            """DROP TABLE IF EXISTS groups CASCADE""",
            """DROP TABLE IF EXISTS messages CASCADE""",
            """DROP TABLE IF EXISTS users CASCADE""")
        for query in queries:
            self.cur.execute(query)