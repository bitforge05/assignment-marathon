import datetime
from sqlalchemy.orm import Session
from .models import Memory
import math

class MemoryEngine:
    # Weights for different memory types
    CATEGORY_WEIGHTS = {
        "IMMEDIATE": 1.0,
        "EXPERIENCE": 0.9,
        "TEMPORAL": 0.8,
        "HISTORICAL": 0.7
    }

    @staticmethod
    def calculate_score(memory: Memory):
        # Time Decay Calculation
        now = datetime.datetime.utcnow()
        age_in_days = (now - memory.created_at).days
        
        # Logarithmic decay to ensure old but important memories don't vanish immediately
        time_decay = 1 / (1 + math.log1p(age_in_days))
        
        # Weight based on category
        cat_weight = MemoryEngine.CATEGORY_WEIGHTS.get(memory.category, 0.5)
        
        # Final Score
        return (memory.importance * cat_weight * time_decay)

    @staticmethod
    def get_ranked_context(db: Session, entity_id: str, limit: int = 5):
        memories = db.query(Memory).filter(Memory.entity_id == entity_id).all()
        
        scored_memories = []
        for m in memories:
            score = MemoryEngine.calculate_score(m)
            # Update last used
            m.last_used = datetime.datetime.utcnow()
            scored_memories.append({
                "id": m.id,
                "content": m.content,
                "category": m.category,
                "score": round(score, 4),
                "importance": m.importance,
                "created_at": m.created_at,
                "metadata": m.metadata_json
            })
        
        # Sort by score descending
        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        
        # Stale Memory Handling: Filter out very low scores (optional)
        # return [m for m in scored_memories if m["score"] > 0.1][:limit]
        
        return scored_memories[:limit]

    @staticmethod
    def add_memory(db: Session, entity_id: str, content: str, category: str, importance: float, metadata: dict = None):
        new_memory = Memory(
            entity_id=entity_id,
            content=content,
            category=category,
            importance=importance,
            metadata_json=metadata
        )
        db.add(new_memory)
        db.commit()
        db.refresh(new_memory)
        return new_memory
