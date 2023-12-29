from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Register routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
