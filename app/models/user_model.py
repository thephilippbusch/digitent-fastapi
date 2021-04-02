from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    username: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@mail.com",
                "password": "some password",
                "username": "some username"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "email": "user@mail.com",
                "password": "some password"
            }
        }


class UserIDModel(BaseModel):
    id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "some id"
            }
        }