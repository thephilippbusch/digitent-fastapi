from app.postgres.postgres import PostgreSQL

from app.schemas.chatbot_answer_schema import ChatbotAnswerSchema

pgql_conn = PostgreSQL.connection()
pgql_cur = PostgreSQL.cursor()

class ChatbotAnswerManager:
    def check_admin(user_id: str) -> bool:
        try:
            req = (f"""
                SELECT admin FROM users
                WHERE _id = '{user_id}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchone()
            if res['admin']:
                return True
            return False
        except Exception as e:
            print(e)
            return False

    def add_answer(answer: ChatbotAnswerSchema, id: str):
        try:
            is_admin = ChatbotAnswerManager.check_admin(answer.created_by)
            if not is_admin:
                return False
            print(answer)
            if answer.responses:
                r = '{'
                for i in range(len(answer.responses)):
                    if (i+1) < len(answer.responses):
                        r += f'"{answer.responses[i]}", '
                    else:
                        r += f'"{answer.responses[i]}"'
                r += '}'
                req = (f"""
                    INSERT INTO chatbot_answers (_id, trigger, message, created_by, responses)
                    VALUES ('{id}', '{answer.trigger}', '{answer.message}', '{answer.created_by}', '{r}')
                """)
                print(req)
            else:
                req = (f"""
                    INSERT INTO chatbot_answers (_id, trigger, message, created_by)
                    VALUES ('{id}', '{answer.trigger}', '{answer.message}', '{answer.created_by}')
                """)
            pgql_cur.execute(req)
            pgql_conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_messages_by_creator(creator_id: str):
        try:
            req = (f"""
                SELECT * FROM chatbot_answers
                WHERE created_by = '{creator_id}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchall()
            
            if len(res) > 0:
                return res
            return None
        except Exception as e:
            print(e)
            return None

    def get_answer_by_trigger(trigger: str):
        try:
            req = (f"""
                SELECT * FROM chatbot_answers
                WHERE trigger = '{trigger}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchone()

            return res
        except Exception as e:
            print(e)
            return None
