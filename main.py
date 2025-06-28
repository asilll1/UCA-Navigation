from flask import Flask, render_template, request, jsonify  # Import necessary Flask modules
import folium  # Import folium for creating maps
from folium import plugins  # Import folium plugins for additional features
import json  # Import JSON module for data handling
import webbrowser  # Import webbrowser to open browser windows
import os  # Import os for file operations
from config import config  # Import configuration

class CampusNavigation:
    def __init__(self):
        self.location = (41.42925349851171, 75.9012347499233)  # Set default location coordinates

        # Building descriptions for better user experience
        self.building_descriptions = {
            'Academic block': 'Main academic building with classrooms, offices, and administrative facilities',
            'A1 block': 'A-series building 1 - Contains specialized classrooms and labs',
            'A2 block': 'A-series building 2 - Houses additional academic facilities',
            'B1 block': 'B-series building 1 - Features modern learning spaces',
            'B2 block': 'B-series building 2 - Contains advanced research facilities'
        }

        # Define paths and buildings for navigation
        self.building_files = {
            ('Academic block', 'A1 block'): {
                'path': 'Paths/Academic block_to_A1 block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson'
                ],
                'estimated_time': 2,
                'distance': '150m',
                'route_type': 'Direct via bridge'
            },
            ('Academic block', 'A2 block'): {
                'path': 'Paths/Academic block_to_A2 block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge A block.geojson'
                ],
                'estimated_time': 3,
                'distance': '250m',
                'route_type': 'Via A1 block and under bridge'
            },
            ('Academic block', 'B1 block'): {
                'path': 'Paths/Academic block_to_B1 block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/Bridge.geojson'
                ],
                'estimated_time': 3,
                'distance': '200m',
                'route_type': 'Direct via bridge'
            },
            ('Academic block', 'B2 block'): {
                'path': 'Paths/Academic block_to_B2 block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 4,
                'distance': '300m',
                'route_type': 'Via B1 block and under bridge'
            },
            ('A1 block', 'Academic block'): {
                'path': 'Paths/A1 block_to_Academic block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson'
                ],
                'estimated_time': 2,
                'distance': '150m',
                'route_type': 'Direct via bridge'
            },
            ('A1 block', 'A2 block'): {
                'path': 'Paths/A1 block_to_A2 block.geojson',
                'buildings': [
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/Under the bridge A block.geojson'
                ],
                'estimated_time': 1,
                'distance': '100m',
                'route_type': 'Direct under bridge'
            },
            ('A1 block', 'B1 block'): {
                'path': 'Paths/A1 block_to_B1 block.geojson',
                'buildings': [
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/B1 block.geojson'
                ],
                'estimated_time': 2,
                'distance': '180m',
                'route_type': 'Via bridge'
            },
            ('A1 block', 'B2 block'): {
                'path': 'Paths/A1 block_to_B2 block.geojson',
                'buildings': [
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 3,
                'distance': '280m',
                'route_type': 'Via bridge and B1 block'
            },
            ('A2 block', 'Academic block'): {
                'path': 'Paths/A2 block_to_Academic block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge A block.geojson'
                ],
                'estimated_time': 3,
                'distance': '250m',
                'route_type': 'Via A1 block and bridge'
            },
            ('A2 block', 'A1 block'): {
                'path': 'Paths/A2 block_to_A1 block.geojson',
                'buildings': [
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/Under the bridge A block.geojson'
                ],
                'estimated_time': 1,
                'distance': '100m',
                'route_type': 'Direct under bridge'
            },
            ('A2 block', 'B1 block'): {
                'path': 'Paths/A2 block_to_B1 block.geojson',
                'buildings': [
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge A block.geojson'
                ],
                'estimated_time': 3,
                'distance': '280m',
                'route_type': 'Via A1 block and bridge'
            },
            ('A2 block', 'B2 block'): {
                'path': 'Paths/A2 block_to_B2 block.geojson',
                'buildings': [
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge A block.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 4,
                'distance': '380m',
                'route_type': 'Via A1 block, bridge, and B1 block'
            },
            ('B1 block', 'Academic block'): {
                'path': 'Paths/B1 block_to_Academic block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/Bridge.geojson'
                ],
                'estimated_time': 3,
                'distance': '200m',
                'route_type': 'Direct via bridge'
            },
            ('B1 block', 'A1 block'): {
                'path': 'Paths/B1 block_to_A1 block.geojson',
                'buildings': [
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/B1 block.geojson'
                ],
                'estimated_time': 2,
                'distance': '180m',
                'route_type': 'Via bridge'
            },
            ('B1 block', 'A2 block'): {
                'path': 'Paths/B1 block_to_A2 block.geojson',
                'buildings': [
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge A block.geojson'
                ],
                'estimated_time': 3,
                'distance': '280m',
                'route_type': 'Via bridge and A1 block'
            },
            ('B1 block', 'B2 block'): {
                'path': 'Paths/B1 block_to_B2 block.geojson',
                'buildings': [
                    'Buildings/B1 block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 1,
                'distance': '100m',
                'route_type': 'Direct under bridge'
            },
            ('B2 block', 'Academic block'): {
                'path': 'Paths/B2 block_to_Academic block.geojson',
                'buildings': [
                    'Buildings/Academic block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 4,
                'distance': '300m',
                'route_type': 'Via B1 block and bridge'
            },
            ('B2 block', 'A1 block'): {
                'path': 'Paths/B2 block_to_A1 block.geojson',
                'buildings': [
                    'Buildings/A1 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 3,
                'distance': '280m',
                'route_type': 'Via bridge and B1 block'
            },
            ('B2 block', 'A2 block'): {
                'path': 'Paths/B2 block_to_A2 block.geojson',
                'buildings': [
                    'Buildings/A2 block.geojson',
                    'Buildings/A1 block.geojson',
                    'Buildings/B1 block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/Bridge.geojson',
                    'Buildings/Under the bridge A block.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 4,
                'distance': '380m',
                'route_type': 'Via B1 block, bridge, and A1 block'
            },
            ('B2 block', 'B1 block'): {
                'path': 'Paths/B2 block_to_B1 block.geojson',
                'buildings': [
                    'Buildings/B1 block.geojson',
                    'Buildings/B2 block.geojson',
                    'Buildings/Under the bridge B block.geojson'
                ],
                'estimated_time': 1,
                'distance': '100m',
                'route_type': 'Direct under bridge'
            }
        }

    def get_building_descriptions(self):
        """Return building descriptions for the frontend"""
        return self.building_descriptions

    def get_available_routes(self):
        """Return all available routes for the frontend"""
        routes = []
        for (start, dest), info in self.building_files.items():
            routes.append({
                'start': start,
                'destination': dest,
                'estimated_time': info['estimated_time'],
                'distance': info['distance'],
                'route_type': info['route_type']
            })
        return routes

    def empty_map(self):
        """Create an empty map with building outlines"""
        try:
            print("Creating empty map...")
            map_empty = folium.Map(location=self.location, width="100%", height="100%", zoom_start=20)
            
            # Add all building outlines to the empty map
            building_count = 0
            for building_file in os.listdir('Buildings'):
                if building_file.endswith('.geojson'):
                    try:
                        with open(f'Buildings/{building_file}') as f:
                            building_data = json.load(f)
                            building_name = building_file.replace('.geojson', '')
                            folium.GeoJson(
                                building_data, 
                                name=building_name,
                                tooltip=building_name,
                                popup=building_name,
                                style_function=lambda x: {
                                    'fillColor': '#3388ff',
                                    'color': '#000000',
                                    'weight': 2,
                                    'fillOpacity': 0.1
                                }
                            ).add_to(map_empty)
                            building_count += 1
                    except Exception as e:
                        print(f"Error loading building {building_file}: {e}")
            
            print(f"Added {building_count} buildings to the map")
            
            # Add layer control
            folium.LayerControl().add_to(map_empty)
            
            # Generate HTML
            map_html = map_empty._repr_html_()
            print(f"Map HTML generated, length: {len(map_html)}")
            return map_html
            
        except Exception as e:
            print(f"Error creating empty map: {e}")
            # Return a simple fallback map
            fallback_map = folium.Map(location=self.location, zoom_start=20)
            return fallback_map._repr_html_()

    def switch_coords(self, coordinate):
        """Reverse the order of coordinates for proper display"""
        return coordinate[::-1]

    def validate_route(self, start_file, destination_file):
        """Validate if the requested route exists"""
        condition = (start_file, destination_file)
        if condition not in self.building_files:
            return False, f"Route from {start_file} to {destination_file} is not available."
        return True, "Route is valid."

    def process_geojson(self, start_file, destination_file):
        """Process GeoJSON files and create navigation map with error handling"""
        print(f"Processing route from {start_file} to {destination_file}")
        
        # Validate input
        if not start_file or not destination_file:
            return "Please select both start and destination locations."
        
        if start_file == destination_file:
            return "Start and destination cannot be the same."
        
        # Validate route exists
        is_valid, error_message = self.validate_route(start_file, destination_file)
        if not is_valid:
            return error_message

        path = None
        building1 = []

        condition = (start_file, destination_file)
        building_info = self.building_files.get(condition)

        if building_info:
            p_file = building_info['path']
            building1_paths = building_info['buildings']

            # Load building data with error handling
            for file_path in building1_paths:
                try:
                    if os.path.exists(file_path):
                        with open(file_path) as f:
                            building1.append(json.load(f))
                    else:
                        return f"Building file not found: {file_path}"
                except json.JSONDecodeError:
                    return f"Invalid JSON in building file: {file_path}"
                except Exception as e:
                    return f"Error loading building file {file_path}: {str(e)}"

            # Load path data with error handling
            try:
                if os.path.exists(p_file):
                    with open(p_file) as f1:
                        path = json.load(f1)
                else:
                    return f"Path file not found: {p_file}"
            except json.JSONDecodeError:
                return f"Invalid JSON in path file: {p_file}"
            except Exception as e:
                return f"Error loading path file {p_file}: {str(e)}"

        if path:
            path_coords = None
            for feature in path['features']:
                path_coords = feature['geometry']['coordinates']

            if path_coords:
                final_path = list(map(self.switch_coords, path_coords))

                # Create a map with improved styling
                try:
                    map_academic = folium.Map(location=self.location, width="100%", height="100%", zoom_start=20)
                    
                    # Add building outlines with better styling
                    for outline in building1:
                        folium.GeoJson(
                            outline, 
                            name="Campus Buildings",
                            style_function=lambda x: {
                                'fillColor': '#3388ff',
                                'color': '#000000',
                                'weight': 2,
                                'fillOpacity': 0.1
                            }
                        ).add_to(map_academic)
                    
                    # Add animated path with better styling
                    folium.plugins.AntPath(
                        final_path, 
                        use_arrows=True,
                        color='red',
                        weight=4,
                        opacity=0.8
                    ).add_to(map_academic)
                    
                    # Add start and end markers
                    if final_path:
                        folium.Marker(
                            final_path[0],
                            popup=f"Start: {start_file}",
                            icon=folium.Icon(color='green', icon='info-sign')
                        ).add_to(map_academic)
                        
                        folium.Marker(
                            final_path[-1],
                            popup=f"Destination: {destination_file}",
                            icon=folium.Icon(color='red', icon='info-sign')
                        ).add_to(map_academic)

                    map_html = map_academic._repr_html_()
                    print(f"Route map generated successfully, HTML length: {len(map_html)}")
                    return map_html
                    
                except Exception as e:
                    print(f"Error creating route map: {e}")
                    return f"Error creating map: {str(e)}"
            else:
                return "Invalid geojson data: No coordinates found in path."
        else:
            return "Invalid address: Path data not found."

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize campus navigation
    campus_map = CampusNavigation()
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            start_file = request.form.get('start', '').strip()
            dest_file = request.form.get('dest', '').strip()
            
            print(f"Received POST request: {start_file} -> {dest_file}")
            
            # Validate form data
            if not start_file or not dest_file:
                return render_template('index.html', 
                                    map=campus_map.empty_map(), 
                                    error="Please select both start and destination locations.",
                                    building_descriptions=campus_map.get_building_descriptions())
            
            map_html = campus_map.process_geojson(start_file, dest_file)
            
            # Check if there was an error
            if map_html.startswith("Error") or map_html.startswith("Invalid") or map_html.startswith("Please"):
                return render_template('index.html', 
                                    map=campus_map.empty_map(), 
                                    error=map_html,
                                    building_descriptions=campus_map.get_building_descriptions())
            
            # Get route information for display
            condition = (start_file, dest_file)
            route_info = campus_map.building_files.get(condition, {})
            
            return render_template('index.html', 
                                map=map_html, 
                                route_info=route_info,
                                building_descriptions=campus_map.get_building_descriptions())
        
        print("Rendering initial page with empty map")
        return render_template('index.html', 
                            map=campus_map.empty_map(),
                            building_descriptions=campus_map.get_building_descriptions())

    @app.route('/api/routes', methods=['GET'])
    def get_routes():
        """API endpoint to get all available routes"""
        return jsonify(campus_map.get_available_routes())

    @app.route('/api/buildings', methods=['GET'])
    def get_buildings():
        """API endpoint to get building descriptions"""
        return jsonify(campus_map.get_building_descriptions())
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for deployment"""
        return jsonify({'status': 'healthy', 'service': 'UCA Campus Navigation'})

    return app

# Create the app instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == "__main__":
    # Only open browser in development
    if app.config['DEBUG']:
        print("Starting UCA Campus Navigation System...")
        print("Opening browser at http://127.0.0.1:5000")
        webbrowser.open('http://127.0.0.1:5000')
    
    # Run the app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
