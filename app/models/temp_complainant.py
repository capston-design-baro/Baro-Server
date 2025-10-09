from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class TempComplainantInfo(Base):
    """고소인 정보 임시 저장 테이블"""
    __tablename__ = "temp_complainant_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 작성자 (로그인한 사용자)

    # 고소인 정보
    complainant_name = Column(String, nullable=False)
    complainant_address = Column(Text, nullable=False)
    complainant_phone = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
