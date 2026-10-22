from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    phone_number: str
