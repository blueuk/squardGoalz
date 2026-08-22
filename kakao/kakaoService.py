import os
import httpx
from typing import Dict, Any

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")

def get_kakao_auth_url() -> str:
    if not KAKAO_CLIENT_ID or not KAKAO_REDIRECT_URI:
        raise ValueError("카카오 설정값(ENV)이 누락되었습니다.")
    return f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"

async def get_kakao_user_info(code: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        # 1. 인가 코드로 토큰 발급
        token_response = await client.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_CLIENT_ID,
                "client_secret": KAKAO_CLIENT_SECRET,
                "redirect_uri": KAKAO_REDIRECT_URI,
                "code": code
            }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError(f"토큰 발급 실패: {token_data}")

        # 2. 발급받은 토큰으로 유저 정보 조회
        user_info_response = await client.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            }
        )
        user_info = user_info_response.json()
        
    kakao_id = user_info.get("id")
    if not kakao_id:
        raise ValueError(f"유저 정보 조회 실패: {user_info}")

    kakao_account = user_info.get("kakao_account", {})
    profile = kakao_account.get("profile", {})
    nickname = profile.get("nickname", "Unknown")

    return {
        "kakao_id": f"kakao_{kakao_id}",
        "nickname": nickname
    }

