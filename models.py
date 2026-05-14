from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="Client")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company_name = Column(String)
    document_type = Column(String)
    file_path = Column(String)
    uploaded_by = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)