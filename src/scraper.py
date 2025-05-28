import requests
import json
import sqlite3
import datetime
from typing import Dict, List, Optional
import time

class IthacaWeatherScraper:
    def __init__(self, api_key: str, db_path: str = "data/weather.db"):
        self.api_key = api_key
        self.db_path = db_path
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        
        # Ithaca area locations
        self.locations = {
            "Downtown Ithaca": {"lat": 42.4430, "lon": -76.5019},
            "Cornell Campus": {"lat": 42.4534, "lon": -76.4735},
            "Ithaca College": {"lat": 42.4206, "lon": -76.4951},
            "Cayuga Lake": {"lat": 42.4301, "lon": -76.5370}
        }
        
        self.setup_database()
    
    def setup_database(self):
        """Initialize SQLite database with weather data table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                temperature REAL,
                feels_like REAL,
                humidity INTEGER,
                pressure REAL,
                visibility REAL,
                uv_index REAL,
                weather_main TEXT,
                weather_description TEXT,
                wind_speed REAL,
                wind_direction INTEGER,
                cloudiness INTEGER,
                sunrise DATETIME,
                sunset DATETIME,
                raw_data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_current_weather(self, location_name: str) -> Optional[Dict]:
        """Fetch current weather for a specific location"""
        if location_name not in self.locations:
            print(f"Location {location_name} not found")
            return None
        
        coords = self.locations[location_name]
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {location_name}: {e}")
            return None
    
    def parse_weather_data(self, raw_data: Dict, location_name: str) -> Dict:
        """Parse raw API response into structured data"""
        main = raw_data.get('main', {})
        weather = raw_data.get('weather', [{}])[0]
        wind = raw_data.get('wind', {})
        sys = raw_data.get('sys', {})
        
        return {
            'location': location_name,
            'timestamp': datetime.datetime.now(),
            'temperature': main.get('temp'),
            'feels_like': main.get('feels_like'),
            'humidity': main.get('humidity'),
            'pressure': main.get('pressure'),
            'visibility': raw_data.get('visibility', 0) / 1000,  # Convert to km
            'weather_main': weather.get('main'),
            'weather_description': weather.get('description'),
            'wind_speed': wind.get('speed'),
            'wind_direction': wind.get('deg'),
            'cloudiness': raw_data.get('clouds', {}).get('all'),
            'sunrise': datetime.datetime.fromtimestamp(sys.get('sunrise', 0)),
            'sunset': datetime.datetime.fromtimestamp(sys.get('sunset', 0)),
            'raw_data': json.dumps(raw_data)
        }
    
    def save_weather_data(self, weather_data: Dict):
        """Save parsed weather data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO weather_data (
                location, timestamp, temperature, feels_like, humidity, pressure,
                visibility, weather_main, weather_description, wind_speed,
                wind_direction, cloudiness, sunrise, sunset, raw_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather_data['location'],
            weather_data['timestamp'],
            weather_data['temperature'],
            weather_data['feels_like'],
            weather_data['humidity'],
            weather_data['pressure'],
            weather_data['visibility'],
            weather_data['weather_main'],
            weather_data['weather_description'],
            weather_data['wind_speed'],
            weather_data['wind_direction'],
            weather_data['cloudiness'],
            weather_data['sunrise'],
            weather_data['sunset'],
            weather_data['raw_data']
        ))
        
        conn.commit()
        conn.close()
    
    def scrape_all_locations(self):
        """Scrape weather data for all Ithaca locations"""
        print(f"🌤️  Starting weather scrape at {datetime.datetime.now()}")
        
        for location_name in self.locations:
            print(f"Fetching weather for {location_name}...")
            
            raw_data = self.get_current_weather(location_name)
            if raw_data:
                parsed_data = self.parse_weather_data(raw_data, location_name)
                self.save_weather_data(parsed_data)
                print(f"✅ Saved {location_name}: {parsed_data['temperature']}°F, {parsed_data['weather_description']}")
            else:
                print(f"❌ Failed to fetch data for {location_name}")
            
            # Be nice to the API
            time.sleep(1)
        
        print("🎉 Weather scrape completed!\n")
    
    def get_recent_data(self, hours: int = 24) -> List[Dict]:
        """Get weather data from the last N hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = datetime.datetime.now() - datetime.timedelta(hours=hours)
        
        cursor.execute('''
            SELECT * FROM weather_data 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC
        ''', (since,))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results

# Example usage
if __name__ == "__main__":
    # You'll need to get your API key from https://openweathermap.org/api
    API_KEY = "your_openweathermap_api_key_here"
    
    scraper = IthacaWeatherScraper(API_KEY)
    scraper.scrape_all_locations()
    
    # Show recent data
    recent = scraper.get_recent_data(hours=1)
    print(f"Collected {len(recent)} data points in the last hour")
