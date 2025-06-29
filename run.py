import os
import webbrowser
from app import create_app

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