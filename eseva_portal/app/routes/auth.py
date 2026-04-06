from flask import Blueprint, request, jsonify
from app import mongo
import os
import secrets
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

# Dummy database for OTP tracking in memory
# In production, use MongoDB for this as well or a dedicated OTP table
# with an expiration index.
otps = {}

@auth_bp.route("/request-otp", methods=["POST"])
def request_otp():
    data = request.json
    phone = data.get("phone")
    
    if not phone:
        return jsonify({"status": "error", "message": "Phone number is required"}), 400
        
    # Generate a random 6-digit OTP
    otp = str(secrets.randbelow(1_000_000)).zfill(6)
    
    # In production, send OTP via Twilio or Firebase
    # For now, simulate sending OTP by returning it in the response (Dev mode only!)
    otps[phone] = {
        "otp": "123456",  # Fixing it to 123456 for testing purposes
        "timestamp": datetime.utcnow()
    }
    
    return jsonify({
        "status": "success", 
        "message": f"OTP sent to {phone}",
        "dev_otp": "123456" # Remove in production
    }), 200

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    phone = data.get("phone")
    otp = data.get("otp")
    role = data.get("role", "citizen") # citizen or franchise
    
    if not phone or not otp:
        return jsonify({"status": "error", "message": "Phone and OTP are required"}), 400
        
    if phone in otps and otps[phone]["otp"] == otp:
        # OTP verified, create session or JWT
        user = mongo.db.users.find_one({"phone": phone})
        
        if not user:
            # First time user, register as citizen
            new_user = {
                "phone": phone,
                "role": role,
                "name": f"User {phone[-4:]}",
                "created_at": datetime.utcnow(),
                "vault": []
            }
            mongo.db.users.insert_one(new_user)
        
        # Clear the OTP
        del otps[phone]
        
        return jsonify({
            "status": "success", 
            "message": "Login successful",
            "user": {
                "phone": phone,
                "role": role
            }
        }), 200
    
    return jsonify({"status": "error", "message": "Invalid OTP"}), 401

@auth_bp.route("/profile", methods=["GET"])
def get_profile():
    phone = request.args.get("phone")
    if not phone:
        return jsonify({"status": "error", "message": "Phone number is required"}), 400
    
    user = mongo.db.users.find_one({"phone": phone})
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
        
    # Remove MongoDB's internal ID
    user.pop("_id", None)
    
    return jsonify({
        "status": "success",
        "user": user
    }), 200
