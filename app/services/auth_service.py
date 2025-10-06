from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.users_repo import UsersRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.models.user import User

class AuthService:
    def __init__(self, repo: UsersRepository | None = None):
        self.repo = repo or UsersRepository()

    def register(self, db: Session, username: str, email: str, password: str) -> User:
        if self.repo.get_by_username(db, username):
            raise HTTPException(status.HTTP_409_CONFLICT, "Username already in use")
        if self.repo.get_by_email(db, email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already in use")
        pwd_hash = hash_password(password)
        return self.repo.create(db, username=username, email=email, password_hash=pwd_hash)

    def login(self, db: Session, username_or_email: str, password: str) -> str:
        user = self.repo.get_by_username_or_email(db, username_or_email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        return create_access_token(sub=user.id, expires_minutes=settings.JWT_EXPIRES_MIN)
