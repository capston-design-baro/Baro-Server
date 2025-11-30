"""전국 경찰서 관할구역 시드 데이터"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.police_station import PoliceStation


def seed_police_stations():
    """전국 경찰서 데이터 삽입"""
    db: Session = SessionLocal()

    try:
        # 기존 데이터 삭제
        db.query(PoliceStation).delete()

        police_stations = [
            # 서울특별시 - 서울은 대부분 구 단위 관할
            {"province": "서울특별시", "city": None, "district": "중구", "station_name": "서울중부경찰서", "jurisdiction": "중구 중 광희동, 남학동, 묵정동..."},
            {"province": "서울특별시", "city": None, "district": "종로구", "station_name": "서울종로경찰서", "jurisdiction": "종로구 중 가회동, 견지동, 경운동..."},
            {"province": "서울특별시", "city": None, "district": "중구", "station_name": "서울남대문경찰서", "jurisdiction": "중구 중 남대문로1가동부터 5가동까지..."},
            {"province": "서울특별시", "city": None, "district": "서대문구", "station_name": "서울서대문경찰서", "jurisdiction": "서대문구"},
            {"province": "서울특별시", "city": None, "district": "종로구", "station_name": "서울혜화경찰서", "jurisdiction": "종로구 중 권농동, 동숭동, 명륜동..."},
            {"province": "서울특별시", "city": None, "district": "용산구", "station_name": "서울용산경찰서", "jurisdiction": "용산구"},
            {"province": "서울특별시", "city": None, "district": "성북구", "station_name": "서울성북경찰서", "jurisdiction": "성북구 중 돈암동, 동선동, 동소문동..."},
            {"province": "서울특별시", "city": None, "district": "동대문구", "station_name": "서울동대문경찰서", "jurisdiction": "동대문구"},
            {"province": "서울특별시", "city": None, "district": "마포구", "station_name": "서울마포경찰서", "jurisdiction": "마포구"},
            {"province": "서울특별시", "city": None, "district": "영등포구", "station_name": "서울영등포경찰서", "jurisdiction": "영등포구"},
            {"province": "서울특별시", "city": None, "district": "성동구", "station_name": "서울성동경찰서", "jurisdiction": "성동구"},
            {"province": "서울특별시", "city": None, "district": "동작구", "station_name": "서울동작경찰서", "jurisdiction": "동작구"},
            {"province": "서울특별시", "city": None, "district": "광진구", "station_name": "서울광진경찰서", "jurisdiction": "광진구"},
            {"province": "서울특별시", "city": None, "district": "은평구", "station_name": "서울서부경찰서", "jurisdiction": "은평구 중 녹번동, 수색동, 신사동, 응암동, 증산동, 역촌동"},
            {"province": "서울특별시", "city": None, "district": "강북구", "station_name": "서울강북경찰서", "jurisdiction": "강북구"},
            {"province": "서울특별시", "city": None, "district": "금천구", "station_name": "서울금천경찰서", "jurisdiction": "금천구"},
            {"province": "서울특별시", "city": None, "district": "중랑구", "station_name": "서울중랑경찰서", "jurisdiction": "중랑구"},
            {"province": "서울특별시", "city": None, "district": "강남구", "station_name": "서울강남경찰서", "jurisdiction": "강남구 중 논현동, 삼성동, 신사동, 압구정동, 청담동, 역삼동 일부"},
            {"province": "서울특별시", "city": None, "district": "관악구", "station_name": "서울관악경찰서", "jurisdiction": "관악구"},
            {"province": "서울특별시", "city": None, "district": "강서구", "station_name": "서울강서경찰서", "jurisdiction": "강서구"},
            {"province": "서울특별시", "city": None, "district": "강동구", "station_name": "서울강동경찰서", "jurisdiction": "강동구"},
            {"province": "서울특별시", "city": None, "district": "성북구", "station_name": "서울종암경찰서", "jurisdiction": "성북구 중 상월곡동, 석관동, 장위동, 하월곡동, 길음제2동, 종암동 일부"},
            {"province": "서울특별시", "city": None, "district": "구로구", "station_name": "서울구로경찰서", "jurisdiction": "구로구"},
            {"province": "서울특별시", "city": None, "district": "서초구", "station_name": "서울서초경찰서", "jurisdiction": "서초구 중 내곡동, 신원동, 서초동, 양재동, 염곡동, 우면동, 잠원동, 반포동 일부"},
            {"province": "서울특별시", "city": None, "district": "양천구", "station_name": "서울양천경찰서", "jurisdiction": "양천구"},
            {"province": "서울특별시", "city": None, "district": "송파구", "station_name": "서울송파경찰서", "jurisdiction": "송파구"},
            {"province": "서울특별시", "city": None, "district": "노원구", "station_name": "서울노원경찰서", "jurisdiction": "노원구"},
            {"province": "서울특별시", "city": None, "district": "서초구", "station_name": "서울방배경찰서", "jurisdiction": "서초구 중 방배동 일부, 반포동 일부"},
            {"province": "서울특별시", "city": None, "district": "은평구", "station_name": "서울은평경찰서", "jurisdiction": "은평구 중 갈현동, 구산동, 구파발동, 대조동, 불광동, 진관내동, 진관외동"},
            {"province": "서울특별시", "city": None, "district": "도봉구", "station_name": "서울도봉경찰서", "jurisdiction": "도봉구"},
            {"province": "서울특별시", "city": None, "district": "강남구", "station_name": "서울수서경찰서", "jurisdiction": "강남구 중 개포동, 도곡동, 수서동, 세곡동, 율현동, 일원동, 자곡동, 대치동 일부, 역삼동 일부"},

            # 부산광역시
            {"province": "부산광역시", "city": None, "district": "중구", "station_name": "부산중부경찰서", "jurisdiction": "중구"},
            {"province": "부산광역시", "city": None, "district": "동래구", "station_name": "부산동래경찰서", "jurisdiction": "동래구"},
            {"province": "부산광역시", "city": None, "district": "영도구", "station_name": "부산영도경찰서", "jurisdiction": "영도구"},
            {"province": "부산광역시", "city": None, "district": "동구", "station_name": "부산동부경찰서", "jurisdiction": "동구"},
            {"province": "부산광역시", "city": None, "district": "부산진구", "station_name": "부산진경찰서", "jurisdiction": "부산진구"},
            {"province": "부산광역시", "city": None, "district": "서구", "station_name": "부산서부경찰서", "jurisdiction": "서구"},
            {"province": "부산광역시", "city": None, "district": "남구", "station_name": "부산남부경찰서", "jurisdiction": "남구"},
            {"province": "부산광역시", "city": None, "district": "해운대구", "station_name": "부산해운대경찰서", "jurisdiction": "해운대구"},
            {"province": "부산광역시", "city": None, "district": "사상구", "station_name": "부산사상경찰서", "jurisdiction": "사상구"},
            {"province": "부산광역시", "city": None, "district": "금정구", "station_name": "부산금정경찰서", "jurisdiction": "금정구"},
            {"province": "부산광역시", "city": None, "district": "사하구", "station_name": "부산사하경찰서", "jurisdiction": "사하구"},
            {"province": "부산광역시", "city": None, "district": "연제구", "station_name": "부산연제경찰서", "jurisdiction": "연제구"},
            {"province": "부산광역시", "city": None, "district": "강서구", "station_name": "부산강서경찰서", "jurisdiction": "강서구"},
            {"province": "부산광역시", "city": None, "district": "북구", "station_name": "부산북부경찰서", "jurisdiction": "북구"},
            {"province": "부산광역시", "city": None, "district": "기장군", "station_name": "부산기장경찰서", "jurisdiction": "기장군"},
            {"province": "부산광역시", "city": None, "district": "수영구", "station_name": "부산수영경찰서", "jurisdiction": "수영구"},

            # 충청북도 - 청주시는 시 내에 여러 구가 있음
            {"province": "충청북도", "city": "청주시", "district": "흥덕구", "station_name": "청주흥덕경찰서",
             "jurisdiction": "청주시 흥덕구, 서원구 중 성화동, 개신동 일부[충북대학교 병원(의과대학·장례식장 포함), 개신오거리(고가차도 포함), 서부로(충북대병원 장례식장 입구∼개신오거리) 및 두산한솔아파트∼1순환로 727은 제외한다], 죽림동, 남이면, 현도면"},
            {"province": "충청북도", "city": "청주시", "district": "상당구", "station_name": "청주상당경찰서",
             "jurisdiction": "청주시 상당구 일부(청주청원경찰서의 관할 구역은 제외한다), 서원구 중 모충동, 수곡1동, 수곡2동, 산남동, 분평동, 미평동, 장성동, 장암동"},
            {"province": "충청북도", "city": "청주시", "district": "청원구", "station_name": "청주청원경찰서",
             "jurisdiction": "청주시 청원구, 서원구 중 사직1동, 사직2동, 사창동, 개신동 일부(청주흥덕경찰서 관할구역은 제외한다), 상당구 중 북문로2가, 북문로 3가, 수동, 영동(상당공원, 사직대로∼대성로122번길은 제외한다)"},
            {"province": "충청북도", "city": "충주시", "district": None, "station_name": "충주경찰서", "jurisdiction": "충주시"},
            {"province": "충청북도", "city": "제천시", "district": None, "station_name": "제천경찰서", "jurisdiction": "제천시"},
            {"province": "충청북도", "city": None, "district": "영동군", "station_name": "영동경찰서", "jurisdiction": "영동군"},
            {"province": "충청북도", "city": None, "district": "괴산군", "station_name": "괴산경찰서", "jurisdiction": "괴산군, 증평군"},
            {"province": "충청북도", "city": None, "district": "단양군", "station_name": "단양경찰서", "jurisdiction": "단양군"},
            {"province": "충청북도", "city": None, "district": "보은군", "station_name": "보은경찰서", "jurisdiction": "보은군"},
            {"province": "충청북도", "city": None, "district": "옥천군", "station_name": "옥천경찰서", "jurisdiction": "옥천군"},
            {"province": "충청북도", "city": None, "district": "음성군", "station_name": "음성경찰서", "jurisdiction": "음성군"},
            {"province": "충청북도", "city": None, "district": "진천군", "station_name": "진천경찰서", "jurisdiction": "진천군"},

            # 대구광역시
            {"province": "대구광역시", "city": None, "district": "중구", "station_name": "대구중부경찰서", "jurisdiction": "중구"},
            {"province": "대구광역시", "city": None, "district": "동구", "station_name": "대구동부경찰서", "jurisdiction": "동구"},
            {"province": "대구광역시", "city": None, "district": "서구", "station_name": "대구서부경찰서", "jurisdiction": "서구"},
            {"province": "대구광역시", "city": None, "district": "남구", "station_name": "대구남부경찰서", "jurisdiction": "남구"},
            {"province": "대구광역시", "city": None, "district": "북구", "station_name": "대구북부경찰서", "jurisdiction": "북구"},
            {"province": "대구광역시", "city": None, "district": "수성구", "station_name": "대구수성경찰서", "jurisdiction": "수성구"},
            {"province": "대구광역시", "city": None, "district": "달서구", "station_name": "대구달서경찰서", "jurisdiction": "달서구"},
            {"province": "대구광역시", "city": None, "district": "달성군", "station_name": "대구달성경찰서", "jurisdiction": "달성군"},
            {"province": "대구광역시", "city": None, "district": "달서구", "station_name": "대구서부경찰서(성서)", "jurisdiction": "달서구 일부"},

            # 인천광역시
            {"province": "인천광역시", "city": None, "district": "중구", "station_name": "인천중부경찰서", "jurisdiction": "중구"},
            {"province": "인천광역시", "city": None, "district": "동구", "station_name": "인천동부경찰서", "jurisdiction": "동구"},
            {"province": "인천광역시", "city": None, "district": "미추홀구", "station_name": "인천남부경찰서", "jurisdiction": "미추홀구"},
            {"province": "인천광역시", "city": None, "district": "연수구", "station_name": "인천연수경찰서", "jurisdiction": "연수구"},
            {"province": "인천광역시", "city": None, "district": "남동구", "station_name": "인천남동경찰서", "jurisdiction": "남동구"},
            {"province": "인천광역시", "city": None, "district": "부평구", "station_name": "인천부평경찰서", "jurisdiction": "부평구"},
            {"province": "인천광역시", "city": None, "district": "계양구", "station_name": "인천계양경찰서", "jurisdiction": "계양구"},
            {"province": "인천광역시", "city": None, "district": "서구", "station_name": "인천서부경찰서", "jurisdiction": "서구"},
            {"province": "인천광역시", "city": None, "district": "강화군", "station_name": "인천강화경찰서", "jurisdiction": "강화군"},
            {"province": "인천광역시", "city": None, "district": "옹진군", "station_name": "인천옹진경찰서", "jurisdiction": "옹진군"},
            {"province": "인천광역시", "city": None, "district": "중구", "station_name": "인천공항경찰단", "jurisdiction": "인천국제공항"},

            # 광주광역시
            {"province": "광주광역시", "city": None, "district": "동구", "station_name": "광주동부경찰서", "jurisdiction": "동구"},
            {"province": "광주광역시", "city": None, "district": "서구", "station_name": "광주서부경찰서", "jurisdiction": "서구"},
            {"province": "광주광역시", "city": None, "district": "남구", "station_name": "광주남부경찰서", "jurisdiction": "남구"},
            {"province": "광주광역시", "city": None, "district": "북구", "station_name": "광주북부경찰서", "jurisdiction": "북구"},
            {"province": "광주광역시", "city": None, "district": "광산구", "station_name": "광주광산경찰서", "jurisdiction": "광산구"},

            # 대전광역시
            {"province": "대전광역시", "city": None, "district": "중구", "station_name": "대전중부경찰서", "jurisdiction": "중구"},
            {"province": "대전광역시", "city": None, "district": "동구", "station_name": "대전동부경찰서", "jurisdiction": "동구"},
            {"province": "대전광역시", "city": None, "district": "서구", "station_name": "대전서부경찰서", "jurisdiction": "서구"},
            {"province": "대전광역시", "city": None, "district": "유성구", "station_name": "대전유성경찰서", "jurisdiction": "유성구"},
            {"province": "대전광역시", "city": None, "district": "대덕구", "station_name": "대전대덕경찰서", "jurisdiction": "대덕구"},

            # 울산광역시
            {"province": "울산광역시", "city": None, "district": "중구", "station_name": "울산중부경찰서", "jurisdiction": "중구"},
            {"province": "울산광역시", "city": None, "district": "남구", "station_name": "울산남부경찰서", "jurisdiction": "남구"},
            {"province": "울산광역시", "city": None, "district": "동구", "station_name": "울산동부경찰서", "jurisdiction": "동구"},
            {"province": "울산광역시", "city": None, "district": "북구", "station_name": "울산북부경찰서", "jurisdiction": "북구"},
            {"province": "울산광역시", "city": None, "district": "울주군", "station_name": "울산울주경찰서", "jurisdiction": "울주군"},

            # 세종특별자치시
            {"province": "세종특별자치시", "city": None, "district": None, "station_name": "세종경찰서", "jurisdiction": "세종특별자치시"},

            # 경기도
            {"province": "경기도", "city": "수원시", "district": "장안구", "station_name": "수원중부경찰서", "jurisdiction": "수원시 장안구"},
            {"province": "경기도", "city": "수원시", "district": "권선구", "station_name": "수원남부경찰서", "jurisdiction": "수원시 권선구"},
            {"province": "경기도", "city": "수원시", "district": "팔달구", "station_name": "수원중부경찰서", "jurisdiction": "수원시 팔달구"},
            {"province": "경기도", "city": "수원시", "district": "영통구", "station_name": "수원남부경찰서", "jurisdiction": "수원시 영통구"},
            {"province": "경기도", "city": "성남시", "district": "수정구", "station_name": "성남수정경찰서", "jurisdiction": "성남시 수정구"},
            {"province": "경기도", "city": "성남시", "district": "중원구", "station_name": "성남중원경찰서", "jurisdiction": "성남시 중원구"},
            {"province": "경기도", "city": "성남시", "district": "분당구", "station_name": "성남분당경찰서", "jurisdiction": "성남시 분당구"},
            {"province": "경기도", "city": "고양시", "district": "덕양구", "station_name": "고양경찰서", "jurisdiction": "고양시 덕양구"},
            {"province": "경기도", "city": "고양시", "district": "일산동구", "station_name": "고양일산동부경찰서", "jurisdiction": "고양시 일산동구"},
            {"province": "경기도", "city": "고양시", "district": "일산서구", "station_name": "고양일산서부경찰서", "jurisdiction": "고양시 일산서구"},
            {"province": "경기도", "city": "용인시", "district": "처인구", "station_name": "용인동부경찰서", "jurisdiction": "용인시 처인구"},
            {"province": "경기도", "city": "용인시", "district": "기흥구", "station_name": "용인서부경찰서", "jurisdiction": "용인시 기흥구"},
            {"province": "경기도", "city": "용인시", "district": "수지구", "station_name": "용인수지경찰서", "jurisdiction": "용인시 수지구"},
            {"province": "경기도", "city": "부천시", "district": None, "station_name": "부천원미경찰서", "jurisdiction": "부천시 원미구"},
            {"province": "경기도", "city": "부천시", "district": None, "station_name": "부천소사경찰서", "jurisdiction": "부천시 소사구"},
            {"province": "경기도", "city": "부천시", "district": None, "station_name": "부천오정경찰서", "jurisdiction": "부천시 오정구"},
            {"province": "경기도", "city": "안산시", "district": "단원구", "station_name": "안산단원경찰서", "jurisdiction": "안산시 단원구"},
            {"province": "경기도", "city": "안산시", "district": "상록구", "station_name": "안산상록경찰서", "jurisdiction": "안산시 상록구"},
            {"province": "경기도", "city": "안양시", "district": "만안구", "station_name": "안양만안경찰서", "jurisdiction": "안양시 만안구"},
            {"province": "경기도", "city": "안양시", "district": "동안구", "station_name": "안양동안경찰서", "jurisdiction": "안양시 동안구"},
            {"province": "경기도", "city": "남양주시", "district": None, "station_name": "남양주경찰서", "jurisdiction": "남양주시"},
            {"province": "경기도", "city": "화성시", "district": None, "station_name": "화성동부경찰서", "jurisdiction": "화성시 동부"},
            {"province": "경기도", "city": "화성시", "district": None, "station_name": "화성서부경찰서", "jurisdiction": "화성시 서부"},
            {"province": "경기도", "city": "평택시", "district": None, "station_name": "평택경찰서", "jurisdiction": "평택시"},
            {"province": "경기도", "city": "의정부시", "district": None, "station_name": "의정부경찰서", "jurisdiction": "의정부시"},
            {"province": "경기도", "city": "시흥시", "district": None, "station_name": "시흥경찰서", "jurisdiction": "시흥시"},
            {"province": "경기도", "city": "파주시", "district": None, "station_name": "파주경찰서", "jurisdiction": "파주시"},
            {"province": "경기도", "city": "김포시", "district": None, "station_name": "김포경찰서", "jurisdiction": "김포시"},
            {"province": "경기도", "city": "광명시", "district": None, "station_name": "광명경찰서", "jurisdiction": "광명시"},
            {"province": "경기도", "city": "광주시", "district": None, "station_name": "광주경찰서", "jurisdiction": "광주시"},
            {"province": "경기도", "city": "군포시", "district": None, "station_name": "군포경찰서", "jurisdiction": "군포시"},
            {"province": "경기도", "city": "이천시", "district": None, "station_name": "이천경찰서", "jurisdiction": "이천시"},
            {"province": "경기도", "city": "양주시", "district": None, "station_name": "양주경찰서", "jurisdiction": "양주시"},
            {"province": "경기도", "city": "오산시", "district": None, "station_name": "오산경찰서", "jurisdiction": "오산시"},
            {"province": "경기도", "city": "구리시", "district": None, "station_name": "구리경찰서", "jurisdiction": "구리시"},
            {"province": "경기도", "city": "안성시", "district": None, "station_name": "안성경찰서", "jurisdiction": "안성시"},
            {"province": "경기도", "city": "포천시", "district": None, "station_name": "포천경찰서", "jurisdiction": "포천시"},
            {"province": "경기도", "city": "의왕시", "district": None, "station_name": "의왕경찰서", "jurisdiction": "의왕시"},
            {"province": "경기도", "city": "하남시", "district": None, "station_name": "하남경찰서", "jurisdiction": "하남시"},
            {"province": "경기도", "city": "여주시", "district": None, "station_name": "여주경찰서", "jurisdiction": "여주시"},
            {"province": "경기도", "city": "양평군", "district": None, "station_name": "양평경찰서", "jurisdiction": "양평군"},
            {"province": "경기도", "city": "동두천시", "district": None, "station_name": "동두천경찰서", "jurisdiction": "동두천시"},
            {"province": "경기도", "city": "과천시", "district": None, "station_name": "과천경찰서", "jurisdiction": "과천시"},
            {"province": "경기도", "city": "가평군", "district": None, "station_name": "가평경찰서", "jurisdiction": "가평군"},
            {"province": "경기도", "city": "연천군", "district": None, "station_name": "연천경찰서", "jurisdiction": "연천군"},

            # 강원도
            {"province": "강원도", "city": "춘천시", "district": None, "station_name": "춘천경찰서", "jurisdiction": "춘천시"},
            {"province": "강원도", "city": "원주시", "district": None, "station_name": "원주경찰서", "jurisdiction": "원주시"},
            {"province": "강원도", "city": "강릉시", "district": None, "station_name": "강릉경찰서", "jurisdiction": "강릉시"},
            {"province": "강원도", "city": "동해시", "district": None, "station_name": "동해경찰서", "jurisdiction": "동해시"},
            {"province": "강원도", "city": "태백시", "district": None, "station_name": "태백경찰서", "jurisdiction": "태백시"},
            {"province": "강원도", "city": "속초시", "district": None, "station_name": "속초경찰서", "jurisdiction": "속초시"},
            {"province": "강원도", "city": "삼척시", "district": None, "station_name": "삼척경찰서", "jurisdiction": "삼척시"},
            {"province": "강원도", "city": None, "district": "홍천군", "station_name": "홍천경찰서", "jurisdiction": "홍천군"},
            {"province": "강원도", "city": None, "district": "횡성군", "station_name": "횡성경찰서", "jurisdiction": "횡성군"},
            {"province": "강원도", "city": None, "district": "영월군", "station_name": "영월경찰서", "jurisdiction": "영월군"},
            {"province": "강원도", "city": None, "district": "평창군", "station_name": "평창경찰서", "jurisdiction": "평창군"},
            {"province": "강원도", "city": None, "district": "정선군", "station_name": "정선경찰서", "jurisdiction": "정선군"},
            {"province": "강원도", "city": None, "district": "철원군", "station_name": "철원경찰서", "jurisdiction": "철원군"},
            {"province": "강원도", "city": None, "district": "화천군", "station_name": "화천경찰서", "jurisdiction": "화천군"},
            {"province": "강원도", "city": None, "district": "양구군", "station_name": "양구경찰서", "jurisdiction": "양구군"},
            {"province": "강원도", "city": None, "district": "인제군", "station_name": "인제경찰서", "jurisdiction": "인제군"},
            {"province": "강원도", "city": None, "district": "고성군", "station_name": "고성경찰서", "jurisdiction": "고성군"},
            {"province": "강원도", "city": None, "district": "양양군", "station_name": "양양경찰서", "jurisdiction": "양양군"},

            # 충청남도
            {"province": "충청남도", "city": "천안시", "district": "동남구", "station_name": "천안동남경찰서", "jurisdiction": "천안시 동남구"},
            {"province": "충청남도", "city": "천안시", "district": "서북구", "station_name": "천안서북경찰서", "jurisdiction": "천안시 서북구"},
            {"province": "충청남도", "city": "공주시", "district": None, "station_name": "공주경찰서", "jurisdiction": "공주시"},
            {"province": "충청남도", "city": "보령시", "district": None, "station_name": "보령경찰서", "jurisdiction": "보령시"},
            {"province": "충청남도", "city": "아산시", "district": None, "station_name": "아산경찰서", "jurisdiction": "아산시"},
            {"province": "충청남도", "city": "서산시", "district": None, "station_name": "서산경찰서", "jurisdiction": "서산시"},
            {"province": "충청남도", "city": "논산시", "district": None, "station_name": "논산경찰서", "jurisdiction": "논산시"},
            {"province": "충청남도", "city": "계룡시", "district": None, "station_name": "계룡경찰서", "jurisdiction": "계룡시"},
            {"province": "충청남도", "city": "당진시", "district": None, "station_name": "당진경찰서", "jurisdiction": "당진시"},
            {"province": "충청남도", "city": None, "district": "금산군", "station_name": "금산경찰서", "jurisdiction": "금산군"},
            {"province": "충청남도", "city": None, "district": "부여군", "station_name": "부여경찰서", "jurisdiction": "부여군"},
            {"province": "충청남도", "city": None, "district": "서천군", "station_name": "서천경찰서", "jurisdiction": "서천군"},
            {"province": "충청남도", "city": None, "district": "청양군", "station_name": "청양경찰서", "jurisdiction": "청양군"},
            {"province": "충청남도", "city": None, "district": "홍성군", "station_name": "홍성경찰서", "jurisdiction": "홍성군"},
            {"province": "충청남도", "city": None, "district": "예산군", "station_name": "예산경찰서", "jurisdiction": "예산군"},
            {"province": "충청남도", "city": None, "district": "태안군", "station_name": "태안경찰서", "jurisdiction": "태안군"},

            # 전라북도
            {"province": "전라북도", "city": "전주시", "district": "완산구", "station_name": "전주완산경찰서", "jurisdiction": "전주시 완산구"},
            {"province": "전라북도", "city": "전주시", "district": "덕진구", "station_name": "전주덕진경찰서", "jurisdiction": "전주시 덕진구"},
            {"province": "전라북도", "city": "군산시", "district": None, "station_name": "군산경찰서", "jurisdiction": "군산시"},
            {"province": "전라북도", "city": "익산시", "district": None, "station_name": "익산경찰서", "jurisdiction": "익산시"},
            {"province": "전라북도", "city": "정읍시", "district": None, "station_name": "정읍경찰서", "jurisdiction": "정읍시"},
            {"province": "전라북도", "city": "남원시", "district": None, "station_name": "남원경찰서", "jurisdiction": "남원시"},
            {"province": "전라북도", "city": "김제시", "district": None, "station_name": "김제경찰서", "jurisdiction": "김제시"},
            {"province": "전라북도", "city": None, "district": "완주군", "station_name": "완주경찰서", "jurisdiction": "완주군"},
            {"province": "전라북도", "city": None, "district": "진안군", "station_name": "진안경찰서", "jurisdiction": "진안군"},
            {"province": "전라북도", "city": None, "district": "무주군", "station_name": "무주경찰서", "jurisdiction": "무주군"},
            {"province": "전라북도", "city": None, "district": "장수군", "station_name": "장수경찰서", "jurisdiction": "장수군"},
            {"province": "전라북도", "city": None, "district": "임실군", "station_name": "임실경찰서", "jurisdiction": "임실군"},
            {"province": "전라북도", "city": None, "district": "순창군", "station_name": "순창경찰서", "jurisdiction": "순창군"},
            {"province": "전라북도", "city": None, "district": "고창군", "station_name": "고창경찰서", "jurisdiction": "고창군"},
            {"province": "전라북도", "city": None, "district": "부안군", "station_name": "부안경찰서", "jurisdiction": "부안군"},

            # 전라남도
            {"province": "전라남도", "city": "목포시", "district": None, "station_name": "목포경찰서", "jurisdiction": "목포시"},
            {"province": "전라남도", "city": "여수시", "district": None, "station_name": "여수경찰서", "jurisdiction": "여수시"},
            {"province": "전라남도", "city": "순천시", "district": None, "station_name": "순천경찰서", "jurisdiction": "순천시"},
            {"province": "전라남도", "city": "나주시", "district": None, "station_name": "나주경찰서", "jurisdiction": "나주시"},
            {"province": "전라남도", "city": "광양시", "district": None, "station_name": "광양경찰서", "jurisdiction": "광양시"},
            {"province": "전라남도", "city": None, "district": "담양군", "station_name": "담양경찰서", "jurisdiction": "담양군"},
            {"province": "전라남도", "city": None, "district": "곡성군", "station_name": "곡성경찰서", "jurisdiction": "곡성군"},
            {"province": "전라남도", "city": None, "district": "구례군", "station_name": "구례경찰서", "jurisdiction": "구례군"},
            {"province": "전라남도", "city": None, "district": "고흥군", "station_name": "고흥경찰서", "jurisdiction": "고흥군"},
            {"province": "전라남도", "city": None, "district": "보성군", "station_name": "보성경찰서", "jurisdiction": "보성군"},
            {"province": "전라남도", "city": None, "district": "화순군", "station_name": "화순경찰서", "jurisdiction": "화순군"},
            {"province": "전라남도", "city": None, "district": "장흥군", "station_name": "장흥경찰서", "jurisdiction": "장흥군"},
            {"province": "전라남도", "city": None, "district": "강진군", "station_name": "강진경찰서", "jurisdiction": "강진군"},
            {"province": "전라남도", "city": None, "district": "해남군", "station_name": "해남경찰서", "jurisdiction": "해남군"},
            {"province": "전라남도", "city": None, "district": "영암군", "station_name": "영암경찰서", "jurisdiction": "영암군"},
            {"province": "전라남도", "city": None, "district": "무안군", "station_name": "무안경찰서", "jurisdiction": "무안군"},
            {"province": "전라남도", "city": None, "district": "함평군", "station_name": "함평경찰서", "jurisdiction": "함평군"},
            {"province": "전라남도", "city": None, "district": "영광군", "station_name": "영광경찰서", "jurisdiction": "영광군"},
            {"province": "전라남도", "city": None, "district": "장성군", "station_name": "장성경찰서", "jurisdiction": "장성군"},
            {"province": "전라남도", "city": None, "district": "완도군", "station_name": "완도경찰서", "jurisdiction": "완도군"},
            {"province": "전라남도", "city": None, "district": "진도군", "station_name": "진도경찰서", "jurisdiction": "진도군"},
            {"province": "전라남도", "city": None, "district": "신안군", "station_name": "신안경찰서", "jurisdiction": "신안군"},

            # 경상북도
            {"province": "경상북도", "city": "포항시", "district": "남구", "station_name": "포항남부경찰서", "jurisdiction": "포항시 남구"},
            {"province": "경상북도", "city": "포항시", "district": "북구", "station_name": "포항북부경찰서", "jurisdiction": "포항시 북구"},
            {"province": "경상북도", "city": "경주시", "district": None, "station_name": "경주경찰서", "jurisdiction": "경주시"},
            {"province": "경상북도", "city": "김천시", "district": None, "station_name": "김천경찰서", "jurisdiction": "김천시"},
            {"province": "경상북도", "city": "안동시", "district": None, "station_name": "안동경찰서", "jurisdiction": "안동시"},
            {"province": "경상북도", "city": "구미시", "district": None, "station_name": "구미경찰서", "jurisdiction": "구미시"},
            {"province": "경상북도", "city": "영주시", "district": None, "station_name": "영주경찰서", "jurisdiction": "영주시"},
            {"province": "경상북도", "city": "영천시", "district": None, "station_name": "영천경찰서", "jurisdiction": "영천시"},
            {"province": "경상북도", "city": "상주시", "district": None, "station_name": "상주경찰서", "jurisdiction": "상주시"},
            {"province": "경상북도", "city": "문경시", "district": None, "station_name": "문경경찰서", "jurisdiction": "문경시"},
            {"province": "경상북도", "city": "경산시", "district": None, "station_name": "경산경찰서", "jurisdiction": "경산시"},
            {"province": "경상북도", "city": None, "district": "의성군", "station_name": "의성경찰서", "jurisdiction": "의성군"},
            {"province": "경상북도", "city": None, "district": "청송군", "station_name": "청송경찰서", "jurisdiction": "청송군"},
            {"province": "경상북도", "city": None, "district": "영양군", "station_name": "영양경찰서", "jurisdiction": "영양군"},
            {"province": "경상북도", "city": None, "district": "영덕군", "station_name": "영덕경찰서", "jurisdiction": "영덕군"},
            {"province": "경상북도", "city": None, "district": "청도군", "station_name": "청도경찰서", "jurisdiction": "청도군"},
            {"province": "경상북도", "city": None, "district": "고령군", "station_name": "고령경찰서", "jurisdiction": "고령군"},
            {"province": "경상북도", "city": None, "district": "성주군", "station_name": "성주경찰서", "jurisdiction": "성주군"},
            {"province": "경상북도", "city": None, "district": "칠곡군", "station_name": "칠곡경찰서", "jurisdiction": "칠곡군"},
            {"province": "경상북도", "city": None, "district": "예천군", "station_name": "예천경찰서", "jurisdiction": "예천군"},
            {"province": "경상북도", "city": None, "district": "봉화군", "station_name": "봉화경찰서", "jurisdiction": "봉화군"},
            {"province": "경상북도", "city": None, "district": "울진군", "station_name": "울진경찰서", "jurisdiction": "울진군"},
            {"province": "경상북도", "city": None, "district": "울릉군", "station_name": "울릉경찰서", "jurisdiction": "울릉군"},

            # 경상남도
            {"province": "경상남도", "city": "창원시", "district": "의창구", "station_name": "창원중부경찰서", "jurisdiction": "창원시 의창구"},
            {"province": "경상남도", "city": "창원시", "district": "성산구", "station_name": "창원성산경찰서", "jurisdiction": "창원시 성산구"},
            {"province": "경상남도", "city": "창원시", "district": "마산합포구", "station_name": "창원마산경찰서", "jurisdiction": "창원시 마산합포구, 마산회원구"},
            {"province": "경상남도", "city": "창원시", "district": "진해구", "station_name": "창원진해경찰서", "jurisdiction": "창원시 진해구"},
            {"province": "경상남도", "city": "진주시", "district": None, "station_name": "진주경찰서", "jurisdiction": "진주시"},
            {"province": "경상남도", "city": "통영시", "district": None, "station_name": "통영경찰서", "jurisdiction": "통영시"},
            {"province": "경상남도", "city": "사천시", "district": None, "station_name": "사천경찰서", "jurisdiction": "사천시"},
            {"province": "경상남도", "city": "김해시", "district": None, "station_name": "김해경찰서", "jurisdiction": "김해시"},
            {"province": "경상남도", "city": "밀양시", "district": None, "station_name": "밀양경찰서", "jurisdiction": "밀양시"},
            {"province": "경상남도", "city": "거제시", "district": None, "station_name": "거제경찰서", "jurisdiction": "거제시"},
            {"province": "경상남도", "city": "양산시", "district": None, "station_name": "양산경찰서", "jurisdiction": "양산시"},
            {"province": "경상남도", "city": None, "district": "의령군", "station_name": "의령경찰서", "jurisdiction": "의령군"},
            {"province": "경상남도", "city": None, "district": "함안군", "station_name": "함안경찰서", "jurisdiction": "함안군"},
            {"province": "경상남도", "city": None, "district": "창녕군", "station_name": "창녕경찰서", "jurisdiction": "창녕군"},
            {"province": "경상남도", "city": None, "district": "고성군", "station_name": "고성경찰서", "jurisdiction": "고성군"},
            {"province": "경상남도", "city": None, "district": "남해군", "station_name": "남해경찰서", "jurisdiction": "남해군"},
            {"province": "경상남도", "city": None, "district": "하동군", "station_name": "하동경찰서", "jurisdiction": "하동군"},
            {"province": "경상남도", "city": None, "district": "산청군", "station_name": "산청경찰서", "jurisdiction": "산청군"},
            {"province": "경상남도", "city": None, "district": "함양군", "station_name": "함양경찰서", "jurisdiction": "함양군"},
            {"province": "경상남도", "city": None, "district": "거창군", "station_name": "거창경찰서", "jurisdiction": "거창군"},
            {"province": "경상남도", "city": None, "district": "합천군", "station_name": "합천경찰서", "jurisdiction": "합천군"},

            # 제주특별자치도
            {"province": "제주특별자치도", "city": "제주시", "district": None, "station_name": "제주동부경찰서", "jurisdiction": "제주시 동부"},
            {"province": "제주특별자치도", "city": "제주시", "district": None, "station_name": "제주서부경찰서", "jurisdiction": "제주시 서부"},
            {"province": "제주특별자치도", "city": "서귀포시", "district": None, "station_name": "서귀포경찰서", "jurisdiction": "서귀포시"},
        ]

        # 데이터 삽입
        for station_data in police_stations:
            station = PoliceStation(**station_data)
            db.add(station)

        db.commit()
        print(f"✅ {len(police_stations)}개의 경찰서 데이터가 성공적으로 삽입되었습니다.")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("경찰서 데이터 시딩 시작...")
    seed_police_stations()
    print("완료!")
