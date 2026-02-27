"""
Weather Tool - Fetches real-time weather data from Open-Meteo API
Free API, no authentication required
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import config


def get_weather_forecast(lat: float, lon: float, days: int = 7) -> List[Dict[str, Any]]:
    """
    Fetch weather forecast for given coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        days: Number of days to forecast (max 16)
    
    Returns:
        List of daily weather data
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": min(days, 16)
    }
    
    try:
        response = requests.get(config.OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        daily_data = data.get("daily", {})
        dates = daily_data.get("time", [])
        weather_list = []
        
        for i, date in enumerate(dates):
            weather_code = daily_data.get("weather_code", [0])[i]
            weather_list.append({
                "date": date,
                "temperature_max": daily_data.get("temperature_2m_max", [0])[i],
                "temperature_min": daily_data.get("temperature_2m_min", [0])[i],
                "weather_code": weather_code,
                "weather_description": config.WEATHER_CODES.get(weather_code, "Unknown"),
                "precipitation_probability": daily_data.get("precipitation_probability_max", [0])[i]
            })
        
        return weather_list
    except requests.RequestException as e:
        return [{"error": f"Failed to fetch weather: {str(e)}"}]


def get_weather_icon(weather_code: int) -> str:
    """Get weather icon based on WMO weather code."""
    icons = {
        0: "☀️",   # Clear sky
        1: "🌤️",  # Mainly clear
        2: "⛅",   # Partly cloudy
        3: "☁️",   # Overcast
        45: "🌫️", # Fog
        48: "🌫️", # Depositing rime fog
        51: "🌧️", # Light drizzle
        53: "🌧️", # Moderate drizzle
        55: "🌧️", # Dense drizzle
        61: "🌧️", # Slight rain
        63: "🌧️", # Moderate rain
        65: "🌧️", # Heavy rain
        71: "🌨️", # Slight snow
        73: "🌨️", # Moderate snow
        75: "❄️",  # Heavy snow
        80: "🌦️", # Rain showers
        81: "🌦️", # Moderate rain showers
        82: "⛈️", # Violent rain showers
        95: "⛈️", # Thunderstorm
        96: "⛈️", # Thunderstorm with hail
        99: "⛈️", # Thunderstorm with heavy hail
    }
    return icons.get(weather_code, "🌡️")


def format_weather_summary(weather_data: List[Dict[str, Any]]) -> str:
    """Format weather data into a readable summary."""
    if not weather_data or "error" in weather_data[0]:
        return "Unable to fetch weather data"
    
    summary = "📅 **Weather Forecast:**\n\n"
    for day in weather_data:
        icon = get_weather_icon(day["weather_code"])
        summary += f"{icon} **{day['date']}**: {day['weather_description']}\n"
        summary += f"   🌡️ Temp: {day['temperature_min']:.1f}°C - {day['temperature_max']:.1f}°C\n"
        summary += f"   💧 Rain: {day['precipitation_probability']}%\n\n"
    
    return summary
