import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firestore
cred = credentials.Certificate("<your_credential_secrets>")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Fetch the "restaurants" collection
restaurants_ref = db.collection("<collection_name>")
docs = restaurants_ref.stream()

# Convert to JSON
restaurants = []
for doc in docs:
    data = doc.to_dict()
    data["_id"] = doc.id  # Optional: Set Firestore ID as _id in MongoDB
    restaurants.append(data)

# Save to JSON
with open("restaurants.json", "w") as f:
    json.dump(restaurants, f, indent=4)

print("Data exported successfully!")