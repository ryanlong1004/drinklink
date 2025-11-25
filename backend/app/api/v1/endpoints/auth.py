import hmac

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.schemas.auth import LoginRequest, RefreshRequest, Token

router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Admin login endpoint.
    Returns JWT access and refresh tokens for authentication.
    """
    # Use constant-time comparison to prevent timing attacks
    username_match = hmac.compare_digest(
        login_data.username.encode(), settings.ADMIN_USERNAME.encode()
    )
    password_match = hmac.compare_digest(
        login_data.password.encode(), settings.ADMIN_PASSWORD.encode()
    )

    if username_match and password_match:
        access_token = create_access_token(data={"sub": login_data.username})
        refresh_token = create_refresh_token(data={"sub": login_data.username})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
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


@router.post("/refresh", response_model=Token)
async def refresh(refresh_data: RefreshRequest):
    """
    Refresh access token using refresh token.
    Returns new access and refresh tokens.
    """
    payload = verify_token(refresh_data.refresh_token, token_type="refresh")

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new tokens
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/verify")
async def verify(current_user: str = Depends(get_current_user)):
    """
    Verify if the current token is valid.
    """
    return {"username": current_user, "valid": True}
