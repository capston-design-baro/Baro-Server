from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.complaint import Complaint
from app.schemas.complaint import (
    ComplaintCreate, ComplaintResponse, ComplaintStartResponse, ComplaintDetail,
    ComplaintUpdate, ComplaintGenerateRequest, ComplaintGenerateResponse,
    ChatMessageCreate, ChatResponse
)
from app.middleware.auth_middleware import get_current_user
from app.services.encryption_service import encryption_service
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

@router.post("/start", response_model=ComplaintStartResponse, status_code=status.HTTP_201_CREATED)
async def start_complaint(
    request: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """고소장 작성 시작 - Baro-AI 세션 초기화"""

    # 1. Baro-AI 채팅 세션 초기화
    try:
        ai_response = await ai_service.chat_init(request.offense)
        session_id = ai_response.get("session_id")
        first_question = ai_response.get("message", "사건에 대해 설명해주세요.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 2. DB에 고소장 생성 및 세션 ID 저장
    new_complaint = Complaint(
        user_id=current_user.id,
        crime_type=request.offense,
        status="in_progress",
        ai_session_id=session_id
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    # 3. 응답에 첫 질문 포함
    return ComplaintStartResponse(
        id=new_complaint.id,
        user_id=new_complaint.user_id,
        status=new_complaint.status,
        crime_type=new_complaint.crime_type,
        created_at=new_complaint.created_at,
        first_question=first_question
    )

@router.get("/", response_model=List[ComplaintResponse])
def get_my_complaints(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내 고소장 목록 조회"""
    complaints = db.query(Complaint).filter(
        Complaint.user_id == current_user.id
    ).order_by(Complaint.created_at.desc()).all()

    return complaints

@router.post("/{complaint_id}/chat", response_model=ChatResponse)
async def send_chat_message(
    complaint_id: int,
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """대화 메시지 전송 - Baro-AI와 통신"""

    # 1. 고소장 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    if not complaint.ai_session_id:
        raise HTTPException(status_code=400, detail="AI 세션이 초기화되지 않았습니다")

    # 2. Baro-AI에 메시지 전송
    try:
        ai_response = await ai_service.chat_send(
            session_id=complaint.ai_session_id,
            message=request.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 3. 응답 반환
    return ChatResponse(
        reply=ai_response.get("reply", "")
    )

@router.post("/{complaint_id}/generate", response_model=ComplaintGenerateResponse)
async def generate_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """최종 고소장 생성 - Baro-AI로 고소장 작성"""
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    if not complaint.ai_session_id:
        raise HTTPException(status_code=400, detail="AI 세션이 초기화되지 않았습니다")

    # Baro-AI에 고소장 작성 요청
    try:
        ai_response = await ai_service.chat_compose(complaint.ai_session_id)
        generated_text = ai_response.get("draft", "")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 생성된 고소장 암호화 저장
    complaint.generated_complaint_encrypted = encryption_service.encrypt_json({
        "content": generated_text
    })
    complaint.status = "completed"

    db.commit()

    return {
        "complaint_id": complaint.id,
        "generated_complaint": generated_text,
        "status": "completed"
    }

@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """고소장 삭제"""
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")
    
    db.delete(complaint)
    db.commit()