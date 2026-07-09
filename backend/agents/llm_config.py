from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm_gemma = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=1024
)

llm_llama = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=2048
)

SUMMARIZE_PROMPT = ChatPromptTemplate.from_template(
    """Summarize this HCP interaction notes concisely (max 3 sentences). 
    Focus on: key topics discussed, HCP's interest level, and any action items.
    
    Notes: {notes}
    
    Summary:"""
)

ENTITY_EXTRACTION_PROMPT = ChatPromptTemplate.from_template(
    """Extract structured entities from this HCP interaction. Return as JSON.
    
    Extract:
    - products_mentioned: list of product names
    - competitors_mentioned: list of competitor products/companies
    - key_objections: list of concerns raised
    - interest_areas: list of topics HCP showed interest in
    - action_items: list of follow-up actions needed
    
    Notes: {notes}
    
    JSON:"""
)

COMPLIANCE_CHECK_PROMPT = ChatPromptTemplate.from_template(
    """Review this HCP interaction for compliance issues. Flag if you detect:
    - Off-label product discussions
    - Unapproved claims or indications
    - Missing required safety information
    - Promotional content without proper context
    
    Return: {{flagged: bool, issues: [], risk_level: "low|medium|high", suggestions: []}}
    
    Notes: {notes}
    Products discussed: {products}
    
    Compliance Review:"""
)

FOLLOW_UP_SUGGESTION_PROMPT = ChatPromptTemplate.from_template(
    """Based on this HCP interaction, suggest optimal follow-up actions.
    
    Consider:
    - Best follow-up type (call, email, visit)
    - Recommended timing (days from interaction)
    - Specific products/materials to share
    - Key talking points for next interaction
    
    HCP: {hcp_name}
    Specialty: {specialty}
    Notes: {notes}
    Products discussed: {products}
    
    Suggestions (JSON format):"""
)

EDIT_SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """Improve and clarify this interaction summary. Make it professional and concise.
    
    Original notes: {notes}
    Current summary: {current_summary}
    
    Improved summary:"""
)
