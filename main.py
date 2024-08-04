from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas import UserCreate
from utils import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta
from models import User
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test"



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
access_token_expires = timedelta(minutes=30)

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    encrypted_password = hash_password(user.password)
    new_user = User(username=user.username, password=encrypted_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}











@app.post("/login")
def login_user(user: UserCreate, session: Session = Depends(get_db)):
    db_user = session.query(User).filter_by(username=user.username).first()
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}





