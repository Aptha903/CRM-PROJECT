from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models.schemas import InteractionCreate, InteractionUpdate, InteractionResponse, ChatRequest, ToolResponse
from models.database import Interaction
from database.connection import get_db
from agents.agent_graph import agent_graph
from langchain_core.messages import HumanMessage
from datetime import datetime

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])

@router.post("/chat", response_model=ToolResponse)
def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat interface for logging interactions"""
    from database.connection import SessionLocal
    from models.database import Interaction, InteractionStatusEnum
    import re
    
    db_session = SessionLocal()
    
    try:
        # Get last message
        messages = request.messages
        if not messages:
            return ToolResponse(success=True, message="No message provided", data={})
        
        last_message = messages[-1].content
        
        # Simple extraction
        hcp_name = None
        product_matches = []
        
        hcp_match = re.search(r'(Dr\.?\s+[A-Za-z]+(?:\s+[A-Za-z]+)?)', last_message, re.IGNORECASE)
        if hcp_match:
            hcp_name = hcp_match.group(1).strip()
        
        product_matches = re.findall(r'(Product\s+[A-Z])', last_message, re.IGNORECASE)
        
        # Check intent
        if any(word in last_message.lower() for word in ["log", "create", "new", "add"]):
            if hcp_name:
                interaction = Interaction(
                    hcp_id=f"HCP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    hcp_name=hcp_name,
                    interaction_type="in_person",
                    date=datetime.now(),
                    duration_minutes=15,
                    notes=last_message,
                    products_discussed=product_matches,
                    follow_up_required=False,
                    status=InteractionStatusEnum.DRAFT,
                )
                
                db_session.add(interaction)
                db_session.commit()
                db_session.refresh(interaction)
                
                return ToolResponse(
                    success=True,
                    message=f"✅ Successfully logged interaction with {hcp_name}",
                    data={"interaction_id": interaction.id}
                )
            else:
                return ToolResponse(
                    success=False,
                    message="I couldn't find an HCP name. Please mention 'Dr. [Name]'",
                    data={}
                )
        
        elif any(word in last_message.lower() for word in ["compliance", "check", "flag", "review"]):
            # Extract interaction ID
            id_match = re.search(r'interaction\s+(\d+)', last_message, re.IGNORECASE)
            if id_match:
                interaction_id = int(id_match.group(1))
                interaction = db_session.query(Interaction).filter(Interaction.id == interaction_id).first()
                if interaction:
                    has_products = len(interaction.products_discussed or []) > 0
                    has_notes = len(interaction.notes or "") > 10
                    duration_ok = interaction.duration_minutes >= 5
                    
                    status = "PASS ✅" if (has_products and has_notes and duration_ok) else "REVIEW ⚠️"
                    recommendations = []
                    if not has_products:
                        recommendations.append("- Add products discussed")
                    if not has_notes:
                        recommendations.append("- Add more detailed notes")
                    if not duration_ok:
                        recommendations.append("- Duration seems too short")
                    
                    return ToolResponse(
                        success=True,
                        message=f"Compliance for {interaction.hcp_name} (#{interaction_id}): {status}\n\n{'✅ All checks passed!' if status == 'PASS ✅' else 'Recommendations:\\n' + '\\n'.join(recommendations)}",
                        data={
                            "interaction_id": interaction_id,
                            "status": status,
                            "has_products": has_products,
                            "has_notes": has_notes,
                            "duration_ok": duration_ok,
                        }
                    )
                else:
                    return ToolResponse(success=False, message=f"Interaction #{interaction_id} not found", data={})
            
            return ToolResponse(success=True, message="Usage: 'Check compliance for interaction [ID]'\nExample: 'Check compliance for interaction 7'", data={})
        
        else:
            return ToolResponse(
                success=True,
                message="I can help with: log, compliance. Try: 'Log interaction with Dr. Smith about Product A'",
                data={}
            )
    
    except Exception as e:
        db_session.rollback()
        return ToolResponse(success=False, message=f"Error: {str(e)}", data={})
    finally:
        db_session.close()
@router.post("/compliance/{interaction_id}")
def check_compliance(interaction_id: int, db: Session = Depends(get_db)):
    """Run compliance check"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    # Simple mock compliance check
    has_products = interaction.products_discussed and len(interaction.products_discussed) > 0
    has_notes = interaction.notes and len(interaction.notes) > 10
    
    compliance_result = {
        "interaction_id": interaction_id,
        "hcp_name": interaction.hcp_name,
        "status": "PASS" if (has_products and has_notes) else "REVIEW",
        "checks": {
            "has_products": has_products,
            "has_notes": has_notes,
            "duration_ok": interaction.duration_minutes >= 5,
        },
        "recommendations": []
    }
    
    if not has_products:
        compliance_result["recommendations"].append("Add products discussed")
    if not has_notes:
        compliance_result["recommendations"].append("Add more detailed notes")
    if interaction.duration_minutes < 5:
        compliance_result["recommendations"].append("Interaction duration seems too short")
    
    return compliance_result
