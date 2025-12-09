from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.complaint import Complaint
from app.models.chat_message import ChatMessage
from app.schemas.complaint import (
    ComplaintCreate, ComplaintResponse, ComplaintStartResponse, ComplaintDetail,
    ComplaintUpdate, ComplaintGenerateRequest, ComplaintGenerateResponse,
    ChatMessageCreate, ChatResponse, ComplainantInfoCreate, AccusedInfoCreate,
    RelatedCasesCreate, EvidenceCreate, ChatInitRequest, ChatInitResponse, RagCase,
    ChatMessageResponse, ChatHistoryResponse
)
from app.middleware.auth_middleware import get_current_user
from app.services.encryption_service import encryption_service
from app.services.ai_service import ai_service
from app.services.docx_service import complaint_docx_service
from app.utils.address_parser import get_police_station_name

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

@router.post("/info/complainant", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def register_complainant_info(
    request: ComplainantInfoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """고소인 정보 등록 - Complaint 생성 및 complaint_id 반환"""

    # 고소인 정보 암호화
    encrypted_complainant_name = encryption_service.encrypt_field(request.complainant_name)
    encrypted_complainant_address = encryption_service.encrypt_field(request.complainant_address)
    encrypted_complainant_office_address = encryption_service.encrypt_field(request.complainant_office_address) if request.complainant_office_address else None
    encrypted_complainant_job = encryption_service.encrypt_field(request.complainant_job) if request.complainant_job else None
    encrypted_complainant_phone = encryption_service.encrypt_field(request.complainant_phone)
    encrypted_complainant_home_phone = encryption_service.encrypt_field(request.complainant_home_phone) if request.complainant_home_phone else None
    encrypted_complainant_office_phone = encryption_service.encrypt_field(request.complainant_office_phone) if request.complainant_office_phone else None

    # Complaint 생성 (고소인 정보만 포함, crime_type은 나중에 설정)
    new_complaint = Complaint(
        user_id=current_user.id,
        status="in_progress",
        complainant_name=encrypted_complainant_name,
        complainant_address=encrypted_complainant_address,
        complainant_office_address=encrypted_complainant_office_address,
        complainant_job=encrypted_complainant_job,
        complainant_phone=encrypted_complainant_phone,
        complainant_home_phone=encrypted_complainant_home_phone,
        complainant_office_phone=encrypted_complainant_office_phone
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

    # 피고소인 정보 암호화 후 업데이트
    complaint.accused_name = encryption_service.encrypt_field(request.accused_name)
    complaint.accused_address = encryption_service.encrypt_field(request.accused_address)
    complaint.accused_office_address = encryption_service.encrypt_field(request.accused_office_address) if request.accused_office_address else None
    complaint.accused_job = encryption_service.encrypt_field(request.accused_job) if request.accused_job else None
    complaint.accused_phone = encryption_service.encrypt_field(request.accused_phone)
    complaint.accused_email = encryption_service.encrypt_field(request.accused_email) if request.accused_email else None
    complaint.accused_etc = encryption_service.encrypt_field(request.accused_etc) if request.accused_etc else None

    db.commit()
    db.refresh(complaint)

    return complaint


@router.post("/info/related-cases/{complaint_id}", response_model=ComplaintResponse, status_code=status.HTTP_200_OK)
def register_related_cases(
    complaint_id: int,
    request: RelatedCasesCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """관련사건 정보 등록 - 중복고소, 관련형사사건, 관련민사소송 여부"""

    # Complaint 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    # 관련사건 정보 업데이트
    complaint.duplicate_complaint = request.duplicate_complaint
    complaint.related_criminal_case = request.related_criminal_case
    complaint.related_civil_case = request.related_civil_case

    db.commit()
    db.refresh(complaint)

    return complaint


@router.post("/info/evidence/{complaint_id}", response_model=ComplaintResponse, status_code=status.HTTP_200_OK)
def register_evidence(
    complaint_id: int,
    request: EvidenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """증거 제출 여부 등록"""

    # Complaint 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    # 증거 제출 여부 업데이트
    complaint.has_evidence = request.has_evidence

    db.commit()
    db.refresh(complaint)

    return complaint


@router.post("/{complaint_id}/chat/init", response_model=ChatInitResponse, status_code=status.HTTP_200_OK)
async def init_chat_session(
    complaint_id: int,
    request: ChatInitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """채팅 세션 초기화 - 사건개요 입력 시 죄목 자동 판단 및 유사 판례 제공"""

    # 1. 기존 complaint 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    if complaint.ai_session_id:
        raise HTTPException(status_code=400, detail="이미 AI 세션이 시작된 고소장입니다")

    # 2. Baro-AI 채팅 세션 초기화 (사건개요 전송)
    try:
        ai_response = await ai_service.chat_init(request.text)
        session_id = ai_response.get("session_id")
        offense = ai_response.get("offense")
        rag_keyword = ai_response.get("rag_keyword")
        rag_cases_data = ai_response.get("rag_cases", [])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 3. Complaint 업데이트 (crime_type, ai_session_id 설정)
    complaint.crime_type = offense
    complaint.ai_session_id = session_id

    # 4. 사용자의 첫 메시지 저장
    user_message = ChatMessage(
        complaint_id=complaint_id,
        role="user",
        content=request.text
    )
    db.add(user_message)
    db.flush()  # user_message를 DB에 반영하여 다음 sequence 계산 가능하게

    # 5. AI 응답 메시지 저장 (offense, rag_keyword, rag_cases를 JSON으로 저장)
    import json
    ai_response_content = json.dumps({
        "offense": offense,
        "rag_keyword": rag_keyword,
        "rag_cases": rag_cases_data
    }, ensure_ascii=False)

    assistant_message = ChatMessage(
        complaint_id=complaint_id,
        role="assistant",
        content=ai_response_content
    )
    db.add(assistant_message)

    db.commit()
    db.refresh(complaint)

    # 6. 응답 (죄목 + 판례)
    rag_cases = [RagCase(**case) for case in rag_cases_data]

    return ChatInitResponse(
        session_id=session_id,
        offense=offense,
        rag_keyword=rag_keyword,
        rag_cases=rag_cases
    )


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
    """대화 메시지 전송 - Baro-AI와 통신 (세션 자동 복원 포함)"""

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

    # 3. 사용자 메시지 저장
    user_message = ChatMessage(
        complaint_id=complaint_id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.flush()  # user_message를 DB에 반영하여 다음 sequence 계산 가능하게

    # 4. Baro-AI에 메시지 전송 (세션 복원 로직 포함)
    try:
        ai_response = await ai_service.chat_send(
            session_id=ai_session_id,
            message=request.message
        )
    except RuntimeError as e:
        error_msg = str(e)

        # 세션을 찾을 수 없는 경우 (Render sleep 후 재시작)
        if "세션을 찾을 수 없습니다" in error_msg or "404" in error_msg:
            try:
                # DB에서 이전 채팅 히스토리 가져오기 (현재 메시지 제외)
                chat_history = db.query(ChatMessage).filter(
                    ChatMessage.complaint_id == complaint_id,
                    ChatMessage.id != user_message.id  # 방금 저장한 메시지는 제외
                ).order_by(ChatMessage.created_at.asc()).all()

                # 채팅 히스토리를 dict 리스트로 변환
                history_list = [
                    {"role": msg.role, "content": msg.content}
                    for msg in chat_history
                ]

                # 세션 복원
                new_session_id = await ai_service.chat_restore_session(history_list)

                # DB에 새 세션 ID 업데이트
                complaint.ai_session_id = new_session_id
                db.flush()

                # 복원된 세션으로 메시지 재전송
                ai_response = await ai_service.chat_send(
                    session_id=new_session_id,
                    message=request.message
                )
            except Exception as restore_error:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"세션 복원 실패: {str(restore_error)}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI 서비스 연결 실패: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 5. AI 응답 추출
    reply = ai_response.get("reply", "")

    # 6. AI 응답 메시지 저장
    assistant_message = ChatMessage(
        complaint_id=complaint_id,
        role="assistant",
        content=reply
    )
    db.add(assistant_message)
    db.commit()

    return ChatResponse(
        reply=reply
    )

@router.get("/{complaint_id}/chat/history", response_model=ChatHistoryResponse)
def get_chat_history(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """채팅 내역 조회 - 재진입 시 이전 대화 복원"""

    # 1. 고소장 조회 및 권한 확인
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    # 2. 해당 complaint의 모든 채팅 메시지 조회 (시간순 정렬)
    messages = db.query(ChatMessage).filter(
        ChatMessage.complaint_id == complaint_id
    ).order_by(ChatMessage.created_at.asc()).all()

    return ChatHistoryResponse(messages=messages)

@router.post("/{complaint_id}/generate", response_model=ComplaintGenerateResponse)
async def generate_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """최종 고소장 생성 - Baro-AI로 고소장 작성 (세션 자동 복원 포함)"""
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.user_id == current_user.id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="고소장을 찾을 수 없습니다")

    if not complaint.ai_session_id:
        raise HTTPException(status_code=400, detail="AI 세션이 초기화되지 않았습니다")

    # Baro-AI에 고소장 작성 요청 (세션 복원 로직 포함)
    try:
        ai_response = await ai_service.chat_compose(complaint.ai_session_id)
        sections = ai_response.get("sections", {})
        criminal_facts = sections.get("criminal_facts", "")
        accusation_reason = sections.get("accusation_reason", "")
    except RuntimeError as e:
        error_msg = str(e)

        # 세션을 찾을 수 없는 경우 (Render sleep 후 재시작)
        if "세션을 찾을 수 없습니다" in error_msg or "404" in error_msg:
            try:
                # DB에서 채팅 히스토리 가져오기
                chat_history = db.query(ChatMessage).filter(
                    ChatMessage.complaint_id == complaint_id
                ).order_by(ChatMessage.created_at.asc()).all()

                # 채팅 히스토리를 dict 리스트로 변환
                history_list = [
                    {"role": msg.role, "content": msg.content}
                    for msg in chat_history
                ]

                # 세션 복원
                new_session_id = await ai_service.chat_restore_session(history_list)

                # DB에 새 세션 ID 업데이트
                complaint.ai_session_id = new_session_id
                db.flush()

                # 복원된 세션으로 고소장 작성 재요청
                ai_response = await ai_service.chat_compose(new_session_id)
                sections = ai_response.get("sections", {})
                criminal_facts = sections.get("criminal_facts", "")
                accusation_reason = sections.get("accusation_reason", "")
            except Exception as restore_error:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"세션 복원 실패: {str(restore_error)}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI 서비스 연결 실패: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 서비스 연결 실패: {str(e)}"
        )

    # 개별 필드에 암호화하여 저장
    complaint.crime_fact = encryption_service.encrypt_field(criminal_facts)
    complaint.complaint_reason = encryption_service.encrypt_field(accusation_reason)

    # 고소인 주소 기반 관할 경찰서 자동 입력
    if complaint.complainant_address:
        complainant_address = encryption_service.decrypt_field(complaint.complainant_address)
        complaint.police_station_name = get_police_station_name(complainant_address, db)

    # 생성된 고소장 암호화 저장 (기존 방식 유지)
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

    # 5. DOCX 파일 생성 (암호화된 필드 복호화)
    complainant_info = {
        "name": encryption_service.decrypt_field(complaint.complainant_name) if complaint.complainant_name else "",
        "address": encryption_service.decrypt_field(complaint.complainant_address) if complaint.complainant_address else "",
        "office_address": encryption_service.decrypt_field(complaint.complainant_office_address) if complaint.complainant_office_address else "",
        "job": encryption_service.decrypt_field(complaint.complainant_job) if complaint.complainant_job else "",
        "phone": encryption_service.decrypt_field(complaint.complainant_phone) if complaint.complainant_phone else "",
        "home_phone": encryption_service.decrypt_field(complaint.complainant_home_phone) if complaint.complainant_home_phone else "",
        "office_phone": encryption_service.decrypt_field(complaint.complainant_office_phone) if complaint.complainant_office_phone else "",
        "email": current_user.email  # User 테이블에서 이메일 가져오기
    }

    accused_info = {
        "name": encryption_service.decrypt_field(complaint.accused_name) if complaint.accused_name else "",
        "address": encryption_service.decrypt_field(complaint.accused_address) if complaint.accused_address else "",
        "office_address": encryption_service.decrypt_field(complaint.accused_office_address) if complaint.accused_office_address else "",
        "job": encryption_service.decrypt_field(complaint.accused_job) if complaint.accused_job else "",
        "phone": encryption_service.decrypt_field(complaint.accused_phone) if complaint.accused_phone else "",
        "email": encryption_service.decrypt_field(complaint.accused_email) if complaint.accused_email else "",
        "etc": encryption_service.decrypt_field(complaint.accused_etc) if complaint.accused_etc else ""
    }

    try:
        docx_stream = complaint_docx_service.create_complaint_docx(
            complainant_info=complainant_info,
            accused_info=accused_info,
            crime_type=complaint.crime_type,
            criminal_facts=criminal_facts,
            accusation_reason=accusation_reason,
            db=db,
            has_evidence=complaint.has_evidence or False,
            duplicate_complaint=complaint.duplicate_complaint or False,
            related_criminal_case=complaint.related_criminal_case or False,
            related_civil_case=complaint.related_civil_case or False,
            police_station_name=complaint.police_station_name or "○○경찰서"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX 파일 생성 실패: {str(e)}")

    # 6. 다운로드 시점 기록 (TTL 삭제용)
    from datetime import datetime, timezone
    complaint.downloaded_at = datetime.now(timezone.utc)
    db.commit()

    # 7. 파일명 생성 (한글 URL 인코딩)
    from urllib.parse import quote
    filename = f"고소장_{complaint.id}_{complaint.crime_type}.docx"
    encoded_filename = quote(filename)

    # 8. StreamingResponse로 파일 반환
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