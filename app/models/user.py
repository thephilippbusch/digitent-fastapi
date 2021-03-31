from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int = Field(default=None)
    email: str = Field()
    password: str = Field()
    username: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "email": "philipp@busch.com",
                "password": "1234",
                "username": "Phillex"
            }
        }
