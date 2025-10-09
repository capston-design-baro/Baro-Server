from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.complaint import Complaint
from app.schemas.complaint import (
    ComplaintCreate, ComplaintResponse, ComplaintStartResponse, ComplaintDetail,
    ComplaintUpdate, ComplaintGenerateRequest, ComplaintGenerateResponse,
    ChatMessageCreate, ChatResponse, ComplainantInfoCreate
)
from app.middleware.auth_middleware import get_current_user
from app.services.encryption_service import encryption_service
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

@router.post("/info/complainant", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def register_complainant_info(
    request: ComplainantInfoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """고소인 정보 등록 - Complaint 생성 및 complaint_id 반환"""

    # Complaint 생성 (고소인 정보만 포함, crime_type은 나중에 설정)
    new_complaint = Complaint(
        user_id=current_user.id,
        status="in_progress",
        complainant_name=request.complainant_name,
        complainant_address=request.complainant_address,
        complainant_phone=request.complainant_phone
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint


@router.post("/{complaint_id}/start", response_model=ComplaintStartResponse, status_code=status.HTTP_200_OK)
async def start_complaint(
    complaint_id: int,
    request: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """고소장 AI 세션 시작 - 기존 Complaint에 범죄 유형 및 AI 세션 연결"""

    # 1. 기존 complaint 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    if complaint.ai_session_id:
        raise HTTPException(status_code=400, detail="이미 AI 세션이 시작된 고소장입니다")

    # 2. Baro-AI 채팅 세션 초기화
    try:
        ai_response = await ai_service.chat_init(request.offense)
        session_id = ai_response.get("session_id")
        first_question = ai_response.get("message", "사건에 대해 설명해주세요.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 3. Complaint 업데이트 (crime_type, ai_session_id 설정)
    complaint.crime_type = request.offense
    complaint.ai_session_id = session_id

    db.commit()
    db.refresh(complaint)

    # 4. 응답에 첫 질문 포함
    return ComplaintStartResponse(
        id=complaint.id,
        user_id=complaint.user_id,
        status=complaint.status,
        crime_type=complaint.crime_type,
        created_at=complaint.created_at,
        ai_session_id=complaint.ai_session_id,
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

@router.post("/{complaint_id}/chat/{ai_session_id}", response_model=ChatResponse)
async def send_chat_message(
    complaint_id: int,
    ai_session_id: str,
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

    # 2. ai_session_id 검증 (보안: 해당 complaint의 세션인지 확인)
    if complaint.ai_session_id != ai_session_id:
        raise HTTPException(status_code=403, detail="유효하지 않은 세션 ID입니다")

    # 3. Baro-AI에 메시지 전송
    try:
        ai_response = await ai_service.chat_send(
            session_id=ai_session_id,
            message=request.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 4. 응답 반환
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