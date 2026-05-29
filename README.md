# 바로(BaLaw) - Baro Server

`Baro-Server`는 바로(BaLaw) 서비스의 FastAPI 기반 백엔드 API 서버입니다.
사용자 인증, 고소장 작성 상태 관리, 개인정보 암호화 저장, Baro-AI 연동, 채팅 내역 저장, 관할 경찰서 매핑, 최종 고소장 DOCX 생성 및 다운로드를 담당합니다.

## 배포 구조

현재 백엔드와 AI 서비스는 AWS EC2에서 Docker Compose 기반으로 운영됩니다.
프론트엔드는 Vercel에서 별도로 배포되며, 백엔드는 내부 Docker 네트워크를 통해 `Baro-AI` 컨테이너와 통신합니다.

```text
Client / Vercel Frontend
  ↓
EC2: baro-backend (FastAPI)
  ├── PostgreSQL: 사용자, 고소장, 채팅 내역 저장
  ├── Fernet: 개인정보 및 고소장 본문 암호화
  ├── Baro-AI: 사건 분석, 보충 질문, 고소장 문안 생성
  ├── Police Station DB: 주소 기반 관할 경찰서 안내
  └── python-docx: DOCX 고소장 생성
```

운영 배포 설정은 `Baro-Deploy` 레포의 `docker-compose.prod.yml`에서 관리합니다.
`Baro-Server` 또는 `Baro-AI`의 배포 대상 브랜치에 push하면 각 레포의 GitHub Actions가 `Baro-Deploy` 배포 workflow를 호출하고, EC2에서 최신 코드를 pull한 뒤 컨테이너를 재빌드 및 재시작합니다.

## 주요 기능

- **인증**
  - 회원가입 및 로그인
  - 이메일 중복 확인
  - JWT Access Token / Refresh Token 발급
  - 비밀번호 Argon2 해싱

- **고소장 작성 상태 관리**
  - 고소인 정보 등록 시 고소장 레코드 생성
  - 피고소인 정보, 관련 형사사건, 민사소송, 증거 제출 여부 저장
  - 작성 중인 고소장 목록 조회 및 삭제
  - 작성 완료 상태 및 다운로드 시점 관리

- **Baro-AI 연동**
  - `/chat/init`, `/chat/send`, `/chat/compose`, `/chat/restore` API 호출
  - 사건 개요 기반 죄목 추정 및 유사 판례 결과 전달
  - AI 세션 ID 저장
  - AI 컨테이너 재시작 등으로 세션이 유실된 경우 저장된 채팅 내역 기반 세션 복원

- **채팅 내역 저장**
  - 사용자 메시지와 AI 응답을 고소장별로 저장
  - 이어쓰기 진입 시 기존 대화 내역 조회
  - 저장된 대화 내역을 기반으로 AI 세션 복원 지원

- **고소장 생성 및 다운로드**
  - AI가 생성한 `범죄사실`, `고소이유` 저장
  - 입력 주소 기반 관할 가능성이 높은 경찰서 자동 매핑
  - `python-docx` 기반 DOCX 파일 생성
  - 다운로드 시점 기록

- **보안 및 데이터 관리**
  - 사용자 이름, 주소, 전화번호 암호화
  - 고소인/피고소인 개인정보 암호화
  - 사건 개요, 범죄사실, 고소이유, 생성 고소장 본문 암호화
  - 다운로드 후 1일이 지난 고소장 및 연관 채팅 데이터 자동 삭제

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| Framework | FastAPI, Uvicorn |
| Database | PostgreSQL, SQLAlchemy |
| Migration | Alembic |
| Auth | JWT, python-jose, Argon2 |
| Encryption | Fernet |
| Scheduler | APScheduler |
| External Service | Baro-AI, OpenAI API 설정 전달 |
| Document | python-docx |
| Deployment | Docker, Docker Compose, AWS EC2, GitHub Actions |

## 프로젝트 구조

```text
.
├── app/
│   ├── api/
│   │   ├── auth.py              # 인증 API
│   │   ├── complaint.py         # 고소장, 채팅, DOCX API
│   │   └── test.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── models/                  # SQLAlchemy 모델
│   ├── schemas/                 # Pydantic 스키마
│   ├── services/
│   │   ├── ai_service.py        # Baro-AI 클라이언트
│   │   ├── auth_service.py      # JWT 및 비밀번호 처리
│   │   ├── docx_service.py      # DOCX 생성
│   │   ├── encryption_service.py# Fernet 암복호화
│   │   └── scheduler_service.py # 다운로드 후 TTL 삭제
│   ├── utils/
│   │   └── address_parser.py    # 주소 기반 관할 경찰서 조회
│   ├── config.py
│   ├── database.py
│   └── main.py
├── alembic/                     # DB 마이그레이션
├── scripts/
│   └── seed_police_stations.py  # 경찰서 관할 데이터 초기 적재
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
└── alembic.ini
```

## 환경 변수

로컬 실행 시 `.env`에 아래 값을 설정합니다.
운영 환경에서는 `Baro-Deploy`의 Docker Compose 실행 경로에 `.env`를 배치합니다.

```env
DATABASE_URL=postgresql://user:password@localhost:5432/baro_db
SECRET_KEY=change-this-secret-key
ENCRYPTION_KEY=change-this-fernet-key
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5-mini
BARO_AI_URL=http://localhost:8001
```

운영 Docker Compose에서는 `DATABASE_URL`이 Compose 환경변수로 조합되며, `BARO_AI_URL`은 내부 Docker 네트워크 주소인 `http://baro-ai:8000`을 사용합니다.

## 로컬 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m scripts.seed_police_stations
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

헬스 체크:

```bash
curl http://localhost:8000/health
```

## Docker 실행

레포 단독 실행보다는 `Baro-Deploy`의 `docker-compose.prod.yml`을 통해 `postgres`, `baro-ai`, `baro-backend`를 함께 실행하는 방식을 기준으로 합니다.

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
```

컨테이너 시작 시 `entrypoint.sh`가 Alembic 마이그레이션을 적용하고, 경찰서 관할 데이터가 비어 있으면 초기 데이터를 적재한 뒤 FastAPI 서버를 시작합니다.

## CI/CD

이 레포에는 `Request EC2 Deploy` GitHub Actions workflow가 포함되어 있습니다.
배포 대상 브랜치에 백엔드 코드가 push되면 `Baro-Deploy` 레포의 배포 workflow를 호출합니다.

배포 workflow는 다음 순서로 동작합니다.

```text
Baro-Server push
  ↓
Request EC2 Deploy
  ↓
Baro-Deploy repository_dispatch
  ↓
EC2 SSH 접속
  ↓
Baro-AI / baro-backend git pull
  ↓
docker compose up -d --build
```

EC2 SSH 포트는 상시 전체 공개하지 않고, GitHub Actions runner의 공인 IP만 보안 그룹에 임시 허용한 뒤 배포가 끝나면 해당 규칙을 제거합니다.

## 라이선스

캡스톤 디자인 프로젝트 - 교육용

## 팀

중앙대학교 소프트웨어학부 캡스톤 디자인 팀
