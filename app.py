import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dashboard import IthacaWeatherDashboard

# Create dashboard instance
dashboard = IthacaWeatherDashboard()

# This is what Render will run
server = dashboard.app.server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    dashboard.app.run(host="0.0.0.0", port=port, debug=False)
