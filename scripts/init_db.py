from sqlalchemy import create_engine, Column, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claimsiq.db")
Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"
    id = Column(String, primary_key=True)
    policy_id = Column(String)
    claim_date = Column(Date)
    claim_amount = Column(Float)
    approved_amount = Column(Float, nullable=True)
    status = Column(String)
    provider_id = Column(String)
    procedure_codes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Provider(Base):
    __tablename__ = "providers"
    id = Column(String, primary_key=True)
    npi = Column(String)
    name = Column(String)
    type = Column(String)
    specialty = Column(String)

def init_database():
    print(f"Initializing database at {DATABASE_URL}...")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
    
    with engine.connect() as conn:
        conn.execute(Base.metadata.tables['claims'].insert().values([]))
        conn.commit()
        print("Created indexes for claims table")

if __name__ == "__main__":
    init_database()
