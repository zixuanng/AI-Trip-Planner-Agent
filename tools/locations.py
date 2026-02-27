"""
Location Search Tool - Searches locations using OpenStreetMap Nominatim API
Free API, no authentication required (requires respectful usage)
"""
import requests
from typing import List, Dict, Any
import time
import config


def search_locations(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search for locations using OpenStreetMap Nominatim.
    
    Args:
        query: Search query (city name, address, etc.)
        limit: Maximum number of results
    
    Returns:
        List of location results with coordinates
    """
    # Nominatim requires a User-Agent header
    headers = {
        "User-Agent": "AI-Trip-Planner/1.0 (Educational Project)"
    }
    
    params = {
        "q": query,
        "format": "json",
        "limit": limit,
        "addressdetails": 1
    }
    
    try:
        # Rate limiting: Nominatim requires max 1 request per second
        time.sleep(1)
        
        response = requests.get(
            config.NOMINATIM_URL, 
            params=params, 
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        locations = []
        for item in data:
            locations.append({
                "name": item.get("display_name", "").split(",")[0],
                "full_name": item.get("display_name", ""),
                "lat": float(item.get("lat", 0)),
                "lon": float(item.get("lon", 0)),
                "type": item.get("type", "unknown"),
                "country": item.get("address", {}).get("country", ""),
                "city": item.get("address", {}).get("city", 
                         item.get("address", {}).get("town", 
                         item.get("address", {}).get("village", ""))),
                "country_code": item.get("address", {}).get("country_code", "").upper()
            })
        
        return locations
    except requests.RequestException as e:
        return [{"error": f"Failed to search locations: {str(e)}"}]


def format_location_choice(locations: List[Dict[str, Any]]) -> str:
    """Format location results for display."""
    if not locations:
        return "No locations found"
    
    if "error" in locations[0]:
        return f"Error: {locations[0]['error']}"
    
    result = "📍 **Search Results:**\n\n"
    for i, loc in enumerate(locations, 1):
        result += f"**{i}. {loc['name']}**\n"
        result += f"   📍 {loc['full_name'][:80]}...\n"
        result += f"   🌍 Type: {loc['type']} | Country: {loc['country']}\n"
        result += f"   📌 Coordinates: {loc['lat']:.4f}, {loc['lon']:.4f}\n\n"
    
    return result


def get_location_details(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get reverse geocoding details for coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        Location details
    """
    headers = {
        "User-Agent": "AI-Trip-Planner/1.0 (Educational Project)"
    }
    
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    
    try:
        time.sleep(1)
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "display_name": data.get("display_name", ""),
            "type": data.get("type", "unknown"),
            "address": data.get("address", {})
        }
    except requests.RequestException as e:
        return {"error": f"Failed to get location details: {str(e)}"}
