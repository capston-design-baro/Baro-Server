# 바로(BaLaw) - AI 기반 고소장 작성 서비스

캡스톤 디자인 프로젝트: 사용자와 AI의 대화를 통해 자동으로 고소장을 작성하는 서비스

## 🚀 배포된 서비스

- **Backend API**: https://baro-server.onrender.com
- **API 문서 (Swagger)**: https://baro-server.onrender.com/docs

> ⚠️ **Sleep 모드**: 15분 미사용 시 sleep 상태 진입. 첫 요청 시 30초-1분 소요됩니다.

## 기술 스택

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **AI Service**: FastAPI, OpenAI API
- **Authentication**: JWT, Argon2
- **Encryption**: Fernet (개인정보 암호화)
- **Deployment**: Docker, Render
- **Database**: PostgreSQL 17

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

## 라이센스

캡스톤 디자인 프로젝트 - 교육용

## 팀
중앙대 소프트웨어학부 캡스톤 디자인 팀
