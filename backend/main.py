from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from typing import List, Annotated

#To run: 
# .\venv\Scripts\Activate
# uvicorn main:app --reload

# Database URL
DATABASE_URL = "mysql+pymysql://root:mateo123@localhost:3306/AppPresentation"

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model Definition
class HeartRate(Base):
    __tablename__ = "heart_rate"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    heart_rate = Column(Integer, nullable=False)
    recorded_at = Column(TIMESTAMP, server_default=func.now())

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI app initialization
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for Request and Response
class HeartRateBase(BaseModel):
    name: str
    heart_rate: int

class HeartRateCreate(HeartRateBase):
    pass

class HeartRateOut(HeartRateBase):
    id: int
    recorded_at: str

    class Config:
        orm_mode = True

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Default Route
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Create a new heart rate record
@app.post("/heartrates/", response_model=HeartRateOut)
def create_heart_rate(heart_rate: HeartRateCreate, db: db_dependency):
    db_heart_rate = HeartRate(name=heart_rate.name, heart_rate=heart_rate.heart_rate)
    db.add(db_heart_rate)
    db.commit()
    db.refresh(db_heart_rate)
    return db_heart_rate

# Get all heart rate records
@app.get("/heartrates/", response_model=List[HeartRateOut])
def read_heart_rates(db: db_dependency, skip: int = 0, limit: int = 10):
    return db.query(HeartRate).offset(skip).limit(limit).all()

# Get heart rate records by name
@app.get("/heartrates/{name}", response_model=List[HeartRateOut])
def read_heart_rates_by_name(name: str, db: db_dependency):
    heart_rates = db.query(HeartRate).filter(HeartRate.name == name).all()
    if not heart_rates:
        raise HTTPException(status_code=404, detail="No heart rate data found for this name")
    return heart_rates


#Retrieve heart rate from polar h10

import asyncio
from bleak import BleakClient

# Polar H10 mac address
mac_address = "EB:D9:AB:99:89:8F"

# UUID for the Heart Rate Measurement characteristic
heart_rate_char_uuid = "00002a37-0000-1000-8000-00805f9b34fb"

async def run():
    async with BleakClient(mac_address) as client:
        print(f"Connected: {client.is_connected}")
        
        # Function to handle heart rate notifications
        def handle_heart_rate(sender, data):
            # Parse heart rate data according to the Bluetooth GATT specification
            heart_rate = data[1]
            print(f"Heart Rate: {heart_rate} BPM")

        # Start notifications on the heart rate characteristic
        await client.start_notify(heart_rate_char_uuid, handle_heart_rate)
        
        print("Receiving heart rate data... Press Ctrl+C to exit")
        
        # Keep the connection open to receive data
        while True:
            await asyncio.sleep(1)

# Run the asyncio event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(run())