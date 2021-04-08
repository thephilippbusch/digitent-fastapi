from app.postgres.postgres import PostgreSQL

from app.schemas.user_schema import UserSchema, UserLoginSchema, AddAdminSchema

pgql_conn = PostgreSQL.connection()
pgql_cur = PostgreSQL.cursor()

class UserManager:
    def insert_user(user: UserSchema, id: str):
        try:
            req = (f"""
                INSERT INTO users (_id, email, password, username, admin)
                VALUES ('{id}', '{user.email}', '{user.password}', '{user.username}', 'f');
            """)

            pgql_cur.execute(req)

            pgql_conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def check_login(user_login: UserLoginSchema):
        try:
            req = (f"""
                SELECT * FROM users
                WHERE email = '{user_login.email}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchone()
            pgql_conn.commit()
            print(res)
            if not res:
                return {
                    "message": f"No user with email '{user_login.email}' found",
                    "successful": False
                }
            if res["password"] != user_login.password:
                return {
                    "message": "Wrong Password",
                    "successful": False
                }
            return {
                "user": {
                    "_id": res["_id"],
                    "email": res["email"],
                    "username": res["username"],
                    "admin": res["admin"]
                },
                "successful": True
            }
        except Exception as e:
            print(e)
            return {
                "message": "Error at /pgql_user: 'def check_user'",
                "successful": False
            }

    def make_admin(data: AddAdminSchema):
        try:
            is_admin_req = (f"""
                SELECT admin FROM users
                WHERE _id = '{data.admin_id}';
            """)
            pgql_cur.execute(is_admin_req)
            is_admin = pgql_cur.fetchone()
            if is_admin["admin"]:
                make_admin_req = (f"""
                    UPDATE users
                    SET admin = 't'
                    WHERE _id = '{data.user_id}'
                    RETURNING *;
                """)
                pgql_cur.execute(make_admin_req)
                res = pgql_cur.fetchone()
                pgql_conn.commit()
                return {
                    "successful": True,
                    "message": "Successful",
                    "data": res
                }
            else:
                return {
                    "successful": False,
                    "message": "Current user is no Admin",
                }
        except Exception as e:
            print(e)
            return {
                "successful": False,
                "message": "Error at /pgql_user: 'def register_admin'",
            }

    def get_user_by_mail(email: str):
        try:
            req = (f"""
                SELECT * FROM users
                WHERE email = '{email}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchone()
            pgql_conn.commit()

            if len(res) != 0:
                return {
                    "_id": res["_id"],
                    "email": res["email"],
                    "password": res["password"],
                    "username": res["username"],
                    "admin": res["admin"]
                }

            return None
        except Exception as e:
            print(e)
            return None

    def get_user_by_id(id: str):
        try:
            req = (f"""
                SELECT * FROM users
                WHERE _id = '{id}';
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchone()
            pgql_conn.commit()

            if res:
                return {
                    "_id": res["_id"],
                    "email": res["email"],
                    "password": res["password"],
                    "username": res["username"],
                    "admin": res["admin"]
                }

            return None
        except Exception as e:
            print(e)
            return None

    def get_contact_list(user_id: str):
        try:
            req = (f"""
                SELECT contacts FROM users
                WHERE _id = '{user_id}';
            """)
            pgql_cur.execute(req)
            contacts = pgql_cur.fetchone()
            if contacts["contacts"]:    
                res = []
                for contact in contacts["contacts"]:
                    contact_detail_query = (f"""
                        SELECT username, email, _id FROM users
                        WHERE _id = '{contact}';
                    """)
                    pgql_cur.execute(contact_detail_query)
                    contact_detail = pgql_cur.fetchone()
                    res.append({
                        "username": contact_detail["username"],
                        "email": contact_detail["email"],
                        "user_id": contact_detail["_id"]
                    })
                return res
            else:
                return {
                    "status": 404,
                    "message": "No contacts found"
                }
        except Exception as e:
            print(e)
            return None

    def add_contact(user_id: str, contact_mail: str):
        try:
            contact_query = (f"""
                SELECT _id FROM users
                WHERE email = '{contact_mail}';
            """)
            pgql_cur.execute(contact_query)
            contact_id = pgql_cur.fetchone()
            if not contact_id["_id"]:
                return {
                "successful": False,
                "message": "User not found"
            }

            print("@ add_contact:")
            existing_contacts_query = (f"""
                SELECT contacts FROM users
                WHERE _id = '{user_id}';
            """)
            pgql_cur.execute(existing_contacts_query)
            existing_contacts = pgql_cur.fetchone()
            
            r = None
            if not existing_contacts[0]:
                r = "{"
                r += f'"{contact_id["_id"]}"'
                r += "}"
            else:
                r = "{"
                for contact in existing_contacts:
                    r += f'"{contact[0]}", '
                r += f'"{contact_id["_id"]}"'
                r += "}"

            if r:
                add_contact_req = (f"""
                    UPDATE users
                    SET contacts = '{r}'
                    WHERE _id = '{user_id}'
                    RETURNING *;
                """)
                pgql_cur.execute(add_contact_req)
                res = pgql_cur.fetchone()
                pgql_conn.commit()
                return {
                    "successful": True,
                    "data": {
                        "contact_is": contact_id["_id"],
                        "email": contact_mail
                    }
                }
            return {
                "successful": False,
                "message": "Internal Error at pgql_user -> add_contact"
            }
        except Exception as e:
            print(e)
            return {
                "successful": False,
                "message": "Internal Error at pgql_user -> add_contact"
            }

    def get_all():
        try:
            req = (f"""
                SELECT * FROM users;
            """)
            pgql_cur.execute(req)
            res = pgql_cur.fetchall()
            pgql_conn.commit()

            return res
        except Exception as e:
            print(e)
            return None
