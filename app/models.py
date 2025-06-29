import json
import os
from typing import Dict, List, Tuple, Optional

class CampusNavigation:
    """Handles campus navigation logic and data management"""
    
    def __init__(self):
        self.location = (41.42925349851171, 75.9012347499233)  # Default location coordinates

        # Building descriptions - updated to reflect that only Academic block is academic, others are dormitories
        self.building_descriptions = {
            'Academic block': 'Main academic building with classrooms, offices, and administrative facilities',
            'A1 block': 'Student dormitory',
            'A2 block': 'Student dormitory',
            'B1 block': 'Student dormitory',
            'B2 block': 'Student dormitory'
        }

        # Define paths and buildings for navigation
        self.building_files = self._initialize_routes()

    def _initialize_routes(self) -> Dict[Tuple[str, str], Dict]:
        """Initialize all available routes between buildings"""
        return {
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

    def get_building_descriptions(self) -> Dict[str, str]:
        """Return building descriptions for the frontend"""
        return self.building_descriptions

    def get_available_routes(self) -> List[Dict]:
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

    def validate_route(self, start_file: str, destination_file: str) -> Tuple[bool, str]:
        """Validate if the requested route exists"""
        condition = (start_file, destination_file)
        if condition not in self.building_files:
            return False, f"Route from {start_file} to {destination_file} is not available."
        return True, "Route is valid."

    def switch_coords(self, coordinate: List[float]) -> List[float]:
        """Reverse the order of coordinates for proper display"""
        return coordinate[::-1]

    def get_route_info(self, start_file: str, destination_file: str) -> Optional[Dict]:
        """Get route information for a specific route"""
        condition = (start_file, destination_file)
        return self.building_files.get(condition) 