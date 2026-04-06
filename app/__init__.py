import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MongoDB
mongo = PyMongo()

def create_app():
    # Configure Flask to serve static files from the 'frontend' folder
    app = Flask(__name__, static_folder="../frontend", static_url_path="")
    
    # Configure the Flask App
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb+srv://user:password@cluster0.abcde.mongodb.net/eseva_portal?retryWrites=true&w=majority")
    
    # Initialize Extensions
    mongo.init_app(app)
    CORS(app)
    
    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.upload import upload_bp
    from app.routes.franchise import franchise_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(franchise_bp, url_prefix="/api/franchise")
    
    @app.route("/")
    def index():
        return app.send_static_file("index.html")
    
    return app
