from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.auth_service import AuthService
from app.core.security import require_jwt
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, MeResponse
from app.repositories.users_repo import UsersRepository

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=MeResponse, status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    svc = AuthService(UsersRepository())
    u = svc.register(db, req.username, req.email, req.password)
    return MeResponse(id=u.id, username=u.username, email=u.email)

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    svc = AuthService(UsersRepository())
    token = svc.login(db, req.username_or_email, req.password)
    from app.core.config import settings
    return TokenResponse(access_token=token, expires_in=settings.JWT_EXPIRES_MIN * 60)

@router.get("/me", response_model=MeResponse)
def me(user_id: str = Depends(require_jwt), db: Session = Depends(get_db)):
    repo = UsersRepository()
    u = repo.get_by_username_or_email(db, user_id)  # o sub é o id; reaproveitando método
    if not u:
        # fallback: buscar por id corretamente
        from sqlalchemy import select
        from app.models.user import User
        u = db.get(User, user_id)
    return MeResponse(id=u.id, username=u.username, email=u.email)
