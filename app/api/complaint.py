from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.complaint import Complaint
from app.schemas.complaint import (
    ComplaintCreate, ComplaintResponse, ComplaintStartResponse, ComplaintDetail,
    ComplaintUpdate, ComplaintGenerateRequest, ComplaintGenerateResponse,
    ChatMessageCreate, ChatResponse, ComplainantInfoCreate, AccusedInfoCreate
)
from app.middleware.auth_middleware import get_current_user
from app.services.encryption_service import encryption_service
from app.services.ai_service import ai_service
from app.services.docx_service import complaint_docx_service

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


@router.post("/info/accused/{complaint_id}", response_model=ComplaintResponse, status_code=status.HTTP_200_OK)
def register_accused_info(
    complaint_id: int,
    request: AccusedInfoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """피고소인 정보 등록 - 기존 Complaint에 피고소인 정보 추가"""

    # Complaint 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    # 피고소인 정보 업데이트
    complaint.accused_name = request.accused_name
    complaint.accused_address = request.accused_address
    complaint.accused_phone = request.accused_phone

    db.commit()
    db.refresh(complaint)

    return complaint


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

    # 4. 응답 반환 (reason과 question 분리)
    full_reply = ai_response.get("reply", "")

    # reply가 "\n"로 구분되어 있으면 첫 줄은 reason, 나머지는 question
    if "\n" in full_reply:
        parts = full_reply.split("\n", 1)
        reason = parts[0].strip()
        question = parts[1].strip() if len(parts) > 1 else full_reply
    else:
        reason = None
        question = full_reply

    return ChatResponse(
        reply=question,
        reason=reason
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
        sections = ai_response.get("sections", {})
        criminal_facts = sections.get("criminal_facts", "")
        accusation_reason = sections.get("accusation_reason", "")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 생성된 고소장 암호화 저장
    complaint.generated_complaint_encrypted = encryption_service.encrypt_json({
        "criminal_facts": criminal_facts,
        "accusation_reason": accusation_reason
    })
    complaint.status = "completed"

    db.commit()

    return {
        "complaint_id": complaint.id,
        "criminal_facts": criminal_facts,
        "accusation_reason": accusation_reason,
        "status": "completed"
    }

@router.get("/{complaint_id}/download")
def download_complaint_docx(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """고소장 DOCX 파일 다운로드"""
    # 1. 고소장 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    # 2. 고소장이 완료되었는지 확인
    if complaint.status != "completed" or not complaint.generated_complaint_encrypted:
        raise HTTPException(status_code=400, detail="생성된 고소장이 없습니다. 먼저 고소장을 생성해주세요.")

    # 3. 암호화된 고소장 복호화
    try:
        decrypted_data = encryption_service.decrypt_json(complaint.generated_complaint_encrypted)
        criminal_facts = decrypted_data.get("criminal_facts", "")
        accusation_reason = decrypted_data.get("accusation_reason", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"고소장 복호화 실패: {str(e)}")

    # 4. 필수 정보 확인
    if not complaint.complainant_name or not complaint.accused_name or not complaint.crime_type:
        raise HTTPException(status_code=400, detail="고소인 또는 피고소인 정보가 누락되었습니다.")

    # 5. DOCX 파일 생성
    complainant_info = {
        "name": complaint.complainant_name,
        "address": complaint.complainant_address or "",
        "phone": complaint.complainant_phone or ""
    }

    accused_info = {
        "name": complaint.accused_name,
        "address": complaint.accused_address or "",
        "phone": complaint.accused_phone or ""
    }

    try:
        docx_stream = complaint_docx_service.create_complaint_docx(
            complainant_info=complainant_info,
            accused_info=accused_info,
            crime_type=complaint.crime_type,
            criminal_facts=criminal_facts,
            accusation_reason=accusation_reason,
            duplicate_complaint=complaint.duplicate_complaint or False,
            related_criminal_case=complaint.related_criminal_case or False,
            related_civil_case=complaint.related_civil_case or False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX 파일 생성 실패: {str(e)}")

    # 6. 파일명 생성 (한글 URL 인코딩)
    from urllib.parse import quote
    filename = f"고소장_{complaint.id}_{complaint.crime_type}.docx"
    encoded_filename = quote(filename)

    # 7. StreamingResponse로 파일 반환
    return StreamingResponse(
        docx_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )

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