# UCA Campus Navigation System

A modern web app for navigating the University of Central Asia campus. Built with Flask and Folium, it helps users find routes between buildings and view interactive campus maps.

## Features
- Interactive campus map with building outlines
- Route planning between academic and dormitory buildings
- Toggle building visibility (LayerControl)
- Responsive and mobile-friendly UI

## Buildings
- Academic block (main academic)
- A1, A2, B1, B2 blocks (dormitories)

## Quick Start
1. **Clone & Install**
   ```bash
   git clone <repo-url>
   cd UCA-Campus-Navigation
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. **Run**
   ```bash
   python run.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure
- `app/` - Flask app modules
- `templates/` - HTML templates
- `Buildings/`, `Paths/` - GeoJSON data
- `run.py` - App entry point

## API
- `/api/routes` - All routes
- `/api/buildings` - Building info
- `/api/health` - Health check

---
MIT License. For questions, open an issue. 