from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from datetime import datetime
from app.services.encryption_service import encryption_service

# 고소장 시작
class ComplaintCreate(BaseModel):
    offense: str  # "fraud" or "insult"

# 고소인 정보 입력
class ComplainantInfoCreate(BaseModel):
    complainant_name: str
    complainant_address: str
    complainant_office_address: Optional[str] = None  # 사무실 주소
    complainant_job: Optional[str] = None  # 직업
    complainant_phone: str  # 휴대폰
    complainant_home_phone: Optional[str] = None  # 자택 전화
    complainant_office_phone: Optional[str] = None  # 사무실 전화

# 피고소인 정보 입력
class AccusedInfoCreate(BaseModel):
    accused_name: str
    accused_address: str
    accused_office_address: Optional[str] = None  # 사무실 주소
    accused_job: Optional[str] = None  # 직업
    accused_phone: str
    accused_email: Optional[str] = None  # 이메일
    accused_etc: Optional[str] = None  # 기타사항

# 관련사건 정보 입력
class RelatedCasesCreate(BaseModel):
    duplicate_complaint: bool  # 중복 고소 여부
    related_criminal_case: bool  # 관련 형사사건 수사 유무
    related_civil_case: bool  # 관련 민사소송 유무

# 사건 정보 업데이트
class ComplaintUpdate(BaseModel):
    accused_name: Optional[str] = None
    accused_address: Optional[str] = None
    accused_phone: Optional[str] = None
    crime_fact: Optional[str] = None
    complaint_reason: Optional[str] = None
    incident_summary: Optional[str] = None
    crime_type: Optional[str] = None
    has_evidence: Optional[bool] = None
    duplicate_complaint: Optional[bool] = None
    related_criminal_case: Optional[bool] = None
    related_civil_case: Optional[bool] = None

# 대화 메시지
class ChatMessageCreate(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    role: str  # 'user' or 'assistant'
    content: str
    reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    reply: str  # AI 응답 메시지 (질문)
    reason: Optional[str] = None  # 재질문 이유

# 고소장 응답
class ComplaintResponse(BaseModel):
    id: int
    user_id: int
    status: str
    crime_type: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# 고소장 시작 응답 (첫 질문 포함)
class ComplaintStartResponse(BaseModel):
    id: int
    user_id: int
    status: str
    crime_type: Optional[str]
    created_at: datetime
    ai_session_id: Optional[str]  # Baro-AI 세션 ID
    first_question: str  # Baro-AI에서 받은 첫 질문

    class Config:
        from_attributes = True

# 고소장 상세
class ComplaintDetail(BaseModel):
    id: int
    status: str
    crime_type: str

    # 고소인 정보 (User에서)
    complainant_name: str
    complainant_email: str

    # 피고소인 정보
    accused_name: str
    accused_address: str
    accused_phone: str

    # 사건 정보
    incident_summary: str
    crime_fact: str
    complaint_reason: str
    has_evidence: str
    duplicate_complaint: str
    related_criminal_case: str
    related_civil_case: str

    created_at: datetime
    updated_at: Optional[datetime]

    @model_validator(mode='before')
    @classmethod
    def decrypt_fields(cls, data):
        """DB에서 조회한 암호화된 필드를 복호화"""
        if hasattr(data, '__dict__'):
            # SQLAlchemy 모델인 경우
            decrypted_data = {}
            encrypted_fields = [
                'complainant_name', 'complainant_address', 'complainant_office_address',
                'complainant_job', 'complainant_phone', 'complainant_home_phone',
                'complainant_office_phone', 'accused_name', 'accused_address',
                'accused_office_address', 'accused_job', 'accused_phone',
                'accused_email', 'accused_etc', 'crime_fact', 'complaint_reason',
                'incident_summary'
            ]

            for key, value in data.__dict__.items():
                if key in encrypted_fields and isinstance(value, bytes):
                    decrypted_data[key] = encryption_service.decrypt_field(value)
                else:
                    decrypted_data[key] = value
            return decrypted_data
        return data

# 최종 고소장 생성 요청
class ComplaintGenerateRequest(BaseModel):
    pass  # 빈 요청

# 최종 고소장 응답
class ComplaintGenerateResponse(BaseModel):
    complaint_id: int
    criminal_facts: str  # 범죄사실
    accusation_reason: str  # 고소이유
    status: str