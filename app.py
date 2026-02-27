"""
AI Trip Planner Agent - Enhanced Streamlit Application
A system that uses tools to fetch real-time weather, search locations, 
calculate expenses, and create itineraries using AI.
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import time
import config
from tools import (
    search_locations,
    get_weather_forecast,
    estimate_trip_cost,
    generate_itinerary,
    generate_quick_tips,
    get_weather_icon
)


# ============================================
# CUSTOM CSS - Modern Travel Theme
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main Theme */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0F4C75 0%, #3282B8 50%, #BBE1FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #0F4C75;
        padding: 0.75rem 1rem;
        background: linear-gradient(90deg, #e8f4fc 0%, #ffffff 100%);
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #3282B8;
    }
    
    /* Cards */
    .trip-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.25rem;
        border-radius: 16px;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 0.75rem 0;
        transition: all 0.3s ease;
    }
    
    .trip-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Weather Cards */
    .weather-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0f7ff 100%);
        padding: 1rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(50, 130, 184, 0.15);
        transition: all 0.3s ease;
    }
    
    .weather-card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(50, 130, 184, 0.25);
    }
    
    .weather-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .weather-date {
        font-weight: 600;
        color: #0F4C75;
        font-size: 0.9rem;
    }
    
    .weather-temp {
        font-size: 1.4rem;
        font-weight: 700;
        color: #3282B8;
    }
    
    .weather-desc {
        font-size: 0.8rem;
        color: #6c757d;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0F4C75 0%, #3282B8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(15, 76, 117, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3282B8 0%, #0F4C75 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(15, 76, 117, 0.4);
    }
    
    .stButton > button:disabled {
        background: #e9ecef;
        color: #adb5bd;
        box-shadow: none;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 1px solid #dee2e6;
    }
    
    [data-testid="stSidebar"] .stTitle {
        color: #0F4C75;
        font-weight: 700;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #3282B8;
        box-shadow: 0 0 0 3px rgba(50, 130, 184, 0.15);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F4C75;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #6c757d;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0F4C75 0%, #3282B8 100%);
        color: white;
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #3282B8;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    
    /* Itinerary Styling */
    .itinerary-day {
        background: white;
        padding: 1.25rem;
        border-radius: 16px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .itinerary-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F4C75;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e8f4fc;
        margin-bottom: 0.75rem;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3282B8, transparent);
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading-text {
        animation: pulse 1.5s infinite;
        color: #3282B8;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .section-header {
            font-size: 1.2rem;
        }
        
        .weather-card {
            padding: 0.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# Page configuration
st.set_page_config(
    page_title="AI Trip Planner ✈️",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize Streamlit session state variables."""
    defaults = {
        'destination_selected': False,
        'location_data': None,
        'weather_data': None,
        'itinerary': None,
        'trip_cost': None,
        'search_performed': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_header():
    """Render the main header."""
    st.markdown("""
    <p class="main-header">✈️ AI Trip Planner Agent</p>
    <p class="subtitle">Plan your perfect trip with real-time weather, AI-powered itineraries & smart budget estimates</p>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the enhanced sidebar with trip configuration."""
    with st.sidebar:
        # Logo/Title
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 3rem;">🌍</span>
            <h2 style="color: #0F4C75; margin: 0.5rem 0;">Trip Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Destination Search Section
        st.markdown("### 🔍 Find Destination")
        
        search_query = st.text_input(
            "Search for a city",
            placeholder="e.g., Tokyo, Paris, New York",
            help="Enter a city name to search",
            key="search_input"
        )
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            search_button = st.button("🔍 Search", use_container_width=True, key="search_btn")
        with col_btn2:
            clear_button = st.button("🗑️", help="Clear selection", key="clear_btn")
        
        if clear_button:
            st.session_state.destination_selected = False
            st.session_state.location_data = None
            st.session_state.weather_data = None
            st.session_state.itinerary = None
            st.session_state.trip_cost = None
            st.rerun()
        
        selected_location = None
        
        if search_button and search_query:
            with st.spinner("🔎 Searching locations..."):
                locations = search_locations(search_query, limit=5)
            
            st.session_state.search_performed = True
            
            if locations and "error" not in locations[0]:
                location_options = [f"📍 {loc['name']}, {loc['country']}" for loc in locations]
                selected_idx = st.selectbox(
                    "Select your destination",
                    range(len(locations)),
                    format_func=lambda i: location_options[i],
                    key="location_select"
                )
                selected_location = locations[selected_idx]
                st.session_state.location_data = selected_location
                st.session_state.destination_selected = True
            else:
                st.error("❌ No locations found. Try a different search term.")
        
        # Show selected destination
        if st.session_state.destination_selected and st.session_state.location_data:
            loc = st.session_state.location_data
            st.markdown(f"""
            <div class="success-box">
                <strong>✅ Selected:</strong><br>
                📍 {loc['name']}, {loc['country']}<br>
                <small>📌 {loc['lat']:.4f}, {loc['lon']:.4f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Trip Dates Section
        st.markdown("### 📅 Trip Details")
        
        today = datetime.now().date()
        
        start_date = st.date_input(
            "🗓️ Start Date",
            min_value=today,
            value=today + timedelta(days=7),
            help="Select your trip start date"
        )
        
        end_date = st.date_input(
            "🗓️ End Date",
            min_value=start_date,
            value=start_date + timedelta(days=7),
            help="Select your trip end date"
        )
        
        # Calculate and display trip duration
        num_days = (end_date - start_date).days + 1
        
        st.markdown(f"""
        <div class="info-box">
            <strong>📆 Duration:</strong> {num_days} day{"s" if num_days != 1 else ""}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Budget Section
        st.markdown("### 💰 Budget")
        
        col1, col2 = st.columns(2)
        with col1:
            currency = st.selectbox(
                "💵 Currency",
                config.SUPPORTED_CURRENCIES,
                index=0,
                key="currency_select"
            )
        with col2:
            daily_budget = st.number_input(
                "Daily Budget",
                min_value=10,
                value=100,
                step=10,
                key="daily_budget"
            )
        
        travelers = st.slider(
            "👥 Travelers",
            min_value=1,
            max_value=20,
            value=2,
            help="Number of people traveling"
        )
        
        st.markdown("---")
        
        # Preferences Section
        st.markdown("### 🎯 Travel Style")
        
        preferences = st.multiselect(
            "What interests you?",
            ["Adventure 🧗", "Relaxation 🧖", "Culture 🏛️", "Food & Cuisine 🍜", 
             "Nature 🌲", "Nightlife 🌃", "Shopping 🛍️", "History 📜"],
            default=["Culture 🏛️", "Food & Cuisine 🍜"],
            key="preferences_select"
        )
        
        # Clean preferences list
        clean_prefs = [p.split(" ")[0] for p in preferences]
        
        st.markdown("---")
        
        # Action Button
        st.markdown("### 🚀 Generate Trip")
        generate_full = st.button("✨ Generate Complete Plan", use_container_width=True, key="generate_full")
        
        return {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "num_days": num_days,
            "currency": currency,
            "daily_budget": daily_budget,
            "travelers": travelers,
            "preferences": clean_prefs,
            "generate_full": generate_full
        }


def render_weather_section(weather_data: List[Dict[str, Any]]):
    """Render the enhanced weather forecast section."""
    if not weather_data or "error" in weather_data[0]:
        st.warning("⚠️ Unable to fetch weather data")
        return
    
    st.markdown('<p class="section-header">🌤️ Weather Forecast</p>', unsafe_allow_html=True)
    
    # Weather cards in a scrollable row
    cols = st.columns(min(len(weather_data), 7))
    
    for i, day in enumerate(weather_data[:7]):
        with cols[i]:
            icon = get_weather_icon(day["weather_code"])
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            day_name = date_obj.strftime("%a")
            
            st.markdown(f"""
            <div class="weather-card">
                <div class="weather-date">{day_name}<br>{day['date'][5:]}</div>
                <div class="weather-icon">{icon}</div>
                <div class="weather-temp">{day['temperature_max']:.0f}° / {day['temperature_min']:.0f}°</div>
                <div class="weather-desc">{day['weather_description']}</div>
                <div class="weather-desc">💧 {day['precipitation_probability']}%</div>
            </div>
            """, unsafe_allow_html=True)


def render_cost_section(cost_data: Dict[str, Any]):
    """Render the enhanced cost estimate section."""
    st.markdown('<p class="section-header">💰 Budget Breakdown</p>', unsafe_allow_html=True)
    
    if "error" in cost_data:
        st.warning(f"⚠️ {cost_data['error']}")
        return
    
    # Main metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Daily Budget",
            f"{cost_data['currency']} {cost_data['daily_budget_per_person']:,.0f}",
            delta="Per person"
        )
    with col2:
        st.metric(
            "Total Budget",
            f"{cost_data['currency']} {cost_data['total_budget']:,.0f}",
            delta=f"{cost_data['num_days']} days × {cost_data['num_travelers']} travelers"
        )
    with col3:
        if "converted_total" in cost_data:
            st.metric(
                f"💱 In {cost_data['destination_currency']}",
                f"{cost_data['destination_currency']} {cost_data['converted_total']:,.0f}"
            )
        else:
            st.metric("Per Day", f"{cost_data['currency']} {cost_data['total_budget'] // cost_data['num_days']:,.0f}")
    
    st.markdown("### 📊 Daily Cost Distribution")
    
    # Cost breakdown visualization
    breakdown = cost_data.get("daily_breakdown", {})
    
    categories = {
        "🏨 Accommodation": breakdown.get("accommodation", 0),
        "🍽️ Food & Dining": breakdown.get("food", 0),
        "🎫 Activities": breakdown.get("activities", 0),
        "🚗 Transportation": breakdown.get("transportation", 0),
        "🎁 Miscellaneous": breakdown.get("miscellaneous", 0)
    }
    
    # Progress bars
    total = sum(categories.values())
    for cat, amount in categories.items():
        if total > 0:
            percentage = (amount / cost_data['daily_budget_per_person']) * 100
            st.progress(min(percentage / 100, 1.0), text=f"{cat}: {cost_data['currency']} {amount:.0f}")
    
    # Category Distribution with custom styling
    st.markdown("### 🥧 Category Distribution")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        # Create visually appealing horizontal bar chart
        # Use a color palette with good contrast
        colors = {
            '🏨 Accommodation': '#0F4C75',  # Deep blue
            '🍽️ Food & Dining': '#FF6B6B',   # Coral
            '🎫 Activities': '#4ECDC4',       # Teal
            '🚗 Transportation': '#FFE66D',   # Yellow
            '🎁 Miscellaneous': '#95E1D3'     # Mint
        }
        
        # Custom styled bars for each category
        max_amount = max(categories.values())
        
        for category, amount in categories.items():
            bar_color = colors.get(category, '#3282B8')
            percentage = (amount / max_amount) * 100 if max_amount > 0 else 0
            
            st.markdown(f"""
            <div style="margin: 12px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-weight: 500; color: #0F4C75;">{category}</span>
                    <span style="font-weight: 600; color: #3282B8;">{cost_data['currency']} {amount:.2f}</span>
                </div>
                <div style="background: #e9ecef; border-radius: 10px; height: 28px; overflow: hidden;">
                    <div style="
                        background: linear-gradient(90deg, {bar_color}, {bar_color}dd); 
                        width: {percentage}%; 
                        height: 100%; 
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        padding-left: 12px;
                        box-shadow: 2px 0 8px rgba(0,0,0,0.1);
                    ">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_chart2:
        # Summary card
        st.markdown(f"""
        <div class="trip-card" style="text-align: center; padding: 1.5rem;">
            <h4 style="color: #0F4C75; margin: 0 0 1rem 0;">💵 Budget Summary</h4>
            <div style="font-size: 1.8rem; font-weight: 700; color: #3282B8; margin: 0.5rem 0;">
                {cost_data['currency']} {cost_data['daily_budget_per_person']:,.0f}
            </div>
            <p style="color: #6c757d; margin: 0;">per person / day</p>
            <hr style="margin: 1rem 0; border: none; border-top: 1px solid #e9ecef;">
            <div style="font-size: 1.4rem; font-weight: 700; color: #0F4C75; margin: 0.5rem 0;">
                {cost_data['currency']} {cost_data['total_budget']:,.0f}
            </div>
            <p style="color: #6c757d; margin: 0;">total trip cost</p>
        </div>
        """, unsafe_allow_html=True)


def render_itinerary_section(itinerary: str, total_cost: float, currency: str):
    """Render the enhanced itinerary section."""
    st.markdown('<p class="section-header">📋 Your AI-Generated Itinerary</p>', unsafe_allow_html=True)
    
    # Cost summary banner
    st.markdown(f"""
    <div class="success-box" style="font-size: 1.1rem;">
        💵 <strong>Estimated Total Cost:</strong> {currency} {total_cost:,.2f}
    </div>
    """, unsafe_allow_html=True)
    
    # Create expandable sections for the itinerary
    # Try to parse the itinerary into sections
    lines = itinerary.split('\n')
    current_section = []
    sections = []
    
    for line in lines:
        if line.strip().startswith('**') and ('Day' in line or 'day' in line):
            if current_section:
                sections.append('\n'.join(current_section))
            current_section = [line]
        else:
            current_section.append(line)
    
    if current_section:
        sections.append('\n'.join(current_section))
    
    # If we have parsed sections, display them with expanders
    if len(sections) > 1:
        for i, section in enumerate(sections[:7]):  # Show max 7 days
            with st.expander(f"📅 {section.split('**')[1] if '**' in section else f'Day {i+1}'}", expanded=(i==0)):
                st.markdown(section)
    else:
        # Display as-is if parsing fails
        st.markdown(itinerary)


def render_how_it_works():
    """Render the instructions when no destination is selected."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="trip-card" style="text-align: center;">
            <div style="font-size: 2.5rem;">🔍</div>
            <strong>1. Search</strong>
            <p style="color: #6c757d; font-size: 0.9rem;">Find your dream destination</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="trip-card" style="text-align: center;">
            <div style="font-size: 2.5rem;">📅</div>
            <strong>2. Plan</strong>
            <p style="color: #6c757d; font-size: 0.9rem;">Set dates & budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="trip-card" style="text-align: center;">
            <div style="font-size: 2.5rem;">🌤️</div>
            <strong>3. Check Weather</strong>
            <p style="color: #6c757d; font-size: 0.9rem;">See forecast for your trip</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="trip-card" style="text-align: center;">
            <div style="font-size: 2.5rem;">✨</div>
            <strong>4. Generate</strong>
            <p style="color: #6c757d; font-size: 0.9rem;">Get AI-powered itinerary</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Info
    st.markdown("""
    <div class="info-box">
        <strong>🔧 Free APIs Used:</strong><br>
        • 🌤️ <strong>Weather:</strong> Open-Meteo (no API key needed)<br>
        • 📍 <strong>Locations:</strong> OpenStreetMap Nominatim (no API key needed)<br>
        • 💱 <strong>Currency:</strong> Frankfurter.app (no API key needed)<br>
        • 🤖 <strong>AI:</strong> Groq Llama-3.1 (free tier)
    </div>
    """, unsafe_allow_html=True)


def render_info_panel(trip_config: dict):
    """Render the info panel on the right."""
    with st.container():
        st.markdown("""
        <div class="trip-card">
            <h4 style="color: #0F4C75; margin: 0 0 1rem 0;">📋 Trip Summary</h4>
        """, unsafe_allow_html=True)
        
        if st.session_state.destination_selected and st.session_state.location_data:
            loc = st.session_state.location_data
            st.markdown(f"""
            **📍 Destination:** {loc['name']}<br>
            **🌍 Country:** {loc['country']}<br>
            **📆 Dates:** {trip_config['start_date']} → {trip_config['end_date']}<br>
            **⏱️ Duration:** {trip_config['num_days']} day{"s" if trip_config['num_days'] != 1 else ""}<br>
            **👥 Travelers:** {trip_config['travelers']}<br>
            **💵 Budget:** {trip_config['currency']} {trip_config['daily_budget']}/day
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Quick tips button
            if st.button("💡 Get Travel Tips", use_container_width=True, key="tips_btn"):
                with st.spinner("Generating tips..."):
                    weather_data = st.session_state.get('weather_data', [])
                    tips = generate_quick_tips(f"{loc['name']}, {loc['country']}", weather_data if weather_data else [])
                    st.success(tips)
        else:
            st.info("👈 Start by searching for a destination!")
        
        st.markdown("</div>", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get configuration
    trip_config = render_sidebar()
    
    # Main content area
    col_main, col_info = st.columns([3, 1])
    
    with col_main:
        # Check if destination is selected
        if not st.session_state.destination_selected or not st.session_state.location_data:
            render_how_it_works()
            return
        
        # Display selected destination info
        loc = st.session_state.location_data
        
        # Individual action buttons in columns
        col_w, col_c, col_i = st.columns(3)
        
        with col_w:
            weather_btn = st.button("🌤️ Get Weather", use_container_width=True, key="weather_btn")
        with col_c:
            cost_btn = st.button("💰 Calculate Cost", use_container_width=True, key="cost_btn")
        with col_i:
            itinerary_btn = st.button("🤖 Generate Itinerary", use_container_width=True, key="itinerary_btn", disabled=not st.session_state.get('weather_data'))
        
        # Handle button clicks
        if weather_btn:
            with st.spinner("🌤️ Fetching weather data..."):
                st.session_state.weather_data = get_weather_forecast(
                    loc['lat'], 
                    loc['lon'], 
                    days=trip_config['num_days']
                )
        
        if cost_btn:
            with st.spinner("💰 Calculating trip costs..."):
                dest_currency = loc.get('country_code', 'USD')
                if dest_currency not in config.SUPPORTED_CURRENCIES:
                    dest_currency = trip_config['currency']
                
                st.session_state.trip_cost = estimate_trip_cost(
                    trip_config['daily_budget'],
                    trip_config['num_days'],
                    trip_config['travelers'],
                    trip_config['currency'],
                    dest_currency
                )
        
        if itinerary_btn:
            if not st.session_state.get('weather_data'):
                st.warning("⚠️ Please get weather forecast first!")
            else:
                with st.spinner("🤖 Generating your personalized itinerary..."):
                    total_budget = st.session_state.trip_cost['total_budget'] if st.session_state.trip_cost else trip_config['daily_budget'] * trip_config['num_days'] * trip_config['travelers']
                    
                    st.session_state.itinerary = generate_itinerary(
                        f"{loc['name']}, {loc['country']}",
                        trip_config['start_date'],
                        trip_config['end_date'],
                        trip_config['travelers'],
                        total_budget,
                        trip_config['currency'],
                        st.session_state.weather_data,
                        trip_config['preferences']
                    )
        
        st.markdown("---")
        
        # Display results
        if st.session_state.weather_data:
            render_weather_section(st.session_state.weather_data)
            st.markdown("---")
        
        if st.session_state.trip_cost:
            render_cost_section(st.session_state.trip_cost)
            st.markdown("---")
        
        if st.session_state.itinerary:
            total_cost = st.session_state.trip_cost['total_budget'] if st.session_state.trip_cost else trip_config['daily_budget'] * trip_config['num_days'] * trip_config['travelers']
            render_itinerary_section(st.session_state.itinerary, total_cost, trip_config['currency'])
    
    with col_info:
        render_info_panel(trip_config)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>✈️ AI Trip Planner Agent | Powered by 
        <span style="color: #0F4C75;">Open-Meteo</span>, 
        <span style="color: #0F4C75;">OpenStreetMap</span>, 
        <span style="color: #0F4C75;">Frankfurter</span> & 
        <span style="color: #0F4C75;">Groq</span></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
