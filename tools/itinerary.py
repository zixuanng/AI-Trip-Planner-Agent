"""
Itinerary Generator - Uses Groq LLM API to create AI-powered trip itineraries
Free tier API key provided by user
"""
import os
from typing import Dict, Any, List, Optional
from groq import Groq
import config


def generate_itinerary(
    destination: str,
    start_date: str,
    end_date: str,
    travelers: int,
    budget: float,
    currency: str,
    weather_data: List[Dict[str, Any]],
    preferences: Optional[List[str]] = None
) -> str:
    """
    Generate a comprehensive trip itinerary using Groq LLM.
    
    Args:
        destination: Destination city/country
        start_date: Trip start date (YYYY-MM-DD)
        end_date: Trip end date (YYYY-MM-DD)
        travelers: Number of travelers
        budget: Total budget
        currency: Currency code
        weather_data: Weather forecast data
        preferences: List of travel preferences
    
    Returns:
        Generated itinerary as string
    """
    client = Groq(api_key=config.GROQ_API_KEY)
    
    # Format weather data for the prompt
    weather_summary = _format_weather_for_prompt(weather_data)
    
    # Build preferences string
    pref_str = ", ".join(preferences) if preferences else "general sightseeing, local culture, good food"
    
    # Calculate trip duration
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end - start).days + 1
    except ValueError:
        num_days = 7  # Default to 7 days
    
    # Create the prompt
    prompt = f"""You are an expert travel planner. Create a detailed {num_days}-day trip itinerary for {destination}.

TRIP DETAILS:
- Destination: {destination}
- Duration: {num_days} days ({start_date} to {end_date})
- Travelers: {travelers} person(s)
- Total Budget: {currency} {budget:.2f}
- Travel Style: {pref_str}

WEATHER FORECAST:
{weather_summary}

Please create a comprehensive itinerary that includes:
1. Day-by-day schedule with morning, afternoon, and evening activities
2. Specific attractions, restaurants, and activities appropriate for the weather
3. Estimated costs for each activity in {currency}
4. Practical tips (best time to visit, transportation, etc.)
5. Local food recommendations

Format the output with clear headings for each day. Make it practical and realistic."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledgeable travel planner who creates detailed, practical, and exciting trip itineraries. Always consider weather conditions when recommending activities."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000,
            top_p=0.9,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating itinerary: {str(e)}\n\nPlease try again or adjust your trip parameters."


def _format_weather_for_prompt(weather_data: List[Dict[str, Any]]) -> str:
    """Format weather data for the LLM prompt."""
    if not weather_data or "error" in weather_data[0]:
        return "Weather data not available"
    
    summary = ""
    for day in weather_data[:7]:  # Use first 7 days
        summary += f"- {day['date']}: {day['weather_description']}, "
        summary += f"{day['temperature_min']:.0f}°C to {day['temperature_max']:.0f}°C, "
        summary += f"{day['precipitation_probability']}% chance of rain\n"
    
    return summary


def generate_quick_tips(destination: str, weather_data: List[Dict[str, Any]]) -> str:
    """
    Generate quick travel tips for a destination.
    
    Args:
        destination: Destination city/country
        weather_data: Weather forecast data
    
    Returns:
        Travel tips as string
    """
    client = Groq(api_key=config.GROQ_API_KEY)
    
    # Check if it's likely to rain
    rainy_days = sum(1 for day in weather_data if day.get("precipitation_probability", 0) > 50)
    weather_tip = "Expect some rain" if rainy_days > 2 else "Generally good weather expected"
    
    prompt = f"""Give me 5 essential travel tips for visiting {destination}. 
Current weather outlook: {weather_tip}.
Keep it concise and practical. Each tip should be 1-2 sentences."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful travel advisor. Provide practical, concise travel tips."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating tips: {str(e)}"


def format_itinerary_summary(itinerary: str, total_cost: float, currency: str) -> str:
    """Format itinerary with a header and cost summary."""
    header = f"""
🌍 **AI-Generated Trip Itinerary**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 **Estimated Total Cost:** {currency} {total_cost:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    return header + itinerary
