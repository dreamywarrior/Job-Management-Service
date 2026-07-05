from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.models.user import User
from app.schemas.user import UserCreate

password_hash = PasswordHash.recommended()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):

    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = password_hash.hash(user.password)

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not password_hash.verify(password, user.password_hash):
        return None

    return user