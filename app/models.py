from datetime import datetime

# This file is for documentation and structure. 
# Since we use MongoDB, there's no fixed schema defined in class.
# But we should consistently use these fields as shown in the blueprints.

# User Structure:
# {
#   "_id": "user_id_mongo",
#   "phone": "+91XXXXXXXXXX",
#   "name": "Citizen Name",
#   "role": "citizen" OR "franchise",
#   "created_at": "datetime",
#   "vault": [
#     {
#       "doc_id": "unique_doc_id",
#       "doc_type": "Aadhaar",
#       "status": "pending_review",
#       "file_url": "path_or_drive_id",
#       "submitted_at": "datetime",
#       "franchise_id": "franchise_001",
#       "meta": {
#           "blur_score": 85.5,
#           "ocr_text": "extracted_data"
#       },
#       "feedback": "Image too dark",
#       "action_at": "datetime"
#     }
#   ]
# }

# Franchise Structure:
# {
#   "_id": "franchise_id_mongo",
#   "franchise_id": "franchise_001",
#   "operator_name": "Operator Name",
#   "location": "City, State",
#   "phone": "+91XXXXXXXXXX"
# }
