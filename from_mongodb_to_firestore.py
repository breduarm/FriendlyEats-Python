import firebase_admin
from firebase_admin import credentials, firestore
from pymongo import MongoClient
import certifi

# 🔹 MongoDB Connection (Replace with your credentials)
MONGO_URI = "<your_connection_secrets>"
MONGO_DB = "<database_name>"
MONGO_COLLECTION = "<collection_name>"

# 🔹 Firestore Setup (Replace with your Firebase credentials JSON file)
FIREBASE_CREDENTIALS = "<your_connection_secrets>"

# Initialize Firestore
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

# Connect to MongoDB
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db_mongo = client[MONGO_DB]
collection_mongo = db_mongo[MONGO_COLLECTION]

# Function to transform MongoDB data into Firestore format
def transform_document(mongo_doc):
    return {
        "name": mongo_doc.get("name", ""),
        "category": mongo_doc.get("category", ""),
        "city": mongo_doc.get("city", ""),
        "avgRating": mongo_doc.get("avgRating", 0),
        "numRatings": mongo_doc.get("numRatings", 0),
        "photo": mongo_doc.get("photo", ""),
        "price": mongo_doc.get("price", 0),
    }

# Fetch and migrate data
def migrate_data():
    documents = collection_mongo.find()
    for doc in documents:
        doc_id = str(doc["_id"])  # Use MongoDB _id as Firestore document ID
        transformed_data = transform_document(doc)
        db_firestore.collection("restaurants").document(doc_id).set(transformed_data)
        print(f"✅ Migrated {doc_id} to Firestore")

if __name__ == "__main__":
    migrate_data()
    print("🚀 Migration completed!")