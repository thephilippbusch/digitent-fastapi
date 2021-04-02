from fastapi import HTTPException

from main import db
from app.models.chat_model import ChatSchema


class ChatManager:
    def add_chat(chat: ChatSchema) -> str:
        try:
            res = db.chats.insert_one(chat)
            return res.inserted_id
        except:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def check_chat(id: str) -> bool:
        try:
            chat_list = db.chats.find({}, { "_id": 1 })
            for chat in chat_list:
                if chat["_id"] == id:
                    return True
            return False
        except:
            raise HTTPException(status_code=500, detail="Internal Server Error")
