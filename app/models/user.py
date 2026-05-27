from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(LargeBinary, nullable=False)  # 암호화
    password_hash = Column(String, nullable=False)
    address = Column(LargeBinary, nullable=True)  # 암호화
    phone_number = Column(LargeBinary, nullable=True)  # 암호화
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    complaints = relationship("Complaint", back_populates="user")
