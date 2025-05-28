import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IthacaWeatherDashboard:
    def __init__(self, db_path="data/weather.db"):
        self.db_path = db_path
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
    
    def get_weather_data(self, hours=24):
        """Get weather data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            since = datetime.now() - timedelta(hours=hours)
            query = '''
                SELECT * FROM weather_data 
                WHERE timestamp > ? 
                ORDER BY timestamp DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=[since])
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
        except Exception as e:
            print(f"Error reading database: {e}")
            return pd.DataFrame()
    
    def get_latest_conditions(self):
        """Get the most recent weather conditions for all locations"""
        df = self.get_weather_data(hours=1)
        if df.empty:
            return {}
        
        latest_data = {}
        for location in df['location'].unique():
            location_data = df[df['location'] == location].iloc[0]
            latest_data[location] = {
                'temperature': location_data.get('temperature', 'N/A'),
                'feels_like': location_data.get('feels_like', 'N/A'),
                'condition': location_data.get('weather_condition', 'N/A'),
                'humidity': location_data.get('humidity', 'N/A'),
                'wind_speed': location_data.get('wind_speed', 'N/A'),
                'timestamp': location_data.get('timestamp', 'N/A')
            }
        
        return latest_data
    
    def create_temperature_chart(self, hours=24):
        """Create temperature comparison chart"""
        df = self.get_weather_data(hours=hours)
        
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available. Run the scraper first!",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False, font_size=16
            )
        
        fig = px.line(df, x='timestamp', y='temperature', 
                     color='location', 
                     title=f'Temperature Trends - Last {hours} Hours',
                     labels={'temperature': 'Temperature (°F)', 'timestamp': 'Time'})
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def create_conditions_chart(self):
        """Create current conditions comparison"""
        latest = self.get_latest_conditions()
        
        if not latest:
            return go.Figure().add_annotation(
                text="No current data available",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False, font_size=16
            )
        
        locations = list(latest.keys())
        temperatures = [latest[loc]['temperature'] for loc in locations]
        feels_like = [latest[loc]['feels_like'] for loc in locations]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Actual Temperature',
            x=locations,
            y=temperatures,
            text=[f"{temp}°F" for temp in temperatures],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            name='Feels Like',
            x=locations,
            y=feels_like,
            text=[f"{temp}°F" for temp in feels_like],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Current Temperature Comparison Across Ithaca',
            yaxis_title='Temperature (°F)',
            barmode='group',
            height=400
        )
        
        return fig
    
    def create_weather_variance_chart(self, hours=24):
        """Create weather variance analysis"""
        df = self.get_weather_data(hours=hours)
        
        if df.empty:
            return go.Figure().add_annotation(
                text="No data for variance analysis",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False, font_size=16
            )
        
        # Calculate temperature variance by hour
        df['hour'] = df['timestamp'].dt.floor('h')
        variance_data = df.groupby('hour')['temperature'].agg(['min', 'max', 'std']).reset_index()
        variance_data['range'] = variance_data['max'] - variance_data['min']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=variance_data['hour'],
            y=variance_data['range'],
            mode='lines+markers',
            name='Temperature Range',
            line=dict(color='red', width=3)
        ))
        
        fig.update_layout(
            title='Ithaca Weather Unpredictability Index',
            xaxis_title='Time',
            yaxis_title='Temperature Range Across Locations (°F)',
            height=300
        )
        
        return fig
    
    def setup_layout(self):
        """Setup the dashboard layout"""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("Ithaca Weather Intelligence Dashboard", 
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
                html.P("Because Ithaca weather is beautifully unpredictable", 
                      style={'textAlign': 'center', 'color': '#7f8c8d', 'fontStyle': 'italic'}),
                html.Hr()
            ]),
            
            # Current conditions cards
            html.Div(id='current-conditions', style={'marginBottom': '30px'}),
            
            # Time range selector
            html.Div([
                html.Label("Select Time Range:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='time-range-dropdown',
                    options=[
                        {'label': 'Last 6 Hours', 'value': 6},
                        {'label': 'Last 24 Hours', 'value': 24},
                        {'label': 'Last 3 Days', 'value': 72},
                        {'label': 'Last Week', 'value': 168}
                    ],
                    value=24,
                    style={'width': '200px'}
                )
            ], style={'marginBottom': '20px'}),
            
            # Charts
            html.Div([
                dcc.Graph(id='temperature-chart'),
                dcc.Graph(id='conditions-chart'),
                dcc.Graph(id='variance-chart')
            ]),
            
            # Auto-refresh
            dcc.Interval(
                id='interval-component',
                interval=5*60*1000,  # Update every 5 minutes
                n_intervals=0
            ),
            
            # Footer
            html.Div([
                html.Hr(),
                html.P([
                    "Data collected from Downtown Ithaca, Cornell Campus, Ithaca College, and Cayuga Lake | ",
                    html.A("View on GitHub", href="https://github.com/kpeis695/ithaca-weather-dashboard", 
                          target="_blank")
                ], style={'textAlign': 'center', 'color': '#95a5a6', 'fontSize': '12px'})
            ])
        ], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})
    
    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        
        @self.app.callback(
            [Output('current-conditions', 'children'),
             Output('temperature-chart', 'figure'),
             Output('conditions-chart', 'figure'),
             Output('variance-chart', 'figure')],
            [Input('interval-component', 'n_intervals'),
             Input('time-range-dropdown', 'value')]
        )
        def update_dashboard(n, hours):
            # Current conditions cards
            latest = self.get_latest_conditions()
            cards = []
            
            for location, data in latest.items():
                card = html.Div([
                    html.H4(location, style={'margin': '0', 'color': '#2c3e50'}),
                    html.H2(f"{data['temperature']}°F", 
                           style={'margin': '5px 0', 'color': '#e74c3c'}),
                    html.P(f"Feels like {data['feels_like']}°F", 
                          style={'margin': '0', 'color': '#7f8c8d'}),
                    html.P(data['condition'], 
                          style={'margin': '0', 'fontWeight': 'bold', 'color': '#34495e'}),
                    html.P(f"Humidity: {data['humidity']}% | Wind: {data['wind_speed']} mph", 
                          style={'margin': '5px 0 0 0', 'fontSize': '12px', 'color': '#95a5a6'})
                ], style={
                    'backgroundColor': '#f8f9fa',
                    'padding': '15px',
                    'borderRadius': '8px',
                    'textAlign': 'center',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'margin': '10px'
                })
                cards.append(card)
            
            conditions_div = html.Div(cards, style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'flexWrap': 'wrap'
            }) if cards else html.Div("No current data available")
            
            # Charts
            temp_chart = self.create_temperature_chart(hours)
            conditions_chart = self.create_conditions_chart()
            variance_chart = self.create_weather_variance_chart(hours)
            
            return conditions_div, temp_chart, conditions_chart, variance_chart
    
    def run(self, debug=True, port=8050):
        """Run the dashboard"""
        print(f"🌤️ Starting Ithaca Weather Dashboard...")
        print(f"📊 Dashboard will be available at: http://localhost:{port}")
        print(f"🔄 Data updates every 5 minutes")
        self.app.run(debug=debug, port=port)

if __name__ == "__main__":
    dashboard = IthacaWeatherDashboard()
    dashboard.run()
