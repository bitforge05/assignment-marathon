from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from .database import Base
import datetime

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(String, index=True)  # e.g., Supplier ID or Customer ID
    content = Column(String)
    category = Column(String)  # IMMEDIATE, HISTORICAL, TEMPORAL, EXPERIENCE
    importance = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_used = Column(DateTime, default=datetime.datetime.utcnow)
    metadata_json = Column(JSON, nullable=True) # JSON store for seasonal info etc.
