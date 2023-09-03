
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://uprevol:live12345@horizonhold.ctcgakaymkmx.ap-south-1.rds.amazonaws.com:5432/horizonhold"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()