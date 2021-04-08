from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    username: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "john@doe.com",
                "password": "secure password",
                "username": "John Doe"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "email": "john@doe.com",
                "password": "secure password"
            }
        }


class AddAdminSchema(BaseModel):
    admin_id: str = Field(...)
    user_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "admin_id": "ADMIN ID",
                "user_id": "USER ID"
            }
        }
