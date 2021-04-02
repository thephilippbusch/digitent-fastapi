from pydantic import BaseModel, Field

class MessageSchema(BaseModel):
    from_user: str = Field(...)
    message: str = Field(...)
    answers: str = Field(requierd=None)

    class Config:
        schema_extra: {
            "example": {
                "from_user": "user@mail.com",
                "message": "Some message",
                "answers": [
                    "answer 1",
                    "answer 2"
                ]
            }
        }
    