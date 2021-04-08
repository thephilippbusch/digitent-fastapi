from app.postgres.postgres import PostgreSQL

from app.schemas.chat_schema import ChatSchema

pgql_conn = PostgreSQL.connection()
pgql_cur = PostgreSQL.cursor()

class ChatManager:
    def add_chat(chat: ChatSchema, id: str):
        try:
            check = (f"""
                SELECT * FROM chats
                WHERE user1_id = '{chat.user_1}'
                AND user2_id = '{chat.user_2}';
            """)
            pgql_cur.execute(check)
            check_res = pgql_cur.fetchone()
            print(check_res)
            
            if not check[0]:
                return False
            req = (f"""
                INSERT INTO chats (_id, user1_id, user2_id)
                VALUES ('{id}', '{chat.user_1}', '{chat.user_2}')
            """)
            pgql_cur.execute(req)
            pgql_conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_chats_by_user(user_id: str):
        try:
            req = (f"""
                SELECT * FROM chat
                WHERE user1_id = '{user_id}'
                OR user2_id = '{user_id}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchall()

            if len(res) > 0:
                return res
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_chat_by_user_contact(user_id: str, contact_id: str):
        try:
            req = (f"""
                SELECT _id from chats
                WHERE user1_id = '{user_id}' AND user2_id = '{contact_id}'
                OR user1_id = '{contact_id}' AND user2_id = '{user_id}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchone()
            print(res)
            if res:
                return {
                    "chat_id": res["_id"]
                }
            return None
        except Exception as e:
            print(e)
            return None