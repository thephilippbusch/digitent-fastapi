from pydantic import BaseModel, Field

class MessageSchema(BaseModel):
    message: str = Field(...)
    from_user: str = Field(...)
    chat_id: str = Field(...)

    class Config:
        schema_extra: {
            "example": {
                "message": "Hello World",
                "from_user": "1234ABCD",
                "chat_id": "ABCD1234"
            }
        }
