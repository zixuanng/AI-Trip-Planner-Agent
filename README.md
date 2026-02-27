# AI Trip Planner Agent ✈️

An intelligent travel planning assistant that uses real-time data and AI to create comprehensive trip itineraries with weather forecasts, location recommendations, and expense calculations.

## Features

- **🌤️ Real-time Weather Forecasts** - Get 7-day weather predictions for any destination
- **📍 Location Search** - Search cities worldwide using OpenStreetMap
- **💰 Budget Calculator** - Calculate trip costs with currency conversion
- **🤖 AI Itinerary Generator** - Generate personalized day-by-day travel plans

## Free APIs Used

| Service   | API                     | Authentication   |
| --------- | ----------------------- | ---------------- |
| Weather   | Open-Meteo              | None required    |
| Locations | OpenStreetMap Nominatim | None required    |
| Currency  | Frankfurter.app         | None required    |
| AI        | Groq (Llama-3.1)        | API key included |

## Prerequisites

- Python 3.10 or higher
- Internet connection

## Installation

1. Navigate to the project directory:

```bash
cd ai-trip-planner
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit web application:

```bash
streamlit run app.py
# or
python -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Search Destination** - Enter a city name in the sidebar (e.g., "Tokyo", "Paris", "New York")
2. **Select Location** - Choose from the search results
3. **Set Trip Details** - Choose dates, budget, and travel preferences
4. **Get Weather** - Click "Get Weather Forecast" to see weather for your dates
5. **Calculate Cost** - Click "Calculate Trip Cost" for budget breakdown
6. **Generate Itinerary** - Click "Generate AI Itinerary" for a complete trip plan!

## Project Structure

```
ai-trip-planner/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── requirements.txt     # Python dependencies
├── SPEC.md              # Project specification
├── README.md            # This file
└── tools/
    ├── __init__.py
    ├── weather.py       # Weather API tool
    ├── locations.py     # Location search tool
    ├── expenses.py      # Currency conversion tool
    └── itinerary.py    # AI itinerary generator
```

## Configuration

The Groq API key is pre-configured in [`config.py`](config.py:7). You can modify:

- `GROQ_API_KEY` - Your own Groq API key if needed
- `SUPPORTED_CURRENCIES` - Add more currencies
- Default budget and traveler settings

## Notes

- Nominatim API has a rate limit of 1 request per second - the code includes delays to respect this
- Exchange rates are cached for 24 hours to minimize API calls
- The AI generates itineraries based on weather conditions and your preferences
