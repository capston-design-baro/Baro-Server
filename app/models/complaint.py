from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 기본 정보
    status = Column(String, default="in_progress")  # 'in_progress', 'completed'
    crime_type = Column(String, nullable=True)  # 'fraud', 'insult'

    # 고소인 정보 (암호화)
    complainant_name = Column(LargeBinary, nullable=True)
    complainant_address = Column(LargeBinary, nullable=True)
    complainant_office_address = Column(LargeBinary, nullable=True)  # 사무실 주소
    complainant_job = Column(LargeBinary, nullable=True)  # 직업
    complainant_phone = Column(LargeBinary, nullable=True)  # 휴대폰
    complainant_home_phone = Column(LargeBinary, nullable=True)  # 자택 전화
    complainant_office_phone = Column(LargeBinary, nullable=True)  # 사무실 전화

    # 피고소인 정보 (암호화)
    accused_name = Column(LargeBinary, nullable=True)
    accused_address = Column(LargeBinary, nullable=True)
    accused_office_address = Column(LargeBinary, nullable=True)  # 사무실 주소
    accused_job = Column(LargeBinary, nullable=True)  # 직업
    accused_phone = Column(LargeBinary, nullable=True)
    accused_email = Column(LargeBinary, nullable=True)  # 이메일
    accused_etc = Column(LargeBinary, nullable=True)  # 기타사항

    # 사건 정보 (암호화)
    crime_fact = Column(LargeBinary, nullable=True)  # 범죄사실
    complaint_reason = Column(LargeBinary, nullable=True)  # 고소이유
    incident_summary = Column(LargeBinary, nullable=True)  # 입증하려는 내용
    has_evidence = Column(Boolean, default=False)       # 증거자료 제출 여부 
    duplicate_complaint = Column(Boolean, default=False)   # 중복 고소 여부
    related_criminal_case = Column(Boolean, default=False) # 관련 형사사건 수사 여부
    related_civil_case = Column(Boolean, default=False)    # 관련 민사소송 여부
    
    # 최종 생성된 고소장 암호화 저장
    generated_complaint_encrypted = Column(LargeBinary, nullable=True)
    
    # S3 대화 로그 경로
    s3_conversation_key = Column(String, nullable=True)  # "conversations/123.json"

    # Baro-AI 세션 ID
    ai_session_id = Column(String, nullable=True)  # Baro-AI의 session_id

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="complaints")
    chat_messages = relationship("ChatMessage", back_populates="complaint", cascade="all, delete-orphan")