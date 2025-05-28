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
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        
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
                weather_condition TEXT,
                weather_description TEXT,
                wind_speed REAL,
                wind_direction TEXT,
                wind_degree INTEGER,
                cloudiness INTEGER,
                is_day INTEGER,
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
            'key': self.api_key,
            'q': f"{coords['lat']},{coords['lon']}",
            'aqi': 'no'
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
        current = raw_data.get('current', {})
        condition = current.get('condition', {})
        
        return {
            'location': location_name,
            'timestamp': datetime.datetime.now(),
            'temperature': current.get('temp_f'),
            'feels_like': current.get('feelslike_f'),
            'humidity': current.get('humidity'),
            'pressure': current.get('pressure_in'),
            'visibility': current.get('vis_miles'),
            'uv_index': current.get('uv'),
            'weather_condition': condition.get('text'),
            'weather_description': condition.get('text'),
            'wind_speed': current.get('wind_mph'),
            'wind_direction': current.get('wind_dir'),
            'wind_degree': current.get('wind_degree'),
            'cloudiness': current.get('cloud'),
            'is_day': current.get('is_day'),
            'raw_data': json.dumps(raw_data)
        }
    
    def save_weather_data(self, weather_data: Dict):
        """Save parsed weather data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO weather_data (
                location, timestamp, temperature, feels_like, humidity, pressure,
                visibility, uv_index, weather_condition, weather_description, 
                wind_speed, wind_direction, wind_degree, cloudiness, is_day, raw_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather_data['location'],
            weather_data['timestamp'],
            weather_data['temperature'],
            weather_data['feels_like'],
            weather_data['humidity'],
            weather_data['pressure'],
            weather_data['visibility'],
            weather_data['uv_index'],
            weather_data['weather_condition'],
            weather_data['weather_description'],
            weather_data['wind_speed'],
            weather_data['wind_direction'],
            weather_data['wind_degree'],
            weather_data['cloudiness'],
            weather_data['is_day'],
            weather_data['raw_data']
        ))
        
        conn.commit()
        conn.close()
    
    def scrape_all_locations(self):
        """Scrape weather data for all Ithaca locations"""
        print(f"Starting weather scrape at {datetime.datetime.now()}")
        
        for location_name in self.locations:
            print(f"Fetching weather for {location_name}...")
            
            raw_data = self.get_current_weather(location_name)
            if raw_data:
                parsed_data = self.parse_weather_data(raw_data, location_name)
                self.save_weather_data(parsed_data)
                temp = parsed_data['temperature']
                condition = parsed_data['weather_condition']
                print(f"✅ Saved {location_name}: {temp}°F, {condition}")
            else:
                print(f"❌ Failed to fetch data for {location_name}")
            
            # Be nice to the API
            time.sleep(1)
        
        print("Weather scrape completed!")
    
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
    
    def get_location_summary(self):
        """Get current weather summary for all locations"""
        recent_data = self.get_recent_data(hours=1)
        
        if not recent_data:
            print("No recent data found. Run scrape_all_locations() first.")
            return
        
        print("\n=== ITHACA WEATHER SNAPSHOT ===")
        for location in self.locations:
            location_data = [d for d in recent_data if d['location'] == location]
            if location_data:
                data = location_data[0]  # Most recent
                print(f"{location}: {data['temperature']}°F ({data['weather_condition']}) - Feels like {data['feels_like']}°F")
        
        # Calculate temperature variance
        temps = [d['temperature'] for d in recent_data if d['temperature']]
        if len(temps) > 1:
            temp_range = max(temps) - min(temps)
            print(f"\nTemperature variance across locations: {temp_range:.1f}°F")
            if temp_range > 5:
                print("🌡️ Significant temperature differences detected across Ithaca!")

# Example usage
if __name__ == "__main__":
    # You'll need to get your API key from https://www.weatherapi.com/
    API_KEY = "aee5a02325c04b4a9eb161027252805"
    
    scraper = IthacaWeatherScraper(API_KEY)
    scraper.scrape_all_locations()
    
    # Show summary
    scraper.get_location_summary()
