from flask import Blueprint, render_template, request
from app.models import CampusNavigation
from app.services import MapService

main = Blueprint('main', __name__)

# Initialize campus navigation and map service
campus_nav = CampusNavigation()
map_service = MapService(campus_nav)

@main.route('/', methods=['GET', 'POST'])
def index():
    """Main route for the campus navigation interface"""
    if request.method == 'POST':
        start_file = request.form.get('start', '').strip()
        dest_file = request.form.get('dest', '').strip()
        
        print(f"Received POST request: {start_file} -> {dest_file}")
        
        # Validate form data
        if not start_file or not dest_file:
            return render_template('index.html', 
                                map=map_service.create_empty_map(), 
                                error="Please select both start and destination locations.",
                                building_descriptions=campus_nav.get_building_descriptions())
        
        map_html = map_service.create_route_map(start_file, dest_file)
        
        # Check if there was an error
        if map_html.startswith("Error") or map_html.startswith("Invalid") or map_html.startswith("Please"):
            return render_template('index.html', 
                                map=map_service.create_empty_map(), 
                                error=map_html,
                                building_descriptions=campus_nav.get_building_descriptions())
        
        # Get route information for display
        route_info = campus_nav.get_route_info(start_file, dest_file)
        
        return render_template('index.html', 
                            map=map_html, 
                            route_info=route_info,
                            building_descriptions=campus_nav.get_building_descriptions())
    
    print("Rendering initial page with empty map")
    return render_template('index.html', 
                        map=map_service.create_empty_map(),
                        building_descriptions=campus_nav.get_building_descriptions()) 