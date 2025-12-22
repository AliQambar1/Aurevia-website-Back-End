from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.environment import db_URI
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Connect FastAPI with SQLAlchemy
engine = create_engine(
    db_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()