from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.schemas.auth import LoginRequest, Token

router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Admin login endpoint.
    Returns JWT token for authentication.
    """
    # Simple admin authentication (in production, use proper user management)
    if (
        login_data.username == settings.ADMIN_USERNAME
        and login_data.password == settings.ADMIN_PASSWORD
    ):
        access_token = create_access_token(data={"sub": login_data.username})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to verify JWT token and get current user.
    Use this for protected admin endpoints.
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return username


@router.get("/verify")
async def verify(current_user: str = Depends(get_current_user)):
    """
    Verify if the current token is valid.
    """
    return {"username": current_user, "valid": True}
