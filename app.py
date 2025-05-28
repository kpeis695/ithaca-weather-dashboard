from src.dashboard import IthacaWeatherDashboard
import os

# Create dashboard instance
dashboard = IthacaWeatherDashboard()

# This is what Render will run
server = dashboard.app.server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    dashboard.app.run(host="0.0.0.0", port=port, debug=False)
