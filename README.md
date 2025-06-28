# UCA Campus Navigation System

A modern, interactive web-based navigation system for the University of Central Asia campus. This application helps students, staff, and visitors find optimal routes between different campus buildings with visual maps and detailed route information.

## 🌟 Features

- **Interactive Maps**: Real-time route visualization with animated paths
- **Building Information**: Detailed descriptions of all campus buildings
- **Route Details**: Estimated time, distance, and route type for each path
- **Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **User-Friendly Interface**: Modern UI with intuitive navigation
- **Error Handling**: Comprehensive validation and error messages
- **Accessibility**: Keyboard navigation and screen reader support
- **Persistent Selections**: Remembers user's previous route selections

## 🏗️ Campus Buildings

- **Academic Block**: Main academic building with classrooms, offices, and administrative facilities
- **A1 Block**: A-series building 1 - Contains specialized classrooms and labs
- **A2 Block**: A-series building 2 - Houses additional academic facilities
- **B1 Block**: B-series building 1 - Features modern learning spaces
- **B2 Block**: B-series building 2 - Contains advanced research facilities

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd Navigation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   - The application will automatically open in your default web browser
   - If it doesn't open automatically, navigate to: `http://127.0.0.1:5000`

## 🚀 Deployment Options

### Quick Deployment
Use our automated deployment script:
```bash
python deploy.py
```

### 1. **Local Docker Deployment** (Recommended for testing)
```bash
# Build and run with Docker Compose
docker-compose up --build -d

# Access at: http://localhost:5000
# Stop with: docker-compose down
```

### 2. **Heroku Cloud Deployment** (Free tier available)
```bash
# Install Heroku CLI first
# Then run:
python deploy.py
# Select option 2 for Heroku deployment
```

### 3. **Docker Cloud Platforms**
- **Docker Hub**: Share your container image
- **Google Cloud Run**: Serverless container deployment
- **AWS ECS**: Amazon's container orchestration
- **Azure Container Instances**: Microsoft's container service

### 4. **Manual Deployment Steps**

#### Heroku Deployment
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

#### Docker Deployment
```bash
# Build image
docker build -t uca-navigation .

# Run container
docker run -p 5000:5000 uca-navigation

# Or use docker-compose
docker-compose up --build
```

#### Production Server Deployment
```bash
# Install gunicorn
pip install gunicorn

# Run in production mode
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

## 📱 Usage

### Basic Navigation
1. Select your **start location** from the dropdown menu
2. Select your **destination** from the dropdown menu
3. Click **"Show Route"** to display the navigation path
4. View route details including estimated time and distance

### Features
- **Reset Map**: Click "Reset Map" to return to the overview of all buildings
- **Mobile Toggle**: On mobile devices, use the hamburger menu to show/hide the navigation panel
- **Building Information**: Scroll down in the sidebar to see descriptions of all campus buildings

### Route Information
Each route displays:
- ⏱️ **Estimated Time**: How long the journey typically takes
- 📏 **Distance**: Approximate distance of the route
- 🛣️ **Route Type**: Description of the path (e.g., "Direct via bridge", "Via A1 block and under bridge")

## 🗂️ Project Structure

```
Navigation/
├── main.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment config
├── runtime.txt            # Python version for Heroku
├── Dockerfile             # Docker container config
├── docker-compose.yml     # Docker Compose config
├── deploy.py              # Deployment automation script
├── install.py             # Installation helper script
├── README.md              # This file
├── Buildings/             # GeoJSON files for building outlines
│   ├── Academic block.geojson
│   ├── A1 block.geojson
│   ├── A2 block.geojson
│   ├── B1 block.geojson
│   ├── B2 block.geojson
│   ├── Bridge.geojson
│   ├── Under the bridge A block.geojson
│   └── Under the bridge B block.geojson
├── Paths/                 # GeoJSON files for route paths
│   ├── Academic block_to_A1 block.geojson
│   ├── Academic block_to_A2 block.geojson
│   └── ... (20 route files)
└── templates/             # HTML templates
    └── index.html         # Main application interface
```

## 🔧 Technical Details

### Technologies Used
- **Backend**: Flask (Python web framework)
- **Maps**: Folium (Python library for interactive maps)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with responsive design
- **Icons**: Font Awesome 6.0
- **Production**: Gunicorn (WSGI server)

### Key Components
- **CampusNavigation Class**: Core navigation logic and data management
- **Flask Routes**: Web endpoints for serving the application
- **GeoJSON Processing**: Handles building outlines and route paths
- **Interactive Maps**: Folium-based map visualization with markers and animated paths

### API Endpoints
- `GET /`: Main application interface
- `POST /`: Process route requests
- `GET /api/routes`: Get all available routes (JSON)
- `GET /api/buildings`: Get building descriptions (JSON)
- `GET /health`: Health check endpoint for deployment

### Environment Variables
- `FLASK_ENV`: Set to 'production' for production deployment
- `PORT`: Port number (default: 5000)
- `SECRET_KEY`: Secret key for Flask sessions

## 🎨 UI/UX Improvements

### Modern Design
- Gradient backgrounds and glassmorphism effects
- Smooth animations and transitions
- Intuitive iconography and visual feedback
- Professional color scheme

### Mobile Experience
- Responsive design that adapts to all screen sizes
- Collapsible sidebar for mobile devices
- Touch-friendly interface elements
- Optimized for mobile navigation

### Accessibility
- Keyboard navigation support
- Screen reader compatibility
- High contrast elements
- Clear focus indicators

## 🔒 Security & Production

### Security Best Practices
- Environment-based configuration
- Secure secret key management
- Input validation and sanitization
- Error handling without sensitive data exposure

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Configure secure `SECRET_KEY`
- [ ] Use HTTPS in production
- [ ] Set up proper logging
- [ ] Configure monitoring and health checks
- [ ] Set up backup and recovery procedures

## 🚀 Future Enhancements

Potential improvements for future versions:
- **Real-time Location**: GPS integration for current location
- **Multiple Routes**: Alternative route suggestions
- **Indoor Navigation**: Detailed indoor building maps
- **Accessibility Features**: Wheelchair-accessible routes
- **Weather Integration**: Route adjustments based on weather
- **Search Functionality**: Building search by name or function
- **User Accounts**: Personalized route history and favorites
- **Analytics**: Usage tracking and route popularity
- **Offline Support**: PWA capabilities for offline use

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for the University of Central Asia. Please contact the university for usage permissions.

## 📞 Support

For technical support or questions about the navigation system, please contact the UCA IT department or the project maintainers.

---

**Developed for University of Central Asia** 🎓 