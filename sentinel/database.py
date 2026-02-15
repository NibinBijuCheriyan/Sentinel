from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./sentinel.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String) # Reddit, Twitter
    handle = Column(String, index=True)
    date = Column(DateTime)
    content = Column(Text)
    url = Column(String, unique=True)
    risk_score = Column(Float, default=0.0)
    flags = Column(String) # Comma-separated flags
    reviewed = Column(Boolean, default=False)
    reviewer_notes = Column(Text, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
