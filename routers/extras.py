from fastapi import APIRouter, Header, status, Response

from schemas.property import ResponseWithoutData

router = APIRouter()

@router.get(
    "/req-header",
    status_code = status.HTTP_200_OK
)
def get_request_header(user_name: str | None = Header(default=None)):
    return {
        "status": True,
        "user_name": user_name
    }


@router.get(
    "/set-cookie",
    status_code=status.HTTP_200_OK
)
def set_cookie(response: Response):
    response.headers["X-API-Version"] = "1.0"

    response.set_cookie(
        key="session_token",
        value="xyz123",
        httponly=True,
        samesite="lax"
    )

    return {
        "status": True,
        "message": "Header and cookie added successfully"
    }