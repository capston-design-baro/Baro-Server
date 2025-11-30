"""주소 파싱 유틸리티"""
import re
from typing import Optional, Tuple


def parse_address(address: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    한국 주소에서 시/도, 시, 구/군을 추출합니다.

    Args:
        address: 전체 주소 문자열 (예: "서울특별시 동작구 노량진동 123")

    Returns:
        (province, city, district) 튜플
        - province: 시/도 (예: "서울특별시", "경기도")
        - city: 시 (예: "청주시", "성남시") - 특별시/광역시의 경우 None
        - district: 구/군 (예: "동작구", "청원구", "영동군")

    Examples:
        >>> parse_address("서울특별시 동작구 노량진동 123")
        ("서울특별시", None, "동작구")
        >>> parse_address("충청북도 청주시 청원구 정자동 456")
        ("충청북도", "청주시", "청원구")
        >>> parse_address("세종특별자치시 한누리대로 2130")
        ("세종특별자치시", None, None)
        >>> parse_address("충청북도 영동군 영동읍 123")
        ("충청북도", None, "영동군")
    """
    if not address:
        return None, None, None

    # 주소 정규화 (공백 제거 및 정리)
    address = address.strip()

    # 축약형을 정식 명칭으로 변환
    abbreviation_map = {
        '경기': '경기도',
        '강원': '강원도',
        '충북': '충청북도',
        '충남': '충청남도',
        '전북': '전라북도',
        '전남': '전라남도',
        '경북': '경상북도',
        '경남': '경상남도',
        '제주': '제주특별자치도',
        '서울': '서울특별시',
        '부산': '부산광역시',
        '대구': '대구광역시',
        '인천': '인천광역시',
        '광주': '광주광역시',
        '대전': '대전광역시',
        '울산': '울산광역시',
        '세종': '세종특별자치시'
    }

    for abbr, full in abbreviation_map.items():
        if address.startswith(abbr + ' ') or address.startswith(abbr):
            address = address.replace(abbr, full, 1)
            break

    # 시/도 패턴 (특별시, 광역시, 도, 특별자치시, 특별자치도)
    province_pattern = r'(서울특별시|부산광역시|대구광역시|인천광역시|광주광역시|대전광역시|울산광역시|세종특별자치시|경기도|강원특별자치도|강원도|충청북도|충청남도|전북특별자치도|전라북도|전라남도|경상북도|경상남도|제주특별자치도)'

    # 시/구/군 패턴
    admin_pattern = r'([가-힣]+시|[가-힣]+구|[가-힣]+군)'

    province = None
    city = None
    district = None

    # 1. 시/도 추출
    province_match = re.search(province_pattern, address)
    if province_match:
        province = province_match.group(1)
        # 시/도 이후의 주소에서 시/구/군 추출
        remaining_address = address[province_match.end():]

        # 2. 모든 시/구/군 찾기
        admin_matches = re.findall(admin_pattern, remaining_address)

        if len(admin_matches) >= 2:
            # 시와 구가 모두 있는 경우 (예: "청주시 청원구")
            city = admin_matches[0]
            district = admin_matches[1]
        elif len(admin_matches) == 1:
            # 하나만 있는 경우
            admin = admin_matches[0]
            if admin.endswith('시'):
                # 시만 있는 경우 (예: "충주시")
                city = admin
                district = None
            else:
                # 특별시/광역시 + 구/군 (예: "서울특별시 동작구", "충청북도 영동군")
                city = None
                district = admin
        else:
            # 세종특별자치시처럼 구/군이 없는 경우
            city = None
            district = None

    return province, city, district


def get_police_station_name(address: str, db) -> str:
    """
    주소를 기반으로 관할 경찰서명을 조회합니다.

    Args:
        address: 전체 주소 문자열
        db: SQLAlchemy Session 객체

    Returns:
        경찰서명 (예: "서울동작경찰서")
        찾지 못한 경우 기본값 "○○경찰서" 반환

    Examples:
        >>> get_police_station_name("서울특별시 동작구 노량진동 123", db)
        "서울동작경찰서"
        >>> get_police_station_name("충청북도 청주시 청원구 정자동 456", db)
        "청주청원경찰서"
    """
    from app.models.police_station import PoliceStation

    province, city, district = parse_address(address)

    if not province:
        return "○○경찰서"

    # 우선순위 1: province, city, district 모두 일치
    if province and city and district:
        station = db.query(PoliceStation).filter(
            PoliceStation.province == province,
            PoliceStation.city == city,
            PoliceStation.district == district
        ).first()
        if station:
            return station.station_name

    # 우선순위 2: province와 district만 일치 (특별시/광역시의 경우)
    if province and district:
        station = db.query(PoliceStation).filter(
            PoliceStation.province == province,
            PoliceStation.district == district
        ).first()
        if station:
            return station.station_name

    # 우선순위 3: province와 city만 일치 (시 단위 관할)
    if province and city:
        station = db.query(PoliceStation).filter(
            PoliceStation.province == province,
            PoliceStation.city == city,
            PoliceStation.district.is_(None)
        ).first()
        if station:
            return station.station_name

    # 우선순위 4: province만 일치 (세종특별자치시 등)
    if province:
        station = db.query(PoliceStation).filter(
            PoliceStation.province == province
        ).first()
        if station:
            return station.station_name

    # 찾지 못한 경우 기본값 반환
    return "○○경찰서"
