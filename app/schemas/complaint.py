from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# 고소장 시작
class ComplaintCreate(BaseModel):
    offense: str  # "fraud" or "insult"

# 고소인 정보 입력
class ComplainantInfoCreate(BaseModel):
    complainant_name: str
    complainant_address: str
    complainant_phone: str

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
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str

class ChatResponse(BaseModel):
    reply: str  # AI 응답 메시지

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

# 최종 고소장 생성 요청
class ComplaintGenerateRequest(BaseModel):
    pass  # 빈 요청

# 최종 고소장 응답
class ComplaintGenerateResponse(BaseModel):
    complaint_id: int
    generated_complaint: str  # 복호화된 최종 고소장
    status: str