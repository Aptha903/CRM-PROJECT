
# 🏥 AI-First CRM HCP Module - Log Interaction Screen

An AI-powered Customer Relationship Management system for logging and managing interactions with Healthcare Professionals (HCPs). Built with LangGraph, Groq LLM, FastAPI, and React.

---

## 🎯 Overview

This project implements an intelligent CRM module that allows field representatives to log interactions with HCPs through either:
- **Structured Form Interface** - Traditional form-based data entry
- **Conversational Chat Interface** - Natural language interaction powered by AI

The system uses a **LangGraph AI Agent** with 5 specialized tools to automate and enhance the interaction logging workflow.

---

## ✨ Features

### Core Functionality
- ✅ Log interactions with HCPs (form + chat)
- ✅ Edit existing interactions
- ✅ View all logged interactions
- ✅ Delete interactions
- ✅ Compliance checking
- ✅ Follow-up suggestions
- ✅ Interaction summaries

### AI-Powered Tools (LangGraph)
1. **Log Interaction Tool** - Captures interaction data with LLM-powered entity extraction and summarization
2. **Edit Interaction Tool** - Modifies logged data using natural language commands
3. **Compliance Check Tool** - Validates interactions against pharmaceutical compliance rules
4. **Suggest Follow-up Tool** - Recommends next actions based on interaction context
5. **Summarize Interaction Tool** - Generates concise summaries of HCP interactions

---

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Redux Toolkit** for state management
- **Tailwind CSS** for styling
- **Google Inter Font**
- **Lucide React** for icons

### Backend
- **Python 3.11+**
- **FastAPI** for REST API
- **SQLAlchemy** for ORM
- **SQLite/PostgreSQL** database
- **Pydantic** for data validation

### AI & LLM
- **LangGraph** for agent orchestration
- **Groq API** (gemma2-9b-it, llama-3.3-70b-versatile)
- **Natural Language Processing** for entity extraction

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key (get from https://console.groq.com/keys)

### Backend Setup

```bash
# Clone repository
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your Groq API key to .env
# GROQ_API_KEY=gsk_your_api_key_here

# Run database migrations
python -m sqlalchemy_utils

# Start backend server
uvicorn main:app --reload
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./crm.db
GROQ_API_KEY=gsk_your_groq_api_key_here
DEBUG=True
```

---

## 🚀 Usage

### Form Interface
1. Navigate to the "Form" tab
2. Select HCP from dropdown
3. Choose interaction type
4. Fill in details (products, notes, etc.)
5. Click "Log Interaction"

### Chat Interface
1. Navigate to the "Chat" tab
2. Type natural language commands:
   - "Log a meeting with Dr. Smith about Product A"
   - "Edit interaction with Dr. Smith to add discussed compliance guidelines"
   - "Check compliance for interaction 5"
   - "Suggest follow-up for Dr. Smith"
   - "Summarize my interactions with Dr. Smith"

### View Interactions
1. Navigate to "Interactions" tab
2. View all logged interactions
3. Filter by HCP, date, or product
4. Edit or delete interactions

---

## 📁 Project Structure
crm-hcp-module/
├── backend/
│ ├── main.py # FastAPI application
│ ├── models.py # SQLAlchemy database models
│ ├── schemas.py # Pydantic schemas
│ ├── database.py # Database connection
│ ├── groq_config.py # Groq LLM configuration
│ ├── tools.py # LangGraph tool definitions
│ ├── agent_graph.py # LangGraph agent graph
│ └── requirements.txt # Python dependencies
├── frontend/
│ ├── src/
│ │ ├── App.tsx # Main React component
│ │ ├── store.ts # Redux store
│ │ ├── features/ # Redux slices
│ │ └── components/ # UI components
│ ├── package.json
│ └── README.md
└── README.md # This file

text

---

## 🤖 LangGraph Agent Architecture

### Agent Graph Flow
User Input → LangGraph Agent → Tool Router → Tool Execution → LLM Processing → Response

text

### Tool Definitions

All 5 tools are defined in `backend/tools.py` and use Groq LLM for intelligent processing:

1. **log_interaction_tool** - Extracts entities, validates data, logs to database
2. **edit_interaction_tool** - Parses edit commands, updates records
3. **compliance_check_tool** - Checks against compliance rules, flags issues
4. **suggest_followup_tool** - Analyzes context, recommends actions
5. **summarize_interactions_tool** - Aggregates data, generates summary

---

## 🎥 Video Demo

A 10-15 minute walkthrough is available demonstrating:
- Frontend functionality (Form + Chat interfaces)
- All 5 LangGraph tools in action
- Code structure explanation
- Project overview

---

## 📊 API Endpoints

### Interactions
- `GET /interactions/` - List all interactions
- `POST /interactions/` - Create new interaction
- `GET /interactions/{id}` - Get interaction by ID
- `PUT /interactions/{id}` - Update interaction
- `DELETE /interactions/{id}` - Delete interaction

### HCPs
- `GET /hcps/` - List all HCPs
- `POST /hcps/` - Create new HCP
- `GET /hcps/{id}` - Get HCP by ID

### Products
- `GET /products/` - List all products
- `POST /products/` - Create new product

---

## 🔒 Security

- API key stored in environment variables
- Input validation with Pydantic
- CORS configured for frontend
- SQL injection protection via SQLAlchemy ORM

---

## 📝 Assignment Requirements Met

✅ **Frontend**: React with Redux state management  
✅ **Backend**: Python with FastAPI  
✅ **AI Agent Framework**: LangGraph  
✅ **LLM**: Groq (gemma2-9b-it, llama-3.3-70b-versatile)  
✅ **Database**: SQLite/PostgreSQL  
✅ **Font**: Google Inter  
✅ **5 LangGraph Tools**: All implemented with LLM integration  
✅ **Log Interaction Screen**: Form + Chat interfaces  
✅ **GitHub Repository**: Complete with documentation  

---

## 👨‍💻 Developer

Built as part of the AI-First CRM HCP Module assignment.

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- Groq for LLM API access
- LangGraph for agent orchestration framework
- FastAPI for backend framework
- React community for excellent frontend tools
