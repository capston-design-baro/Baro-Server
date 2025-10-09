from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.complaint import ComplainantInfoCreate
from app.models.user import User
from app.models.temp_complainant import TempComplainantInfo
from app.database import get_db
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/info/complainant", tags=["Complainant"])


@router.post("", status_code=status.HTTP_201_CREATED)
def save_complainant_info(
    request: ComplainantInfoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """고소인 정보 등록 (데이터베이스 임시 저장)"""

    # 기존 임시 정보가 있으면 삭제 (사용자당 하나의 임시 정보만 유지)
    existing = db.query(TempComplainantInfo).filter(
        TempComplainantInfo.user_id == current_user.id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

    # 새로운 고소인 정보 저장
    temp_info = TempComplainantInfo(
        user_id=current_user.id,
        complainant_name=request.complainant_name,
        complainant_address=request.complainant_address,
        complainant_phone=request.complainant_phone
    )

    db.add(temp_info)
    db.commit()
    db.refresh(temp_info)

    return {
        "id": temp_info.id,
        "message": "고소인 정보가 저장되었습니다.",
        "complainant_name": temp_info.complainant_name,
        "complainant_address": temp_info.complainant_address,
        "complainant_phone": temp_info.complainant_phone
    }


@router.get("")
def get_complainant_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """임시 저장된 고소인 정보 조회"""

    temp_info = db.query(TempComplainantInfo).filter(
        TempComplainantInfo.user_id == current_user.id
    ).first()

    if not temp_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="저장된 고소인 정보가 없습니다."
        )

    return {
        "id": temp_info.id,
        "complainant_name": temp_info.complainant_name,
        "complainant_address": temp_info.complainant_address,
        "complainant_phone": temp_info.complainant_phone,
        "created_at": temp_info.created_at
    }


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_complainant_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """임시 저장된 고소인 정보 삭제"""

    temp_info = db.query(TempComplainantInfo).filter(
        TempComplainantInfo.user_id == current_user.id
    ).first()

    if temp_info:
        db.delete(temp_info)
        db.commit()

    return None


# 헬퍼 함수: complaint API에서 사용
def get_temp_complainant_info(user_id: int, db: Session) -> TempComplainantInfo:
    """임시 저장소에서 고소인 정보 가져오기"""
    return db.query(TempComplainantInfo).filter(
        TempComplainantInfo.user_id == user_id
    ).first()


def clear_temp_complainant_info(user_id: int, db: Session):
    """임시 저장소에서 고소인 정보 삭제"""
    temp_info = db.query(TempComplainantInfo).filter(
        TempComplainantInfo.user_id == user_id
    ).first()

    if temp_info:
        db.delete(temp_info)
        db.commit()
