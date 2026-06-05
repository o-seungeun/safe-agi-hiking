#
# 아이나비 서버로 실제 HTTP 요청을 보내는 통신 모듈
# /OrdaAI/sookmyung/health 호출
# DTO-5 POST 전송 같은 실제 요청 함수 제공
# 어떻게 보낼지 담당
# inavi_client.py가 result.py의 하위 모듈처럼 쓰이는 구조
#

import httpx
from typing import Any, Dict

class InaviClient:
    """
    아이나비 서버 API 호출 전담 클라이언트.
    역할:
    - 아이나비 서버 health check 호출
    - 추후 DTO-5 AI 결과 전송 API 호출
    """

    def __init__(
        self,
        base_url: str = "http://3.37.223.154:1447",
        timeout: int = 5
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _make_url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.base_url}/{path}"

    async def get_health(self) -> Dict[str, Any]:
        """
        아이나비 서버 health check 호출.
        GET /OrdaAI/sookmyung/health
        """
        url = self._make_url("/OrdaAI/sookmyung/health")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url,
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            return response.json()

    async def post_ai_result(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        DTO-5 AI 결과를 아이나비 서버로 전송.
        TODO: 아이나비 DTO-5 수신 API 경로 확정 후 수정
        """
        url = self._make_url("/OrdaAI/sookmyung/result")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            return response.json()

if __name__ == "__main__":
    import asyncio

    async def main():
        try:
            client = InaviClient()
            response = await client.get_health()

            print("HTTP Status: 200")
            print("Response Body:", response)

        except Exception as e:
            print("Request failed:", e)

    asyncio.run(main())