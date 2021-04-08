from pydantic import BaseModel, Field

class ChatSchema(BaseModel):
    user_1: str = Field(...)
    user_2: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_1": "ABCD1234",
                "user_2": "1234ABCD",
            }
        }
