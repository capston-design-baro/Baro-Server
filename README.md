# 바로(Baro) - AI 기반 고소장 작성 서비스

캡스톤 디자인 프로젝트: 사용자와 AI의 대화를 통해 자동으로 고소장을 작성하는 서비스

## 프로젝트 구조

```
baro/
├── baro-backend/          # FastAPI 백엔드 서버 (PostgreSQL 연동)
├── Baro-AI/               # AI 대화 서비스 (OpenAI API)
├── docker-compose.yml     # 로컬 개발용 Docker 설정
└── README.md
```

## 기술 스택

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **AI Service**: FastAPI, OpenAI API
- **Authentication**: JWT, Argon2
- **Encryption**: Fernet (개인정보 암호화)
- **Deployment**: Docker, Render
- **Database**: PostgreSQL 17

## 로컬 개발 환경 설정

### 1. 사전 요구사항

- Docker Desktop 설치
- Python 3.11+ (로컬 개발 시)
- OpenAI API Key

### 2. 환경변수 설정

루트 디렉토리에 `.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일 내용:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini

# Backend Security Keys
SECRET_KEY=your-secret-key-min-32-chars
ENCRYPTION_KEY=your-base64-encoded-key
```

**ENCRYPTION_KEY 생성 방법:**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Docker로 실행

```bash
# 이미지 빌드
docker compose build

# 컨테이너 실행 (백그라운드)
docker compose up -d

# 로그 확인
docker compose logs -f

# 중지
docker compose down
```

### 4. 서비스 확인

- **Backend API**: http://localhost:8000/health
- **AI Service**: http://localhost:8001/
- **PostgreSQL**: localhost:5433

### 5. API 문서

- **Backend Swagger UI**: http://localhost:8000/docs
- **Backend ReDoc**: http://localhost:8000/redoc

## Render 배포 가이드

### 1. GitHub에 코드 푸시

```bash
git add .
git commit -m "feat: Add Docker configuration"
git push origin <branch-name>
```

### 2. PostgreSQL 데이터베이스 생성

1. [Render](https://render.com) 로그인
2. **New +** → **PostgreSQL**
3. 설정:
   - Name: `baro-postgres`
   - Region: **Singapore**
   - Instance Type: **Free**
4. **Internal Database URL** 복사

### 3. Baro-AI 서비스 배포

1. **New +** → **Web Service**
2. GitHub 저장소 연결
3. 설정:
   - Name: `baro-ai`
   - Region: **Singapore**
   - Root Directory: `Baro-AI`
   - Runtime: **Docker**
   - Instance Type: **Free**
4. 환경변수:
   ```
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   ```
5. Health Check Path: `/`
6. **Create Web Service** → URL 복사

### 4. Baro-Backend 서비스 배포

1. **New +** → **Web Service**
2. 동일한 저장소 선택
3. 설정:
   - Name: `baro-backend`
   - Region: **Singapore**
   - Root Directory: `baro-backend`
   - Runtime: **Docker**
   - Instance Type: **Free**
4. 환경변수:
   ```
   DATABASE_URL=<PostgreSQL Internal URL>
   SECRET_KEY=your-production-secret-key
   ENCRYPTION_KEY=<generated-key>
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   BARO_AI_URL=https://baro-ai-xxxx.onrender.com
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```
5. Health Check Path: `/health`
6. **Create Web Service**

### 5. 자동 배포

Git push 시 자동으로 재배포됩니다:

```bash
git push origin <branch>
# 5-10분 후 자동 배포 완료
```

## 주요 기능

### 사용자 인증
- 회원가입/로그인 (JWT)
- Access Token + Refresh Token
- 비밀번호 Argon2 해싱

### 고소장 작성
1. 고소인/피고소인 정보 입력 (암호화 저장)
2. AI와 대화하며 사건 정보 수집
3. 최종 고소장 생성 (.docx 다운로드)

### 보안
- 개인정보 Fernet 암호화
- JWT 토큰 기반 인증
- HTTPS (Render 자동 제공)

## 개발 팁

### 데이터베이스 마이그레이션

```bash
# 컨테이너 내부 접속
docker exec -it baro-backend bash

# Alembic 마이그레이션
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### 로그 확인

```bash
# 전체 로그
docker compose logs -f

# 특정 서비스
docker compose logs -f baro-backend
docker compose logs -f baro-ai
```

### PostgreSQL 접속

```bash
# Docker 컨테이너 내부 접속
docker exec -it baro-postgres psql -U baro -d baro_db
```

## Render 무료 플랜 제약사항

- **Sleep 모드**: 15분 미사용 시 sleep (첫 요청 시 30초-1분 소요)
- **월 750시간 제한**: 서비스당
- **PostgreSQL 1GB 제한**

**발표 팁**: 발표 30분 전에 미리 접속해서 서비스를 깨워두세요!

## 트러블슈팅

### Docker 빌드 실패
- `chromadb` 컴파일 에러: Dockerfile에 `g++` 추가 확인
- 포트 충돌: `docker-compose.yml`에서 포트 변경

### 데이터베이스 연결 실패
- `DATABASE_URL`이 Internal URL인지 확인
- PostgreSQL 서비스 Running 상태 확인

### CORS 에러
- `baro-backend/app/main.py`의 `allow_origins`에 프론트엔드 URL 추가

## 라이센스

캡스톤 디자인 프로젝트 - 교육용

## 팀

소프트웨어학부 캡스톤 디자인 팀
