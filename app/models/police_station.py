from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class PoliceStation(Base):
    """전국 경찰서 관할구역 정보"""
    __tablename__ = "police_stations"

    id = Column(Integer, primary_key=True, index=True)

    # 경찰서 정보
    province = Column(String, nullable=False, index=True)  # 시/도 (예: "서울특별시", "부산광역시")
    city = Column(String, nullable=True, index=True)  # 시 (예: "청주시", "수원시")
    district = Column(String, nullable=True, index=True)  # 구/군 (예: "청원구", "흥덕구", "동작구")
    station_name = Column(String, nullable=False)  # 경찰서명 (예: "서울동작경찰서")
    jurisdiction = Column(Text, nullable=True)  # 상세 관할구역 정보
