from pydantic import BaseModel, Field

from .message_model import MessageSchema

class ChatSchema(BaseModel):
    user: list = Field(...)
    history: list = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user": [
                    "user1_id",
                    "user2_id",
                    "..."
                ],
                "history": [
                    "message1_id",
                    "message2_id",
                    "..."
                ]
            }
        }
