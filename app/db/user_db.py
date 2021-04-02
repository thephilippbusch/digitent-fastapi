from fastapi import HTTPException
from bson import ObjectId

from main import db
from app.models.user_model import UserSchema, UserLoginSchema

def convert_dict(data: dict) -> dict:
    if "_id" in data:
        id = str(data['_id'])
        del data['_id']
        data['id'] = id
    return data

class UserManager:

    def add_user(user: UserSchema):
        try:
            res = db.user.insert_one(user.dict())
            return str(res.inserted_id)
        except Exception as e:
            print(e)

    def check_user(user_data: UserLoginSchema) -> bool:
        try:
            login_data = user_data.dict()
            user_list = db.user.find({}, { "email": 1 })
            for user in user_list:
                if user['email'] == login_data['email']:
                    return True
            return False
        except Exception as e:
            print(e)

    def find_all() -> dict:
        try:
            res = []
            user_list = db.user.find()
            for user in user_list:
                res.append(convert_dict(user))
            return res
        except Exception as e:
            print(e)

    def find_by_id(id: str) -> dict:
        try:
            res = db.user.find_one({ "_id": ObjectId(id) })
            if res:
                return convert_dict(res)
            else:
                return None
        except Exception as e:
            print(e)

    def find_by_mail(email: str) -> dict:
        try:
            res = db.user.find_one({ "email": email })
            if res:
                return convert_dict(res)
            else:
                return None
        except Exception as e:
            print(e)
