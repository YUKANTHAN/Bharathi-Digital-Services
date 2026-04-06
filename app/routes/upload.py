from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import mongo
import os
import secrets
from datetime import datetime
from app.utils.validator import check_blur
from app.utils.ocr import extract_text

upload_bp = Blueprint("upload", __name__)

# Temporary directory for file processing
UPLOAD_DIR = os.path.join(os.getcwd(), "temp_uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@upload_bp.route("/file", methods=["POST"])
def upload_file():
    phone = request.form.get("phone")
    doc_type = request.form.get("doc_type")
    
    if not phone or not doc_type:
        return jsonify({"status": "error", "message": "Phone number and document type are required"}), 400
        
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request"}), 400
        
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        # Create a unique filename to avoid collisions
        unique_filename = f"{phone}_{secrets.token_hex(4)}_{filename}"
        filepath = os.path.join(UPLOAD_DIR, unique_filename)
        file.save(filepath)
        
        # Step 2: Quality Check (Blur Detection)
        blur_score = check_blur(filepath)
        
        # Define threshold for blurriness (Lower means blurrier)
        BLUR_THRESHOLD = 50.0
        
        if blur_score < BLUR_THRESHOLD:
            # Delete the file and reject upload if it's too blurry
            os.remove(filepath)
            return jsonify({
                "status": "error", 
                "message": "The uploaded image is too blurry. Please take a clearer photo and try again.",
                "blur_score": blur_score
            }), 422 # 422 Unprocessable Entity
            
        # Step 3: OCR Processing (Optional - we could run in a background thread if slow)
        extracted_content = extract_text(filepath)
        
        # Step 4: Metadata Recording
        doc_id = secrets.token_hex(8)
        new_doc = {
            "doc_id": doc_id,
            "doc_type": doc_type,
            "status": "pending_review", # Possible: pending_review, approved, rejected
            "file_url": filepath, # In production, replace with Google Drive ID/URL
            "submitted_at": datetime.utcnow(),
            "meta": {
                "blur_score": blur_score,
                "ocr_text": extracted_content # New OCR Data!
            },
            "franchise_id": "franchise_001", # For MVP, assign to a default franchise
            "feedback": ""
        }
        
        # Step 4: Database Update (Append to user's vault)
        # Find user by phone and add document to their vault
        mongo.db.users.update_one(
            {"phone": phone},
            {"$push": {"vault": new_doc}},
            upsert=True
        )
        
        return jsonify({
            "status": "success", 
            "message": "Document uploaded successfully and sent for franchise review.",
            "doc_id": doc_id
        }), 201

@upload_bp.route("/vault", methods=["GET"])
def get_user_vault():
    phone = request.args.get("phone")
    if not phone:
        return jsonify({"status": "error", "message": "Phone number is required"}), 400
        
    user = mongo.db.users.find_one({"phone": phone})
    if not user:
        return jsonify({"status": "success", "vault": []}), 200
        
    return jsonify({
        "status": "success",
        "vault": user.get("vault", [])
    }), 200
