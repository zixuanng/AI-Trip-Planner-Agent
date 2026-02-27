"""
Configuration settings for AI Trip Planner Agent
"""
import os

# Groq API Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# API Endpoints
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
FRANKFURTER_URL = "https://api.frankfurter.app/latest"

# Supported currencies
SUPPORTED_CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", 
    "INR", "KRW", "SGD", "HKD", "MXN", "BRL", "NZD", "SEK",
    "NOK", "DKK", "PLN", "THB", "MYR", "PHP", "IDR", "VND"
]

# Weather code descriptions (WMO Weather interpretation codes)
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

# Default trip preferences
DEFAULT_TRAVELERS = 2
DEFAULT_DAILY_BUDGET = 100
