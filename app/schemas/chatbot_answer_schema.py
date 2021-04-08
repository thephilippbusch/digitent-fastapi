from pydantic import BaseModel, Field
from typing import List, Optional

class ChatbotAnswerSchema(BaseModel):
    trigger: str = Field(...)
    message: str = Field(...)
    created_by: str = Field(...)
    responses: Optional[List[str]] = None

    class Config:
        schema_extra: {
            "example": {
                "trigger": "trigger message",
                "message": "Some message",
                "created_by": "1234ABVCD",
                "responses": [
                    "response 1",
                    "response 2"
                ]
            }
        }