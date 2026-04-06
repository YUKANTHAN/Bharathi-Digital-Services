from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://user:password@cluster0.abcde.mongodb.net/eseva_portal?retryWrites=true&w=majority")

def setup_db():
    client = MongoClient(MONGO_URI)
    db = client.get_database("eseva_portal")
    
    # Create a test franchise operator
    # Note: Using phone number '+919999999999' for the operator
    operator = {
        "phone": "+919999999999",
        "role": "franchise",
        "name": "Arun (Franchise Operator)",
        "franchise_id": "franchise_001",
        "location": "Chennai Main Station"
    }
    
    # Update or insert
    db.users.update_one(
        {"phone": operator["phone"]},
        {"$set": operator},
        upsert=True
    )
    
    print("Database setup complete with test operator: +919999999999")

if __name__ == "__main__":
    setup_db()
