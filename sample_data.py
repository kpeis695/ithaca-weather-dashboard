import sqlite3
import datetime
import random
import json
import os

def create_sample_weather_data(db_path="data/weather.db"):
    """Generate realistic sample weather data for Ithaca locations"""
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
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
    
    locations = {
        "Downtown Ithaca": {"base_temp": 62, "elevation": 0},
        "Cornell Campus": {"base_temp": 60, "elevation": 2},
        "Ithaca College": {"base_temp": 61, "elevation": 1},
        "Cayuga Lake": {"base_temp": 64, "elevation": -1}
    }
    
    weather_conditions = [
        "Sunny", "Partly cloudy", "Cloudy", "Overcast", 
        "Light rain", "Rain", "Drizzle", "Foggy", "Clear"
    ]
    
    wind_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    
    # Generate data for the last 7 days, every 2 hours
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=7)
    current_time = start_time
    
    print("Generating sample weather data...")
    
    while current_time <= end_time:
        # Base weather pattern for this time
        hour = current_time.hour
        day_factor = (hour - 6) / 12  # Temperature variation throughout day
        day_factor = max(0, min(1, day_factor))
        
        # Add some weather variability
        weather_mood = random.choice(["stable", "changing", "volatile"])
        base_condition = random.choice(weather_conditions)
        
        for location, props in locations.items():
            # Temperature with realistic variation
            base_temp = props["base_temp"]
            temp_variation = props["elevation"] * 2  # Elevation effect
            daily_variation = day_factor * 15 - 7.5  # Daily temperature swing
            random_variation = random.uniform(-3, 3)
            
            if weather_mood == "volatile":
                random_variation *= 2
            
            temperature = base_temp + temp_variation + daily_variation + random_variation
            feels_like = temperature + random.uniform(-3, 3)
            
            # Other weather parameters
            humidity = random.randint(40, 90)
            pressure = random.uniform(29.8, 30.2)
            visibility = random.uniform(5, 15)
            uv_index = max(0, random.uniform(0, 8) * day_factor)
            wind_speed = random.uniform(2, 15)
            wind_direction = random.choice(wind_directions)
            wind_degree = wind_directions.index(wind_direction) * 45
            cloudiness = random.randint(10, 90)
            is_day = 1 if 6 <= hour <= 18 else 0
            
            # Adjust condition based on parameters
            if cloudiness > 70:
                condition = "Overcast"
            elif cloudiness > 40:
                condition = "Partly cloudy"
            elif humidity > 80 and random.random() > 0.7:
                condition = "Light rain"
            else:
                condition = base_condition
            
            # Create realistic raw data
            raw_data = {
                "location": {"name": location},
                "current": {
                    "temp_f": round(temperature, 1),
                    "feelslike_f": round(feels_like, 1),
                    "humidity": humidity,
                    "pressure_in": round(pressure, 2),
                    "vis_miles": round(visibility, 1),
                    "uv": round(uv_index, 1),
                    "wind_mph": round(wind_speed, 1),
                    "wind_dir": wind_direction,
                    "wind_degree": wind_degree,
                    "cloud": cloudiness,
                    "is_day": is_day,
                    "condition": {"text": condition}
                }
            }
            
            # Insert data
            cursor.execute('''
                INSERT INTO weather_data (
                    location, timestamp, temperature, feels_like, humidity, pressure,
                    visibility, uv_index, weather_condition, weather_description, 
                    wind_speed, wind_direction, wind_degree, cloudiness, is_day, raw_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                location,
                current_time,
                round(temperature, 1),
                round(feels_like, 1),
                humidity,
                round(pressure, 2),
                round(visibility, 1),
                round(uv_index, 1),
                condition,
                condition,
                round(wind_speed, 1),
                wind_direction,
                wind_degree,
                cloudiness,
                is_day,
                json.dumps(raw_data)
            ))
        
        # Move to next time point (every 2 hours)
        current_time += datetime.timedelta(hours=2)
    
    conn.commit()
    
    # Print summary
    cursor.execute('SELECT COUNT(*) FROM weather_data')
    total_records = cursor.fetchone()[0]
    
    cursor.execute('SELECT location, COUNT(*) FROM weather_data GROUP BY location')
    location_counts = cursor.fetchall()
    
    print(f"\n✅ Sample data generation complete!")
    print(f"📊 Total records: {total_records}")
    print("📍 Records per location:")
    for location, count in location_counts:
        print(f"   {location}: {count} records")
    
    # Show recent data sample
    cursor.execute('''
        SELECT location, temperature, weather_condition, timestamp 
        FROM weather_data 
        ORDER BY timestamp DESC 
        LIMIT 8
    ''')
    recent_data = cursor.fetchall()
    
    print(f"\n🌤️ Recent sample data:")
    for location, temp, condition, timestamp in recent_data:
        print(f"   {location}: {temp}°F, {condition} ({timestamp})")
    
    conn.close()

if __name__ == "__main__":
    create_sample_weather_data()
    print("\n🚀 Ready to run dashboard with sample data!")
    print("Run: python3 src/dashboard.py")
