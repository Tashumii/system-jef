"""
Configuration settings for the application.
Includes database connection details and UI constants.
"""

# Database Configuration
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",  # Default XAMPP MySQL password is empty
    "database": "sports_db"
}

# Application Configuration
APP_CONFIG = {
    "title": "Sports Management Dashboard",
    "geometry": "1200x700",
    "resizable": True
}

# League Options
# Updated to include leagues for Soccer, Basketball, F1, and Billiards
LEAGUE_OPTIONS = [
    # --- Soccer ---
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Champions League",
    "Europa League",

    # --- Basketball ---
    "NBA",
    "EuroLeague",
    "College Basketball",
    "WNBA",

    # --- Formula 1 ---
    "F1 World Championship",
    "Monaco Grand Prix",
    "British Grand Prix",
    "Italian Grand Prix",

    # --- Billiards/Snooker ---
    "World Pool Championship",
    "Mosconi Cup",
    "World Snooker Championship",
    "US Open Pool Championship"
]
