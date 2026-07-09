from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class InteractionType(str, Enum):
    IN_PERSON = "in_person"
    PHONE_CALL = "phone_call"
    VIDEO_CALL = "video_call"
    EMAIL = "email"
    OTHER = "other"

class InteractionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    FLAGGED = "flagged"
    APPROVED = "approved"

class HCPBase(BaseModel):
    hcp_id: str
    name: str
    specialty: str
    location: str
    organization: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class InteractionCreate(BaseModel):
    hcp_id: str
    hcp_name: str
    interaction_type: InteractionType
    date: str  # ← CHANGE FROM datetime TO str
    duration_minutes: int
    notes: str
    products_discussed: Optional[List[str]] = []
    follow_up_required: bool = False
    follow_up_date: Optional[str] = None  # ← CHANGE FROM datetime TO str
    summary: Optional[str] = None
    entities_extracted: Optional[Dict[str, Any]] = None

class InteractionUpdate(BaseModel):
    notes: Optional[str] = None
    products_discussed: Optional[List[str]] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[datetime] = None
    summary: Optional[str] = None
    edit_reason: Optional[str] = None

class InteractionResponse(BaseModel):
    id: int
    hcp_id: str
    hcp_name: str
    interaction_type: InteractionType
    date: datetime  # ← Use datetime, not str
    duration_minutes: int
    notes: str
    products_discussed: Optional[List[str]] = []
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None  # ← Use datetime, not str
    summary: Optional[str] = None
    entities_extracted: Optional[Dict[str, Any]] = None
    status: InteractionStatus
    created_at: datetime
    updated_at: datetime
    created_by: str
    edit_history: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        from_attributes = True
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    mode: str = "log"
    interaction_id: Optional[int] = None

class ToolResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
