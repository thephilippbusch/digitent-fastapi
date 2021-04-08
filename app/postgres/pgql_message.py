from app.postgres.postgres import PostgreSQL

from app.schemas.message_schema import MessageSchema

pgql_conn = PostgreSQL.connection()
pgql_cur = PostgreSQL.cursor()

class MessageManager:
    def add_message(message: MessageSchema, id: str):
        try:
            req = (f"""
                INSERT INTO messages (_id, message, from_user, chat_id)
                VALUES ('{id}', '{message.message}', '{message.from_user}', '{message.chat_id}')
            """)
            pgql_cur.execute(req)
            pgql_conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_messages_by_chat(chat_id: str):
        try:
            req = (f"""
                SELECT * FROM messages
                WHERE chat_id = '{chat_id}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchall()
            
            return res
        except Exception as e:
            print(e)
            return None
