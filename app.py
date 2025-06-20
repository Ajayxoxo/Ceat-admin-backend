from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)
CORS(app)  # Allow requests from browser (CORS enabled)

# MongoDB Setup
MONGO_URI = "mongodb+srv://weat:y1Gz3lap4IkOPdC9@backenddb.enp5odq.mongodb.net/kalimark?retryWrites=true&w=majority&appName=BackendDB"
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db['Mumbai']  # You can use dynamic selection if needed

@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()

    city = data.get('city')
    doc_id = data.get('docId')
    update_fields = data.get('update')

    if not all([city, doc_id, update_fields]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": update_fields}
        )
        if result.matched_count == 0:
            return jsonify({"error": "No document found with that ID"}), 404
        return jsonify({"message": f"{city} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
