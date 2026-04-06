import os
from app import create_app

# Create Flask app instance
app = create_app()

if __name__ == "__main__":
    # Check if the secret key is defined in the environment
    if not os.getenv("SECRET_KEY"):
        print("WARNING: SECRET_KEY is not defined in the environment. Using default key for development.")
    
    # Check if the MongoDB URI is defined in the environment
    if not os.getenv("MONGO_URI"):
        print("WARNING: MONGO_URI is not defined in the environment. Using default MongoDB URI for development.")

    # Run the application
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
