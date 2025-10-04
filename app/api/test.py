from fastapi import APIRouter

router = APIRouter(prefix="/api/test", tags=["Test"])

@router.get("/hello")
def hello():
    return {"message": "Hello from API!"}

@router.post("/echo")
def echo(text: str):
    return {"you_said": text}