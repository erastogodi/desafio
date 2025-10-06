from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

class UsersRepository:
    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.execute(select(User).where(User.username == username)).scalar_one_or_none()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_by_username_or_email(self, db: Session, value: str) -> User | None:
        stmt = select(User).where((User.username == value) | (User.email == value))
        return db.execute(stmt).scalar_one_or_none()

    def create(self, db: Session, username: str, email: str, password_hash: str) -> User:
        u = User(username=username, email=email, password_hash=password_hash)
        db.add(u)
        db.commit()
        db.refresh(u)
        return u
