from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database.connection import Base

class InteractionStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    FLAGGED = "flagged"
    APPROVED = "approved"

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(String(100), index=True)
    hcp_name = Column(String(200), nullable=False)
    interaction_type = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    notes = Column(Text, nullable=False)
    products_discussed = Column(JSON, default=list)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)
    summary = Column(Text, nullable=True)
    entities_extracted = Column(JSON, default=dict)
    status = Column(SQLEnum(InteractionStatusEnum), default=InteractionStatusEnum.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100), default="system")
    edit_history = Column(JSON, default=list)
