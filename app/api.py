from flask import Blueprint, jsonify
from app.models import CampusNavigation

api = Blueprint('api', __name__)

# Initialize campus navigation
campus_nav = CampusNavigation()

@api.route('/routes', methods=['GET'])
def get_routes():
    """API endpoint to get all available routes"""
    return jsonify(campus_nav.get_available_routes())

@api.route('/buildings', methods=['GET'])
def get_buildings():
    """API endpoint to get building descriptions"""
    return jsonify(campus_nav.get_building_descriptions())

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy', 'service': 'UCA Campus Navigation'}) 