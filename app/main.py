from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import SecuritySchemeType, HTTPBearer, HTTPBase
from fastapi.security import HTTPBearer as HTTPBearerSecurity
from contextlib import asynccontextmanager
from app.api import test, auth, complaint
from app.models import user, complaint as complaint_model, chat_message
from app.database import engine, Base
from app.services.scheduler_service import scheduler_service

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시
    scheduler_service.start()
    yield
    # 애플리케이션 종료 시
    scheduler_service.shutdown()

app = FastAPI(
    title="바로(Baro) - 고소장 작성 서비스 API",
    description="AI 기반 고소장 자동 작성 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://baro-front-five.vercel.app",
        "https://baro-front-qlq4xlmhw-soyeons-projects-0593c180.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(test.router)
app.include_router(auth.router)
app.include_router(complaint.router)

@app.get("/")
def read_root():
    return {"message": "바로(Baro) API - 고소장 작성 서비스"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
