from langchain_core.tools import tool
from typing import Dict, Any, Optional
from datetime import datetime
import json
from .llm_config import (
    llm_gemma, llm_llama,
    SUMMARIZE_PROMPT, ENTITY_EXTRACTION_PROMPT,
    COMPLIANCE_CHECK_PROMPT, FOLLOW_UP_SUGGESTION_PROMPT,
    EDIT_SUMMARY_PROMPT
)

@tool
def log_interaction(
    hcp_id: str,
    hcp_name: str,
    interaction_type: str,
    date: str,
    duration_minutes: int,
    notes: str,
    products_discussed: Optional[list] = None,
    follow_up_required: bool = False,
    follow_up_date: Optional[str] = None,
    db_session=None
) -> Dict[str, Any]:
    """Log a new HCP interaction. Uses LLM for summarization and entity extraction."""
    from models.database import Interaction, InteractionStatusEnum
    
    summary_result = SUMMARIZE_PROMPT.format_prompt(notes=notes)
    summary = llm_gemma.invoke(summary_result.to_messages()).content.strip()
    
    entity_result = ENTITY_EXTRACTION_PROMPT.format_prompt(notes=notes)
    entities_json = llm_gemma.invoke(entity_result.to_messages()).content.strip()
    
    try:
        entities = json.loads(entities_json) if entities_json.startswith('{') else {}
    except:
        entities = {}
    
    interaction = Interaction(
        hcp_id=hcp_id,
        hcp_name=hcp_name,
        interaction_type=interaction_type,
        date=datetime.fromisoformat(date.replace('Z', '+00:00')),
        duration_minutes=duration_minutes,
        notes=notes,
        products_discussed=products_discussed or [],
        follow_up_required=follow_up_required,
        follow_up_date=datetime.fromisoformat(follow_up_date.replace('Z', '+00:00')) if follow_up_date else None,
        summary=summary,
        entities_extracted=entities,
        status=InteractionStatusEnum.DRAFT
    )
    
    db_session.add(interaction)
    db_session.commit()
    db_session.refresh(interaction)
    
    return {
        "success": True,
        "message": "Interaction logged successfully",
        "data": {
            "interaction_id": interaction.id,
            "summary": summary,
            "entities": entities,
            "status": "draft"
        }
    }

@tool
def edit_interaction(
    interaction_id: int,
    notes: Optional[str] = None,
    products_discussed: Optional[list] = None,
    follow_up_required: Optional[bool] = None,
    follow_up_date: Optional[str] = None,
    edit_reason: Optional[str] = None,
    db_session=None
) -> Dict[str, Any]:
    """Edit an existing HCP interaction. Maintains audit trail."""
    from models.database import Interaction
    
    interaction = db_session.query(Interaction).filter(Interaction.id == interaction_id).first()
    
    if not interaction:
        return {"success": False, "message": "Interaction not found", "data": None}
    
    edit_record = {
        "edited_at": datetime.utcnow().isoformat(),
        "edit_reason": edit_reason or "General update",
        "changes": {}
    }
    
    if notes:
        edit_record["changes"]["notes"] = {"old": interaction.notes, "new": notes}
        interaction.notes = notes
        summary_result = EDIT_SUMMARY_PROMPT.format_prompt(notes=notes, current_summary=interaction.summary or "")
        new_summary = llm_gemma.invoke(summary_result.to_messages()).content.strip()
        edit_record["changes"]["summary"] = {"old": interaction.summary, "new": new_summary}
        interaction.summary = new_summary
    
    if products_discussed is not None:
        edit_record["changes"]["products_discussed"] = {"old": interaction.products_discussed, "new": products_discussed}
        interaction.products_discussed = products_discussed
    
    if follow_up_required is not None:
        edit_record["changes"]["follow_up_required"] = {"old": interaction.follow_up_required, "new": follow_up_required}
        interaction.follow_up_required = follow_up_required
    
    if follow_up_date:
        edit_record["changes"]["follow_up_date"] = {"old": interaction.follow_up_date.isoformat() if interaction.follow_up_date else None, "new": follow_up_date}
        interaction.follow_up_date = datetime.fromisoformat(follow_up_date.replace('Z', '+00:00'))
    
    if interaction.edit_history is None:
        interaction.edit_history = []
    interaction.edit_history.append(edit_record)
    interaction.updated_at = datetime.utcnow()
    
    db_session.commit()
    
    return {
        "success": True,
        "message": "Interaction updated successfully",
        "data": {"interaction_id": interaction_id, "edit_record": edit_record, "new_summary": interaction.summary}
    }

@tool
def suggest_follow_up(
    hcp_name: str,
    specialty: str,
    notes: str,
    products_discussed: list,
    db_session=None
) -> Dict[str, Any]:
    """Suggest optimal follow-up actions based on interaction context."""
    follow_up_result = FOLLOW_UP_SUGGESTION_PROMPT.format_prompt(
        hcp_name=hcp_name, specialty=specialty, notes=notes, products=products_discussed
    )
    suggestions_json = llm_llama.invoke(follow_up_result.to_messages()).content.strip()
    
    try:
        suggestions = json.loads(suggestions_json) if suggestions_json.startswith('{') else {}
    except:
        suggestions = {"follow_up_type": "call", "timing_days": 7, "talking_points": [], "materials_to_share": []}
    
    return {"success": True, "message": "Follow-up suggestions generated", "data": suggestions}

@tool
def compliance_check(
    notes: str,
    products_discussed: list,
    db_session=None
) -> Dict[str, Any]:
    """Check interaction content for compliance issues."""
    compliance_result = COMPLIANCE_CHECK_PROMPT.format_prompt(notes=notes, products=products_discussed)
    compliance_json = llm_llama.invoke(compliance_result.to_messages()).content.strip()
    
    try:
        compliance = json.loads(compliance_json) if compliance_json.startswith('{') else {}
    except:
        compliance = {"flagged": False, "issues": [], "risk_level": "low", "suggestions": []}
    
    return {"success": True, "message": "Compliance check completed", "data": compliance}

@tool
def summarize_interaction(
    notes: str,
    interaction_id: Optional[int] = None,
    db_session=None
) -> Dict[str, Any]:
    """Generate concise summary from detailed interaction notes."""
    summary_result = SUMMARIZE_PROMPT.format_prompt(notes=notes)
    summary = llm_gemma.invoke(summary_result.to_messages()).content.strip()
    
    return {"success": True, "message": "Summary generated", "data": {"summary": summary, "interaction_id": interaction_id}}