"""
Expense Calculator Tool - Currency conversion using Frankfurter API
Free API, no authentication required
"""
import requests
import time as time_module
from typing import Dict, Any, Optional
import config


# Cache for exchange rates
_rates_cache: Dict[str, Dict[str, Any]] = {}


def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """
    Get exchange rate between two currencies.
    
    Args:
        from_currency: Source currency code (e.g., "USD")
        to_currency: Target currency code (e.g., "EUR")
    
    Returns:
        Exchange rate or None if failed
    """
    if from_currency == to_currency:
        return 1.0
    
    cache_key = f"{from_currency}_{to_currency}"
    
    # Check cache
    if cache_key in _rates_cache:
        cached_data = _rates_cache[cache_key]
        # Cache valid for 24 hours
        if cached_data.get("timestamp", 0) > (time_module.time() - 86400):
            return cached_data.get("rate")
    
    try:
        # Frankfurter supports base currency in URL
        url = f"{config.FRANKFURTER_URL}?from={from_currency}&to={to_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        rate = data.get("rates", {}).get(to_currency)
        
        if rate:
            # Cache the result
            _rates_cache[cache_key] = {
                "rate": rate,
                "timestamp": time_module.time()
            }
        
        return rate
    except requests.RequestException:
        return None


def convert_currency(amount: float, from_currency: str, to_currency: str) -> Optional[float]:
    """
    Convert amount from one currency to another.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
    
    Returns:
        Converted amount or None if failed
    """
    if from_currency == to_currency:
        return amount
    
    rate = get_exchange_rate(from_currency, to_currency)
    if rate:
        return amount * rate
    return None


def get_all_exchange_rates(base_currency: str = "USD") -> Dict[str, float]:
    """
    Get all exchange rates for a base currency.
    
    Args:
        base_currency: Base currency code
    
    Returns:
        Dictionary of currency codes to exchange rates
    """
    try:
        url = f"{config.FRANKFURTER_URL}?from={base_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("rates", {})
    except requests.RequestException:
        return {}


def estimate_trip_cost(
    daily_budget: float,
    num_days: int,
    num_travelers: int,
    currency: str,
    destination_currency: Optional[str] = None
) -> Dict[str, Any]:
    """
    Estimate total trip cost with optional currency conversion.
    
    Args:
        daily_budget: Budget per person per day
        num_days: Number of days
        num_travelers: Number of travelers
        currency: Budget currency
        destination_currency: Destination country currency (optional)
    
    Returns:
        Cost breakdown dictionary
    """
    total_budget = daily_budget * num_days * num_travelers
    
    result = {
        "daily_budget_per_person": daily_budget,
        "num_days": num_days,
        "num_travelers": num_travelers,
        "total_budget": total_budget,
        "currency": currency,
        "daily_breakdown": {
            "accommodation": daily_budget * 0.4,
            "food": daily_budget * 0.25,
            "activities": daily_budget * 0.2,
            "transportation": daily_budget * 0.1,
            "miscellaneous": daily_budget * 0.05
        }
    }
    
    # Convert to destination currency if different
    if destination_currency and destination_currency != currency:
        converted_total = convert_currency(total_budget, currency, destination_currency)
        if converted_total:
            result["converted_total"] = converted_total
            result["destination_currency"] = destination_currency
            
            # Convert daily breakdown
            result["converted_daily_breakdown"] = {}
            for category, amount in result["daily_breakdown"].items():
                converted = convert_currency(amount, currency, destination_currency)
                if converted:
                    result["converted_daily_breakdown"][category] = converted
    
    return result


def format_cost_summary(cost_data: Dict[str, Any]) -> str:
    """Format cost data into a readable summary."""
    if "error" in cost_data:
        return f"Error: {cost_data['error']}"
    
    currency = cost_data.get("currency", "USD")
    result = f"💰 **Trip Cost Estimate ({currency})**\n\n"
    
    result += f"👥 Travelers: {cost_data['num_travelers']}\n"
    result += f"📅 Duration: {cost_data['num_days']} days\n"
    result += f"💵 Daily budget per person: {currency} {cost_data['daily_budget_per_person']:.2f}\n\n"
    
    result += "**Daily Breakdown:**\n"
    breakdown = cost_data.get("daily_breakdown", {})
    for category, amount in breakdown.items():
        result += f"  • {category.capitalize()}: {currency} {amount:.2f}\n"
    
    result += f"\n**💵 Total Budget: {currency} {cost_data['total_budget']:.2f}**\n"
    
    if "converted_total" in cost_data:
        dest_currency = cost_data.get("destination_currency", "")
        result += f"\n**Equivalent in {dest_currency}: {dest_currency} {cost_data['converted_total']:.2f}**\n"
    
    return result
