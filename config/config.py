
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # OpenWeatherMap API Configuration
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
    
    # Database Configuration
    DATABASE_PATH = "data/weather.db"
    
    # Scraping Configuration
    SCRAPE_INTERVAL_MINUTES = 30  # How often to collect data
    DATA_RETENTION_DAYS = 365     # How long to keep historical data
    
    # Ithaca-specific settings
    LOCATIONS = {
        "Downtown Ithaca": {
            "lat": 42.4430, 
            "lon": -76.5019,
            "description": "Heart of Ithaca, Commons area"
        },
        "Cornell Campus": {
            "lat": 42.4534, 
            "lon": -76.4735,
            "description": "Cornell University campus on East Hill"
        },
        "Ithaca College": {
            "lat": 42.4206, 
            "lon": -76.4951,
            "description": "Ithaca College campus on South Hill"
        },
        "Cayuga Lake": {
            "lat": 42.4301, 
            "lon": -76.5370,
            "description": "Cayuga Lake waterfront"
        }
    }
    
    # Dashboard Configuration
    DASHBOARD_TITLE = "Ithaca Weather Intelligence"
    DASHBOARD_SUBTITLE = "Because Ithaca weather is beautifully unpredictable"
    DASHBOARD_PORT = 8050
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if cls.OPENWEATHER_API_KEY == 'your_api_key_here':
            raise ValueError(
                "Please set your OpenWeatherMap API key in the .env file or environment variables"
            )
        
        return True

# Create directories if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)
