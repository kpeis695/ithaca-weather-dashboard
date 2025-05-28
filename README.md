# ithaca-weather-dashboard
Interactive weather analytics dashboard tracking Ithaca's unpredictable weather patterns


# Ithaca Weather Intelligence Dashboard

> *"Because Ithaca weather is beautifully unpredictable"*

An interactive weather analytics platform that tracks and analyzes the famously erratic weather patterns of Ithaca, New York. Built to help locals better understand and prepare for the region's unique microclimate variations.

## The Story

Living in Ithaca, you quickly learn that weather forecasts are more like suggestions. One moment it's sunny and 70°F, the next it's snowing sideways. This project was born from countless mornings of being caught unprepared by Ithaca's weather mood swings.

Rather than just checking another weather app, I built this dashboard to analyze **why** Ithaca weather is so unpredictable and **when** those changes are most likely to happen.

## Features

### Current Implementation
- **Multi-Location Tracking**: Downtown Ithaca, Cornell Campus, Ithaca College, and Cayuga Lake
- **Real-Time Data Collection**: Automated weather data scraping every 30 minutes
- **Historical Analysis**: SQLite database storing comprehensive weather metrics
- **API Integration**: OpenWeatherMap API with rate limiting and error handling

### Coming Soon
- Interactive dashboard with weather volatility metrics
- "Should I bring a jacket?" predictive model
- Lake effect analysis showing Cayuga Lake's influence
- Seasonal unpredictability scoring
- Weather change alert system

## Technical Stack

- **Backend**: Python, SQLite, OpenWeatherMap API
- **Data Processing**: Pandas, NumPy for analytics
- **Visualization**: Plotly, Dash for interactive dashboards
- **Automation**: Scheduled data collection with error handling
- **Database**: SQLite with optimized schema for time-series data

## Data Points Tracked

Each location captures:
- Temperature & "feels like" temperature
- Humidity, pressure, and visibility
- Wind speed and direction
- Cloud coverage and weather conditions
- Sunrise/sunset times
- Raw API data for future analysis

## Quick Start

### Prerequisites
- Python 3.8+
- OpenWeatherMap API key (free tier: 1000 calls/day)

### Setup
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.template` to `.env` and add your API key
4. Run the scraper: `python src/scraper.py`

### Get Your API Key
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Navigate to API Keys section
3. Copy your key to the `.env` file

## Project Structure

```
ithaca-weather-dashboard/
├── src/
│   ├── scraper.py          # Weather data collection
│   ├── dashboard.py        # Interactive web dashboard (coming soon)
│   └── analytics.py        # Weather pattern analysis (coming soon)
├── config/
│   └── config.py          # Configuration management
├── data/
│   └── weather.db         # SQLite database (generated)
├── requirements.txt       # Python dependencies
├── .env.template         # Environment variables template
└── README.md            # You are here!
```

## Why This Project?

This project demonstrates several key technical skills:

- **API Integration**: Robust handling of external APIs with rate limiting
- **Database Design**: Efficient time-series data storage and retrieval
- **Data Pipeline**: Automated data collection and processing
- **Error Handling**: Graceful handling of network and API failures
- **Configuration Management**: Secure handling of API keys and settings
- **Code Organization**: Clean, modular Python architecture

## Local Weather Insights

Ithaca's unique geography creates fascinating weather patterns:

- **Gorge Effect**: Temperature variations between valley and hills
- **Lake Influence**: Cayuga Lake's moderating effect on temperatures
- **Elevation Changes**: Campus elevations create microclimates
- **Seasonal Volatility**: Spring and fall bring the most unpredictable conditions

## Upcoming Analytics Features

- **Weather Volatility Index**: Quantify daily weather unpredictability
- **Campus Comparison**: Temperature differences between Cornell, IC, and downtown
- **Seasonal Patterns**: Historical analysis of weather trend reliability
- **Prediction Accuracy**: How often do forecasts match reality in Ithaca?

## Contributing

This is a personal project, but I'm open to suggestions! If you're also an Ithaca weather survivor with ideas for interesting analytics, feel free to open an issue.

## License

MIT License - Feel free to adapt this for your own unpredictable weather location!

## Connect

Built by [Your Name] - [Your LinkedIn] | [Your Portfolio]

*Making sense of Ithaca weather, one data point at a time*

---

**Next Steps**: Currently building the interactive dashboard and weather pattern analytics. Check back soon for live demo!
