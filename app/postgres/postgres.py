import psycopg2, psycopg2.extras
from decouple import config
import uuid
import os

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# HOST = config("postgres_host")
# PORT = config("postgres_port")
# DB = config("postgres_database")
# USER = config("postgres_user")

# conn = psycopg2.connect(
#     host=HOST,
#     port=PORT,
#     database=DB,
#     user=USER
# )
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

init_commands = (
    """
        CREATE TABLE IF NOT EXISTS users (
            _id VARCHAR(255) NOT NULL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            username VARCHAR(255),
            admin BOOLEAN NOT NULL DEFAULT 'f',
            contacts VARCHAR(255) []
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS chats (
            _id VARCHAR(255) NOT NULL PRIMARY KEY,
            user1_id VARCHAR(255) NOT NULL REFERENCES
                users(_id),
            user2_id VARCHAR(255) NOT NULL REFERENCES
                users(_id)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS chatbot_answers (
            _id VARCHAR(255) NOT NULL PRIMARY KEY,
            trigger TEXT NOT NULL,
            message TEXT NOT NULL,
            responses TEXT [],
            created_by VARCHAR(255) NOT NULL REFERENCES
                users(_id)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS messages (
            _id VARCHAR(255) NOT NULL PRIMARY KEY,
            message TEXT NOT NULL,
            from_user VARCHAR(255) NOT NULL REFERENCES
                users(_id),
            chat_id VARCHAR(255) NOT NULL REFERENCES
                chats(_id),
            date TIMESTAMP NOT NULL
        )
    """
)

for command in init_commands:
    cur.execute(command)

init_admin_req = ("""
    INSERT INTO users (_id, email, password, username, admin)
    VALUES ('admin', 'admin@praxi', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 't')
    ON CONFLICT 
    DO NOTHING;
""")
cur.execute(init_admin_req)

conn.commit()

class PostgreSQL:
    def connection():
        return conn

    def cursor():
        return cur
