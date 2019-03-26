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
            if os.environ["APP_SETTINGS"] == "TESTING":
                self.conn = psycopg2.connect(database="epicmail", user="postgres", password="postgres", host="localhost", port=5432)
                print("Connected to epicmail db")
            else:
                self.conn = psycopg2.connect(database=os.environ["DATABASE_NAME"], user=os.environ["DATABASE_USER"], password=os.environ["DATABASE_PASSWORD"], host=os.environ["DATABASE_HOST"], port=os.environ["DATABASE_PORT"])
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
                fistName VARCHAR(30) NOT NULL,
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
                groupName VARCHAR(30) NOT NULL,
                groupeRole VARCHAR(30) NOT NULL
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