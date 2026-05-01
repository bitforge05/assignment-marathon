from backend.database import SessionLocal, engine
from backend.models import Base, Memory
import datetime

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    # Supplier XYZ Memories
    memories = [
        {
            "entity_id": "Supplier_XYZ",
            "content": "Delivered 20% broken products in previous batch.",
            "category": "HISTORICAL",
            "importance": 0.9,
            "created_at": datetime.datetime.utcnow() - datetime.timedelta(days=120)
        },
        {
            "entity_id": "Supplier_XYZ",
            "content": "Road damage during monsoon causes 5-day delivery delays.",
            "category": "TEMPORAL",
            "importance": 0.8,
            "created_at": datetime.datetime.utcnow() - datetime.timedelta(days=365) # Old but seasonal
        },
        {
            "entity_id": "Supplier_XYZ",
            "content": "Always offers 2% discount for payments within 7 days.",
            "category": "EXPERIENCE",
            "importance": 0.7,
            "created_at": datetime.datetime.utcnow() - datetime.timedelta(days=200)
        },
        {
            "entity_id": "Supplier_XYZ",
            "content": "New contract signed with 10% volume discount.",
            "category": "IMMEDIATE",
            "importance": 1.0,
            "created_at": datetime.datetime.utcnow() - datetime.timedelta(days=2)
        }
    ]

    for m_data in memories:
        m = Memory(**m_data)
        db.add(m)
    
    db.commit()
    print("Database seeded successfully with Supplier_XYZ data!")

if __name__ == "__main__":
    seed()
