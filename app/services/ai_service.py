"""Baro-AI 서비스 호출 클라이언트"""
import httpx
from typing import Dict, Any, List
from app.config import settings


class BaroAIService:
    """Baro-AI API 호출 서비스"""

    def __init__(self):
        self.base_url = settings.BARO_AI_URL
        self.timeout = 200.0

    async def chat_init(self, text: str) -> Dict[str, Any]:
        """
        Baro-AI 채팅 세션 초기화 (사건개요 기반)

        Args:
            text: 사건 개요

        Returns:
            {
                "session_id": str,
                "offense": str,  # AI가 자동 판단한 죄목
                "rag_keyword": str,  # 추정된 범죄 키워드
                "rag_cases": [  # 유사 판례
                    {
                        "case_no": str,
                        "label": str,
                        "text": str
                    }
                ]
            }
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/init",
                    json={"text": text}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = "Baro-AI 서버 내부 오류"
            try:
                error_body = e.response.json()
                error_detail = error_body.get("detail", str(error_body))
            except:
                error_detail = e.response.text or str(e)
            raise RuntimeError(f"Baro-AI 서버 오류 ({e.response.status_code}): {error_detail}")
        except httpx.TimeoutException:
            raise RuntimeError("Baro-AI 서버 응답 시간 초과")
        except httpx.ConnectError:
            raise RuntimeError("Baro-AI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        except Exception as e:
            raise RuntimeError(f"예상치 못한 오류: {str(e)}")

    async def chat_send(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Baro-AI에 메시지 전송 및 응답 받기

        Args:
            session_id: Baro-AI 세션 ID
            message: 사용자 메시지

        Returns:
            {
                "session_id": str,
                "reply": str,
                "caution": bool,
                "progress": {
                    "complete": bool,
                    "elements": dict
                }
            }
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/send",
                    json={
                        "session_id": session_id,
                        "message": message
                    }
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            # Baro-AI 서버 에러 (4xx, 5xx)
            error_detail = "Baro-AI 서버 내부 오류"
            try:
                error_body = e.response.json()
                error_detail = error_body.get("detail", str(error_body))
            except:
                error_detail = e.response.text or str(e)

            raise RuntimeError(f"Baro-AI 서버 오류 ({e.response.status_code}): {error_detail}")
        except httpx.TimeoutException:
            raise RuntimeError("Baro-AI 서버 응답 시간 초과. OpenAI API 키가 설정되어 있는지 확인하세요.")
        except httpx.ConnectError:
            raise RuntimeError("Baro-AI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        except Exception as e:
            raise RuntimeError(f"예상치 못한 오류: {str(e)}")

    async def chat_compose(self, session_id: str) -> Dict[str, Any]:
        """
        Baro-AI에 고소장 작성 요청

        Args:
            session_id: Baro-AI 세션 ID

        Returns:
            {
                "offense": str,
                "title": str,
                "sections": {
                    "criminal_facts": str,  # 범죄사실
                    "accusation_reason": str  # 고소이유
                }
            }
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/compose",
                    json={"session_id": session_id}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = "Baro-AI 서버 내부 오류"
            try:
                error_body = e.response.json()
                error_detail = error_body.get("detail", str(error_body))
            except:
                error_detail = e.response.text or str(e)
            raise RuntimeError(f"Baro-AI 서버 오류 ({e.response.status_code}): {error_detail}")
        except httpx.TimeoutException:
            raise RuntimeError("Baro-AI 서버 응답 시간 초과. 고소장 생성에 시간이 오래 걸릴 수 있습니다.")
        except httpx.ConnectError:
            raise RuntimeError("Baro-AI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        except Exception as e:
            raise RuntimeError(f"예상치 못한 오류: {str(e)}")


# 싱글톤 인스턴스
ai_service = BaroAIService()
