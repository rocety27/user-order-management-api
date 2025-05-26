# app/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator  # ✅ required for generator type annotation

DATABASE_URL = "postgresql://postgres:password@localhost/db_name"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:  # ✅ fixed type hint
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
