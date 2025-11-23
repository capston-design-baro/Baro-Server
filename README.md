# 바로(BaLaw) - AI 기반 고소장 작성 서비스

캡스톤 디자인 프로젝트: 사용자와 AI의 대화를 통해 자동으로 고소장을 작성하는 서비스

## 🚀 배포된 서비스

- **Backend API**: https://baro-server.onrender.com
- **API 문서 (Swagger)**: https://baro-server.onrender.com/docs
- **Health Check**: https://baro-server.onrender.com/health
- **Database**: PostgreSQL (Render)

> ⚠️ **Sleep 모드**: 15분 미사용 시 sleep 상태 진입. 첫 요청 시 30초-1분 소요됩니다.

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

## API 테스트

### Health Check
```bash
curl https://baro-server.onrender.com/health
```

### API 문서 확인
브라우저에서 접속: https://baro-server.onrender.com/docs

## 로컬 개발 환경 설정

### 1. 사전 요구사항

- Docker Desktop 설치
- Python 3.13+
- OpenAI API Key

### 2. 환경변수 설정

`.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일 내용:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/baro_db

# Security Keys
SECRET_KEY=your-secret-key-min-32-chars
ENCRYPTION_KEY=your-base64-encoded-key

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini

# Baro-AI Service
BARO_AI_URL=http://localhost:8001
```

**ENCRYPTION_KEY 생성 방법:**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Docker로 실행 (권장)

```bash
# 이미지 빌드
docker build -t baro-backend .

# 컨테이너 실행
docker run -p 8000:8000 --env-file .env baro-backend

# 또는 루트에서 docker-compose 사용
cd ..
docker compose up -d
```

### 4. 가상환경으로 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 서비스 확인

- **Backend API**: http://localhost:8000/health
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc


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
# Alembic 마이그레이션
alembic revision --autogenerate -m "description"
alembic upgrade head

# Docker 사용 시
docker exec -it baro-backend alembic upgrade head
```

### 로그 확인

```bash
# 로컬 Docker
docker logs -f baro-backend

# Render
Render 대시보드 → Logs 탭
```

## 라이센스

캡스톤 디자인 프로젝트 - 교육용

## 팀

중앙대학교 소프트웨어학부 캡스톤 디자인 팀