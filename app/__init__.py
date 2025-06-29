from flask import Flask
from config import config
import os

def create_app(config_name='default'):
    """Application factory function"""
    # Get the current directory (where run.py is located)
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(current_dir, 'templates'))
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app 