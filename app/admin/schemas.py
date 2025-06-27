from pydantic import BaseModel


class AdminUserCreate(BaseModel):
    username: str
    password: str
    email: str
    is_superuser: bool = False

    model_config = {
        "from_attributes": True
    }


class AdminUserLogin(BaseModel):
    username: str
    password: str


class AdminUserOut(BaseModel):
    id: int
    username: str
    email: str
    is_superuser: bool

    model_config = {
        "from_attributes": True
    }
