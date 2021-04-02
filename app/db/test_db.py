from pymongo import MongoClient
from fastapi import HTTPException

client = MongoClient(host="localhost", port=27017)

db = client.test_db

def convert_dict(data: dict) -> dict:
        if '_id' in data:
            id = str(data['_id'])
            del data['_id']
            data['id'] = id
        return data

class TestManager:

    def get_message() -> dict:
        try:
            res = db.test_col.find_one()
            if res:
                return convert_dict(res)
            else:
                return None
        except:
            raise HTTPException(status_code=500, detail="Internal Server Error")
