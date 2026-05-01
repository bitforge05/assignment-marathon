from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Memory
from .memory_engine import MemoryEngine
from pydantic import BaseModel
from typing import Optional, List, Dict
import datetime

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Business Memory Engine")

# Pydantic Schemas
class MemoryCreate(BaseModel):
    entity_id: str
    content: str
    category: str  # IMMEDIATE, HISTORICAL, TEMPORAL, EXPERIENCE
    importance: float
    metadata: Optional[Dict] = None

class InvoiceProcess(BaseModel):
    supplier_id: str
    amount: float
    items: List[str]

@app.get("/")
def read_root():
    return {"message": "AI Business Memory Engine is running"}

@app.post("/memories")
def create_memory(memory: MemoryCreate, db: Session = Depends(get_db)):
    return MemoryEngine.add_memory(
        db, 
        memory.entity_id, 
        memory.content, 
        memory.category, 
        memory.importance, 
        memory.metadata
    )

@app.get("/context/{entity_id}")
def get_context(entity_id: str, db: Session = Depends(get_db)):
    context = MemoryEngine.get_ranked_context(db, entity_id)
    if not context:
        return {"entity_id": entity_id, "context": [], "message": "No previous memory found."}
    return {"entity_id": entity_id, "context": context}

@app.post("/process-invoice")
def process_invoice(invoice: InvoiceProcess, db: Session = Depends(get_db)):
    # 1. Fetch relevant memories for this supplier
    memories = MemoryEngine.get_ranked_context(db, invoice.supplier_id)
    
    # 2. Logic to decide recommendation
    warnings = []
    recommendation = "Approve"
    
    # Simple rule-based expert logic using memories
    for m in memories:
        if "broken" in m["content"].lower() or "damage" in m["content"].lower():
            warnings.append(f"CRITICAL: {m['content']} (Source: {m['category']})")
            recommendation = "Hold for Inspection"
        
        if m["category"] == "TEMPORAL" and "monsoon" in m["content"].lower():
            # Check if current month is monsoon (Jun-Sep)
            current_month = datetime.datetime.now().month
            if 6 <= current_month <= 9:
                warnings.append(f"SEASONAL ALERT: {m['content']}")
                recommendation = "Hold for Quality Check"

    return {
        "invoice_details": invoice,
        "recommendation": recommendation,
        "warnings": warnings,
        "relevant_context": memories
    }
