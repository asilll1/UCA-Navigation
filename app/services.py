import json
import os
import folium
from folium import plugins
from typing import List, Dict, Optional
from app.models import CampusNavigation

class MapService:
    """Handles map generation and GeoJSON processing"""
    
    def __init__(self, campus_nav: CampusNavigation):
        self.campus_nav = campus_nav
        self.location = campus_nav.location

    def create_empty_map(self) -> str:
        """Create an empty map with building outlines"""
        try:
            print("Creating empty map...")
            map_empty = folium.Map(location=self.location, width="100%", height="100%", zoom_start=20)
            
            # Add all building outlines to the empty map, each as a named layer
            building_count = 0
            for building_file in os.listdir('Buildings'):
                if building_file.endswith('.geojson'):
                    try:
                        with open(f'Buildings/{building_file}') as f:
                            building_data = json.load(f)
                            building_name = building_file.replace('.geojson', '')
                            folium.GeoJson(
                                building_data, 
                                name=building_name,  # Named layer for LayerControl
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
            
            # Add layer control in the top right
            folium.LayerControl(position='topright').add_to(map_empty)
            
            # Generate HTML
            map_html = map_empty._repr_html_()
            print(f"Map HTML generated, length: {len(map_html)}")
            return map_html
            
        except Exception as e:
            print(f"Error creating empty map: {e}")
            # Return a simple fallback map
            fallback_map = folium.Map(location=self.location, zoom_start=20)
            return fallback_map._repr_html_()

    def create_route_map(self, start_file: str, destination_file: str) -> str:
        """Create a navigation map with route between two buildings"""
        print(f"Processing route from {start_file} to {destination_file}")
        
        # Validate input
        if not start_file or not destination_file:
            return "Please select both start and destination locations."
        
        if start_file == destination_file:
            return "Start and destination cannot be the same."
        
        # Validate route exists
        is_valid, error_message = self.campus_nav.validate_route(start_file, destination_file)
        if not is_valid:
            return error_message

        path = None
        building1 = []

        condition = (start_file, destination_file)
        building_info = self.campus_nav.building_files.get(condition)

        if building_info:
            p_file = building_info['path']
            building1_paths = building_info['buildings']

            # Load building data with error handling
            for file_path in building1_paths:
                try:
                    if os.path.exists(file_path):
                        with open(file_path) as f:
                            building1.append((file_path, json.load(f)))
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
                final_path = list(map(self.campus_nav.switch_coords, path_coords))

                # Create a map with improved styling
                try:
                    map_academic = folium.Map(location=self.location, width="100%", height="100%", zoom_start=20)
                    
                    # Add building outlines with better styling, each as a named layer
                    for file_path, outline in building1:
                        building_name = os.path.basename(file_path).replace('.geojson', '')
                        folium.GeoJson(
                            outline, 
                            name=building_name,  # Named layer for LayerControl
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
                        opacity=0.8,
                        name='Route Path'  # Named layer for LayerControl
                    ).add_to(map_academic)
                    
                    # Add start and end markers
                    if final_path:
                        folium.Marker(
                            final_path[0],
                            popup=f"Start: {start_file}",
                            icon=folium.Icon(color='green', icon='info-sign'),
                            name='Start Marker'
                        ).add_to(map_academic)
                        
                        folium.Marker(
                            final_path[-1],
                            popup=f"Destination: {destination_file}",
                            icon=folium.Icon(color='red', icon='info-sign'),
                            name='End Marker'
                        ).add_to(map_academic)

                    # Add layer control in the top right
                    folium.LayerControl(position='topright').add_to(map_academic)

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