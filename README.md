# 바로(BaLaw) - AI 기반 고소장 작성 서비스
바로(BaLaw)는 사용자가 사건 정보를 입력하고 AI와 대화하면 고소장 초안을 작성할 수 있도록 돕는 서비스입니다. 

`baro-server`는 바로(BaLaw) 서비스의 백엔드 API 서버입니다. 
사용자 인증, 고소장 작성 상태 관리, 개인정보 암호화 저장, Baro-AI 연동, 채팅 내역 저장, 최종 고소장 DOCX 생성 및 다운로드를 담당합니다.


## 🚀 배포된 서비스

- **BaLaw web site**: https://baro-front-five.vercel.app/
- **Backend API**: https://baro-server.onrender.com
- **API 문서 (Swagger)**: https://baro-server.onrender.com/docs

⚠️ 배포 링크 안내
> 현재 본 서비스는 프로젝트 종료 및 클라우드(Render) 인프라 비용 최적화를 위해 서버 가동을 일시 중단(Suspend)한 상태입니다.
서비스 아키텍처 및 핵심 비즈니스 로직은 본 레포지토리의 코드와 Closed PR 목록을 통해 확인하실 수 있습니다.

## 아키텍쳐 구조
<img width="1423" height="666" alt="캡스톤디자인(1) 최종 발표" src="https://github.com/user-attachments/assets/28c4fc2d-3c53-44b0-87a9-58afbbdc8580" />


## 주요 기능

- **인증**
  - 이메일 중복 확인
  - 회원가입 및 로그인
  - JWT Access Token / Refresh Token 발급
  - 비밀번호 Argon2 해싱

- **고소장 작성 상태 관리**
  - 고소인 정보 등록 시 고소장 레코드 생성
  - 피고소인 정보, 관련 사건 여부, 증거 제출 여부 저장
  - 작성 중인 고소장 목록 조회 및 삭제
  - 작성 완료 상태 관리

- **AI 서비스 연동**
  - Baro-AI `/chat/init`, `/chat/send`, `/chat/compose` API 호출
  - 사건 개요 기반 죄목 추정 및 유사 판례 결과 전달
  - AI 채팅 세션 ID 저장
  - AI 서버 재시작 또는 Render sleep 이후 세션 복원

- **채팅 내역 저장**
  - 사용자 메시지와 AI 응답을 고소장별로 저장
  - 이어쓰기 진입 시 기존 대화 내역 조회

- **고소장 생성 및 다운로드**
  - AI가 생성한 `범죄사실`, `고소이유` 저장
  - 관할 경찰서 자동 매핑
  - `python-docx` 기반 DOCX 파일 생성
  - 다운로드 시점 기록

- **보안 및 데이터 관리**
  - 사용자 이름, 주소, 전화번호 암호화
  - 고소인/피고소인 개인정보 암호화
  - 생성된 고소장 본문 암호화
  - 다운로드 후 1일이 지난 고소장 자동 삭제

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| Framework | FastAPI|
| Database | PostgreSQL, SQLAlchemy |
| Migration | Alembic |
| Auth | JWT, python-jose, Argon2 |
| Encryption | Fernet |
| External API | Baro-AI, OpenAI API 설정 전달 |
| Document | python-docx |
| Deployment | Docker, Render |

## 프로젝트 구조

```text
.
├── app/
│   ├── api/                 # FastAPI 라우터
│   │   ├── auth.py          # 인증 API
│   │   ├── complaint.py     # 고소장/채팅/DOCX API
│   │   └── test.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── models/              # SQLAlchemy 모델
│   ├── schemas/             # Pydantic 스키마
│   ├── services/
│   │   ├── ai_service.py          # Baro-AI 클라이언트
│   │   ├── auth_service.py        # JWT/비밀번호 처리
│   │   ├── docx_service.py        # DOCX 생성
│   │   ├── encryption_service.py  # Fernet 암복호화
│   │   └── scheduler_service.py   # 다운로드 후 TTL 삭제
│   ├── utils/
│   │   └── address_parser.py      # 주소 기반 관할 경찰서 조회
│   ├── config.py
│   ├── database.py
│   └── main.py
├── alembic/                 # DB 마이그레이션
├── scripts/
│   └── seed_police_stations.py
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
└── alembic.ini
```

## 서버 흐름

```text
Client
  ↓
FastAPI baro-server
  ├── Auth: 회원가입, 로그인, 토큰 재발급
  ├── PostgreSQL: 사용자, 고소장, 채팅 내역 저장
  ├── Fernet: 개인정보 및 고소장 본문 암호화
  ├── Baro-AI: 사건 분석, 보충 질문, 고소장 문안 생성
  ├── Police Station DB: 관할 경찰서 자동 입력
  └── python-docx: DOCX 고소장 다운로드
```
## 라이센스

캡스톤 디자인 프로젝트 - 교육용

## 팀
중앙대 소프트웨어학부 캡스톤 디자인 팀
