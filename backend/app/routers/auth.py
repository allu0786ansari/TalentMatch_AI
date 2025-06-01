from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserLogin, PasswordResetRequest, PasswordReset
from app.utils.auth_utils import create_access_token, verify_password, hash_password
from app.utils.email import send_password_reset_email, send_welcome_email
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_password, name=user.name)
    db.add(new_user)
    db.commit()
    # Await the async function
    await send_welcome_email(new_user)  # Fixed: Added await
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = create_access_token({"sub": db_user.email}, expires_in=3600)
    # Await the async function
    await send_password_reset_email(db_user, reset_token)  # Fixed: Added await
    return {"message": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    email = data.token_data.get("sub")
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password reset successfully"}