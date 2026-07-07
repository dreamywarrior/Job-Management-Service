from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.models.user import User
from app.schemas.user import UserCreate

password_hash = PasswordHash.recommended()


# =====================================================
# Get User By Email
# =====================================================

def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


# =====================================================
# Get User By ID
# =====================================================

def get_user_by_id(
    db: Session,
    user_id: int
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# =====================================================
# Create User
# =====================================================

def create_user(
    db: Session,
    user: UserCreate
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise ValueError(
            "An account with this email address already exists. Please log in or use a different email."
        )

    hashed_password = password_hash.hash(
        user.password
    )

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


# =====================================================
# Authenticate User
# =====================================================

def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not password_hash.verify(
        password,
        user.password_hash
    ):
        return None

    return user


# =====================================================
# Update Profile
# =====================================================

def update_profile(
    db: Session,
    user_id: int,
    full_name: str,
    email: str
):

    user = get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise ValueError("User account not found.")

    existing = (
        db.query(User)
        .filter(
            User.email == email,
            User.id != user_id
        )
        .first()
    )

    if existing:

        raise ValueError(
            "Email address is already registered."
        )

    user.full_name = full_name
    user.email = email

    db.commit()

    db.refresh(user)

    return user


# =====================================================
# Change Password
# =====================================================

def change_password(
    db: Session,
    user_id: int,
    current_password: str,
    new_password: str
):

    user = get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise ValueError("User account not found.")

    if not password_hash.verify(
        current_password,
        user.password_hash
    ):

        raise ValueError(
            "Current password is incorrect."
        )

    user.password_hash = password_hash.hash(
        new_password
    )

    db.commit()

    db.refresh(user)

    return user