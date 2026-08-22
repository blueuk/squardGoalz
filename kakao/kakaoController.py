from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from kakao import kakaoService

router = APIRouter(prefix="/kakao", tags=["Kakao"])

@router.get("/login")
async def kakao_login():
    """카카오 로그인 창으로 이동"""
    try:
        url = kakaoService.get_kakao_auth_url()
        return RedirectResponse(url=url)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/callback")
async def kakao_callback(code: str, request: Request):
    """카카오 로그인 후 콜백 - ID와 닉네임을 세션에 저장"""
    try:
        user_data = await kakaoService.get_kakao_user_info(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 세션(Session)에 정보 저장
    request.session["userid"] = user_data["kakao_id"]
    request.session["nickname"] = user_data["nickname"]
    
    # 세션 저장 후 통합 로그인 판별 및 회원가입 화면으로 리다이렉트
    return RedirectResponse(url="/login/kakao/process")

@router.get("/session")
async def get_my_session(request: Request):
    """현재 세션에 저장된 유저 정보 확인용 테스트 엔드포인트"""
    userid = request.session.get("userid")
    nickname = request.session.get("nickname")
    if not userid:
        raise HTTPException(status_code=401, detail="현재 로그인된 세션이 없습니다.")
    
    return {"userid": userid, "nickname": nickname}

@router.post("/logout")
async def kakao_logout(request: Request):
    """세션 초기화(로그아웃)"""
    request.session.clear()
    return {"message": "로그아웃 되었습니다."}

