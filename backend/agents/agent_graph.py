from typing import TypedDict, Annotated, Sequence, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator
import re
from datetime import datetime


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    interaction_data: dict
    tool_outputs: list
    current_step: str


def extract_entities(state: AgentState) -> AgentState:
    messages = state["messages"]
    if not messages:
        return state
    
    last_message = messages[-1].content if messages else ""
    
    hcp_name = None
    duration = 15
    
    hcp_match = re.search(r'(Dr\.?\s+[A-Za-z]+(?:\s+[A-Za-z]+)?)', last_message, re.IGNORECASE)
    if hcp_match:
        hcp_name = hcp_match.group(1).strip()
    
    duration_match = re.search(r'(\d+)\s*(minutes?|mins?|min)', last_message, re.IGNORECASE)
    if duration_match:
        duration = int(duration_match.group(1))
    
    product_matches = re.findall(r'(Product\s+[A-Z])', last_message, re.IGNORECASE)
    
    state["interaction_data"] = {
        "hcp_name": hcp_name or "",
        "products_discussed": product_matches,
        "duration_minutes": duration,
        "notes": last_message,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "interaction_type": "in_person",
        "hcp_id": f"HCP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "follow_up_required": False,
    }
    
    if any(word in last_message.lower() for word in ["log", "create", "new", "add"]):
        state["current_step"] = "log_interaction"
    elif any(word in last_message.lower() for word in ["compliance", "check", "flag"]):
        state["current_step"] = "compliance_check"
    else:
        state["current_step"] = "default"
    
    return state


def execute_tool(state: AgentState) -> AgentState:
    from database.connection import SessionLocal
    db = SessionLocal()
    
    try:
        current_step = state["current_step"]
        data = state["interaction_data"]
        
        if current_step == "log_interaction":
            from models.database import Interaction, InteractionStatusEnum
            
            interaction = Interaction(
                hcp_id=data.get("hcp_id", "UNKNOWN"),
                hcp_name=data.get("hcp_name", "Unknown"),
                interaction_type=data.get("interaction_type", "in_person"),
                date=datetime.fromisoformat(data.get("date") + "T00:00:00"),
                duration_minutes=data.get("duration_minutes", 15),
                notes=data.get("notes", ""),
                products_discussed=data.get("products_discussed", []),
                follow_up_required=data.get("follow_up_required", False),
                status=InteractionStatusEnum.DRAFT,
            )
            
            db.add(interaction)
            db.commit()
            db.refresh(interaction)
            
            state["messages"].append(AIMessage(content=f"✅ Successfully logged interaction with {data.get('hcp_name')} (ID: {interaction.id})"))
        
        elif current_step == "compliance_check":
            has_products = len(data.get("products_discussed", [])) > 0
            has_notes = len(data.get("notes", "")) > 10
            state["messages"].append(AIMessage(content=f"Compliance: {'PASS ✅' if (has_products and has_notes) else 'REVIEW ⚠️'}"))
        
        else:
            state["messages"].append(AIMessage(content="I can help with: log, compliance"))
    
    finally:
        db.close()
    
    return state


def create_agent_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("extract_entities", extract_entities)
    workflow.add_node("execute_tool", execute_tool)
    workflow.set_entry_point("extract_entities")
    workflow.add_edge("extract_entities", "execute_tool")
    workflow.add_edge("execute_tool", END)
    return workflow.compile()


agent_graph = create_agent_graph()