from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class DocumentSchema(BaseModel):
    title: str
    company_name: str
    document_type: str