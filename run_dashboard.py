#!/usr/bin/env python3
"""
Ithaca Weather Dashboard Runner

This script launches the interactive weather dashboard.
Make sure you have weather data by running the scraper first!
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['dash', 'plotly', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n🔧 Install missing packages with:")
        print(f"   pip3 install {' '.join(missing_packages)}")
        return False
    
    return True

def check_data():
    """Check if weather data exists"""
    db_path = "data/weather.db"
    if not os.path.exists(db_path):
        print("❌ No weather database found!")
        print("🔧 Run the scraper first to collect data:")
        print("   python3 src/scraper.py")
        return False
    
    return True

def main():
    print("🌤️ Ithaca Weather Dashboard Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check data
    if not check_data():
        print("\n⚠️  Dashboard will show 'No data available' until you run the scraper")
        input("Press Enter to continue anyway, or Ctrl+C to cancel...")
    
    # Launch dashboard
    try:
        print("\n🚀 Launching dashboard...")
        print("📊 Dashboard will be available at: http://localhost:8050")
        print("🔄 Press Ctrl+C to stop the dashboard")
        print("-" * 40)
        
        from src.dashboard import IthacaWeatherDashboard
        dashboard = IthacaWeatherDashboard()
        dashboard.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Thanks for using Ithaca Weather Intelligence!")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("🔧 Make sure all files are in the correct locations")

if __name__ == "__main__":
    main()
