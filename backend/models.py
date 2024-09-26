from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HeartRate(Base):
    __tablename__ = "heart_rate"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    heart_rate = Column(Integer, nullable=False)
    recorded_at = Column(TIMESTAMP, server_default=func.now())
