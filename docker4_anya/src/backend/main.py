from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import time
from datetime import date
from typing import List

# Wait for DB to be ready
time.sleep(5)

# DB connection from ENV
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin1617!")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "membership_db")

# Function to create database if it doesn't exist
def create_db_if_not_exists():
    try:
        # Connect to the default 'postgres' database to create the new one
        base_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
        temp_engine = create_engine(base_url, isolation_level="AUTOCOMMIT")
        with temp_engine.connect() as conn:
            # Check if DB exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'"))
            if not result.fetchone():
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print(f"Database {DB_NAME} created.")
    except Exception as e:
        print(f"Note: Could not ensure database exists (this is normal if it exists or if running in K8s): {e}")

create_db_if_not_exists()

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    subscription_level = Column(String)
    expiry_date = Column(Date)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Membership Management API")

# Pydantic models
class MemberBase(BaseModel):
    full_name: str
    subscription_level: str
    expiry_date: date

class MemberCreate(MemberBase):
    pass

class MemberOut(MemberBase):
    id: int
    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/members", response_model=List[MemberOut])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = db.query(Member).offset(skip).limit(limit).all()
    return members

@app.post("/members", response_model=MemberOut)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "membership-backend"}
