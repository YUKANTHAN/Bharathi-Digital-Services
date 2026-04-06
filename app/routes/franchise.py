from flask import Blueprint, request, jsonify
from app import mongo
import os
from datetime import datetime

franchise_bp = Blueprint("franchise", __name__)

@franchise_bp.route("/dashboard", methods=["GET"])
def get_franchise_dashboard():
    franchise_id = request.args.get("franchise_id", "franchise_001")
    
    # In MongoDB, we find all users with a document assigned to this franchise and status is pending_review
    # The aggregate pipeline might be more efficient for many users.
    users = mongo.db.users.find({
        "vault.franchise_id": franchise_id,
        "vault.status": "pending_review"
    })
    
    pending_docs = []
    for user in users:
        for doc in user.get("vault", []):
            if doc.get("franchise_id") == franchise_id and doc.get("status") == "pending_review":
                # For display in dashboard, include user identification as well
                doc["user_phone"] = user["phone"]
                doc["user_name"] = user.get("name", "Unknown Citizen")
                pending_docs.append(doc)
    
    return jsonify({
        "status": "success",
        "pending_docs": pending_docs
    }), 200

@franchise_bp.route("/action", methods=["POST"])
def franchise_action():
    data = request.json
    doc_id = data.get("doc_id")
    action = data.get("action") # approved or rejected
    feedback = data.get("feedback", "")
    
    if not doc_id or action not in ["approved", "rejected"]:
        return jsonify({"status": "error", "message": "Document ID and valid action (approved/rejected) are required"}), 400
        
    # Update the document status within the user's vault
    result = mongo.db.users.update_one(
        {"vault.doc_id": doc_id},
        {
            "$set": {
                "vault.$.status": action,
                "vault.$.feedback": feedback,
                "vault.$.action_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        return jsonify({"status": "error", "message": "Document not found or status not changed"}), 404
        
    return jsonify({
        "status": "success",
        "message": f"Document {action} successfully",
        "doc_id": doc_id
    }), 200
