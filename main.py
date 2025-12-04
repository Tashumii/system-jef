"""
Enhanced Sports Management System - Complete Project Structure
===============================================================

PROJECT STRUCTURE:
------------------
sports_management/
├── config/
│   ├── __init__.py
│   └── settings.py
├── database/
│   ├── __init__.py
│   ├── interfaces.py
│   └── mysql_manager.py
├── models/
│   ├── __init__.py
│   ├── sports.py
│   └── player.py
├── ui/
│   ├── __init__.py
│   ├── main_application.py
│   ├── game_form.py
│   ├── player_management.py
│   ├── analytics.py
│   ├── components.py
│   └── auth.py
├── utils/
│   ├── __init__.py
│   ├── validation.py
│   └── auth.py
└── main.py
"""

# ============================================================================
# FILE: config/settings.py
# ============================================================================
"""
Configuration settings for the Enhanced Sports Management System
"""

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "sports_management_db"
}

APP_CONFIG = {
    "title": "🏆 Enhanced Sports Management System",
    "geometry": "1400x900",
    "resizable": True,
    "theme": "dark"
}

# Available sports in the system
SPORTS_LIST = [
    "Soccer",
    "Basketball", 
    "Tennis",
    "Volleyball",
    "Baseball",
    "Hockey",
    "Cricket",
    "Rugby",
    "American Football",
    "Golf"
]

# Game types
GAME_TYPES = [
    "Regular Season",
    "Playoffs",
    "Finals",
    "Friendly",
    "Tournament",
    "Championship",
    "Exhibition"
]

# League options
LEAGUE_OPTIONS = [
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "NBA",
    "EuroLeague",
    "NFL",
    "MLB",
    "NHL",
    "ATP Tour",
    "WTA Tour",
    "ICC Cricket",
    "Rugby World Cup",
    "Custom League"
]

# UI Colors
COLORS = {
    "primary": "#00d4aa",
    "secondary": "#ff6b6b",
    "background": "#1a1a1a",
    "card_bg": "#2d2d2d",
    "input_bg": "#404040",
    "text": "#e0e0e0",
    "text_secondary": "#888888",
    "success": "#00d4aa",
    "warning": "#f9ca24",
    "error": "#ff6b6b"
}


# ============================================================================
# FILE: database/interfaces.py
# ============================================================================
"""
Database Abstraction Layer - Enhanced Interfaces
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IDataManager(ABC):
    """Enhanced abstract database manager interface"""

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection"""
        pass

    @abstractmethod
    def add_game(self, game_obj: Dict[str, Any]) -> bool:
        """Add a new game"""
        pass

    @abstractmethod
    def fetch_games(self) -> List[Dict[str, Any]]:
        """Retrieve all games"""
        pass
    
    @abstractmethod
    def update_game(self, game_id: int, game_obj: Dict[str, Any]) -> bool:
        """Update an existing game"""
        pass
    
    @abstractmethod
    def delete_game(self, game_id: int) -> bool:
        """Delete a game"""
        pass

    # Player management
    @abstractmethod
    def add_player(self, player_obj: Dict[str, Any]) -> bool:
        """Add a new player"""
        pass

    @abstractmethod
    def fetch_players(self, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all players, optionally filtered by sport"""
        pass
    
    @abstractmethod
    def update_player(self, player_id: int, player_obj: Dict[str, Any]) -> bool:
        """Update player information"""
        pass
    
    @abstractmethod
    def delete_player(self, player_id: int) -> bool:
        """Delete a player"""
        pass

    # Team management
    @abstractmethod
    def add_team(self, team_obj: Dict[str, Any]) -> bool:
        """Add a new team"""
        pass

    @abstractmethod
    def fetch_teams(self, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all teams"""
        pass

    # Authentication
    @abstractmethod
    def register_admin(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        """Register a new admin user"""
        pass

    @abstractmethod
    def authenticate_admin(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate an admin user"""
        pass


# ============================================================================
# FILE: database/mysql_manager.py
# ============================================================================
"""
Enhanced MySQL Database Manager with Player and Team Management
"""

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from typing import List, Dict, Any, Optional

from database.interfaces import IDataManager


class EnhancedMySQLManager(IDataManager):
    """Enhanced MySQL Database Manager Implementation"""

    def __init__(self, host: str = "localhost", port: int = 3306,
                 user: str = "root", password: str = "", database: str = "sports_management_db"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> None:
        """Establish MySQL database connection and initialize enhanced schema"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                cursor = self.connection.cursor()

                # Enhanced games table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS games (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        sport VARCHAR(50) NOT NULL,
                        game_type VARCHAR(50),
                        league VARCHAR(100) NOT NULL,
                        team1 VARCHAR(100) NOT NULL,
                        team2 VARCHAR(100) NOT NULL,
                        score VARCHAR(20) NOT NULL,
                        date DATE NOT NULL,
                        time TIME,
                        venue VARCHAR(200),
                        attendance INT,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_games_date (date),
                        INDEX idx_games_sport (sport),
                        INDEX idx_games_league (league)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # Players table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS players (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100) NOT NULL,
                        sport VARCHAR(50) NOT NULL,
                        jersey_number VARCHAR(10),
                        position VARCHAR(50),
                        date_of_birth DATE,
                        nationality VARCHAR(100),
                        height DECIMAL(5,2),
                        weight DECIMAL(5,2),
                        team_id INT,
                        status VARCHAR(20) DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_players_sport (sport),
                        INDEX idx_players_name (last_name, first_name)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # Teams table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS teams (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        sport VARCHAR(50) NOT NULL,
                        league VARCHAR(100),
                        city VARCHAR(100),
                        country VARCHAR(100),
                        founded_year INT,
                        home_venue VARCHAR(200),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_teams_sport (sport),
                        INDEX idx_teams_name (name)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # Admin users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS admin_users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        full_name VARCHAR(100),
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP NULL,
                        INDEX idx_admin_username (username)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                self.connection.commit()
                cursor.close()

        except Error as err:
            messagebox.showerror("Database Error", f"Failed to connect: {err}")
            raise

    def add_game(self, game_obj: Dict[str, Any]) -> bool:
        """Add a new game with enhanced fields"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO games (sport, game_type, league, team1, team2, score, 
                                 date, time, venue, attendance, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                game_obj.get('sport'),
                game_obj.get('game_type'),
                game_obj.get('league'),
                game_obj.get('team1'),
                game_obj.get('team2'),
                game_obj.get('score'),
                game_obj.get('date'),
                game_obj.get('time'),
                game_obj.get('venue'),
                game_obj.get('attendance'),
                game_obj.get('notes')
            ))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to add game: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_games(self) -> List[Dict[str, Any]]:
        """Retrieve all games"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM games ORDER BY date DESC, time DESC")
            return cursor.fetchall()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch games: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def update_game(self, game_id: int, game_obj: Dict[str, Any]) -> bool:
        """Update an existing game"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE games SET sport=%s, game_type=%s, league=%s, team1=%s, 
                               team2=%s, score=%s, date=%s, time=%s, venue=%s, 
                               attendance=%s, notes=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                game_obj.get('sport'), game_obj.get('game_type'),
                game_obj.get('league'), game_obj.get('team1'),
                game_obj.get('team2'), game_obj.get('score'),
                game_obj.get('date'), game_obj.get('time'),
                game_obj.get('venue'), game_obj.get('attendance'),
                game_obj.get('notes'), game_id
            ))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to update game: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def delete_game(self, game_id: int) -> bool:
        """Delete a game"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM games WHERE id=%s", (game_id,))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to delete game: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def add_player(self, player_obj: Dict[str, Any]) -> bool:
        """Add a new player"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO players (first_name, last_name, sport, jersey_number, 
                                   position, date_of_birth, nationality, height, weight)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                player_obj.get('first_name'),
                player_obj.get('last_name'),
                player_obj.get('sport'),
                player_obj.get('jersey_number'),
                player_obj.get('position'),
                player_obj.get('date_of_birth'),
                player_obj.get('nationality'),
                player_obj.get('height'),
                player_obj.get('weight')
            ))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to add player: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_players(self, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all players, optionally filtered by sport"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            if sport:
                cursor.execute("SELECT * FROM players WHERE sport=%s ORDER BY last_name", (sport,))
            else:
                cursor.execute("SELECT * FROM players ORDER BY last_name")
            return cursor.fetchall()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch players: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def update_player(self, player_id: int, player_obj: Dict[str, Any]) -> bool:
        """Update player information"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE players SET first_name=%s, last_name=%s, sport=%s, 
                                 jersey_number=%s, position=%s, date_of_birth=%s,
                                 nationality=%s, height=%s, weight=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                player_obj.get('first_name'), player_obj.get('last_name'),
                player_obj.get('sport'), player_obj.get('jersey_number'),
                player_obj.get('position'), player_obj.get('date_of_birth'),
                player_obj.get('nationality'), player_obj.get('height'),
                player_obj.get('weight'), player_id
            ))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to update player: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def delete_player(self, player_id: int) -> bool:
        """Delete a player"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM players WHERE id=%s", (player_id,))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to delete player: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def add_team(self, team_obj: Dict[str, Any]) -> bool:
        """Add a new team"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO teams (name, sport, league, city, country, founded_year, home_venue)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                team_obj.get('name'), team_obj.get('sport'),
                team_obj.get('league'), team_obj.get('city'),
                team_obj.get('country'), team_obj.get('founded_year'),
                team_obj.get('home_venue')
            ))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to add team: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_teams(self, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all teams"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            if sport:
                cursor.execute("SELECT * FROM teams WHERE sport=%s ORDER BY name", (sport,))
            else:
                cursor.execute("SELECT * FROM teams ORDER BY name")
            return cursor.fetchall()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch teams: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    def register_admin(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        """Register a new admin user"""
        from utils.auth import hash_password
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM admin_users WHERE username=%s OR email=%s", (username, email))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or email already exists")
                return False
            
            password_hash = hash_password(password)
            query = "INSERT INTO admin_users (username, email, password_hash, full_name) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, email, password_hash, full_name))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to register: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def authenticate_admin(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate an admin user"""
        from utils.auth import verify_password
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admin_users WHERE username=%s AND is_active=TRUE", (username,))
            user = cursor.fetchone()
            if user and verify_password(password, user['password_hash']):
                return user
            return None
        except Error:
            return None
        finally:
            if cursor:
                cursor.close()


# ============================================================================
# FILE: models/sports.py
# ============================================================================
"""
Enhanced Sport models with more sports support
"""

from abc import ABC, abstractmethod


class Sport(ABC):
    """Base Sport Class"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def validate_score(self, score_str: str) -> bool:
        """Validate sport-specific score format"""
        pass

    def get_name(self) -> str:
        return self.name


class Soccer(Sport):
    def __init__(self):
        super().__init__("Soccer")

    def validate_score(self, score_str: str) -> bool:
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            score1, score2 = int(parts[0].strip()), int(parts[1].strip())
            return 0 <= score1 <= 15 and 0 <= score2 <= 15
        except ValueError:
            return False


class Basketball(Sport):
    def __init__(self):
        super().__init__("Basketball")

    def validate_score(self, score_str: str) -> bool:
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            score1, score2 = int(parts[0].strip()), int(parts[1].strip())
            return 50 <= score1 <= 200 and 50 <= score2 <= 200
        except ValueError:
            return False


class Tennis(Sport):
    def __init__(self):
        super().__init__("Tennis")

    def validate_score(self, score_str: str) -> bool:
        # Tennis: 3-1 (sets) or 6-4, 6-3, 7-5 (games)
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            score1, score2 = int(parts[0].strip()), int(parts[1].strip())
            return 0 <= score1 <= 7 and 0 <= score2 <= 7
        except ValueError:
            return False


class Volleyball(Sport):
    def __init__(self):
        super().__init__("Volleyball")

    def validate_score(self, score_str: str) -> bool:
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            score1, score2 = int(parts[0].strip()), int(parts[1].strip())
            return 0 <= score1 <= 5 and 0 <= score2 <= 5
        except ValueError:
            return False


# ============================================================================
# FILE: models/player.py
# ============================================================================
"""
Player model class
"""

from typing import Optional
from datetime import date


class Player:
    """Player model class"""
    
    def __init__(self, first_name: str, last_name: str, sport: str,
                 jersey_number: Optional[str] = None,
                 position: Optional[str] = None,
                 date_of_birth: Optional[date] = None,
                 nationality: Optional[str] = None,
                 height: Optional[float] = None,
                 weight: Optional[float] = None):
        
        self.first_name = first_name
        self.last_name = last_name
        self.sport = sport
        self.jersey_number = jersey_number
        self.position = position
        self.date_of_birth = date_of_birth
        self.nationality = nationality
        self.height = height
        self.weight = weight
    
    def get_full_name(self) -> str:
        """Return full name"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'sport': self.sport,
            'jersey_number': self.jersey_number,
            'position': self.position,
            'date_of_birth': self.date_of_birth,
            'nationality': self.nationality,
            'height': self.height,
            'weight': self.weight
        }


# ============================================================================
# FILE: utils/validation.py
# ============================================================================
"""
Enhanced validation utilities
"""

import re
from datetime import datetime
from typing import List, Dict, Any


class ValidationResult:
    """Validation result container"""
    
    def __init__(self, is_valid: bool, message: str = "", field: str = "", severity: str = "error"):
        self.is_valid = is_valid
        self.message = message
        self.field = field
        self.severity = severity


class EnhancedValidator:
    """Enhanced data validation"""
    
    @staticmethod
    def validate_required(value: str, field_name: str) -> ValidationResult:
        """Validate required field"""
        if not value or not value.strip():
            return ValidationResult(False, f"{field_name} is required", field_name)
        return ValidationResult(True)
    
    @staticmethod
    def validate_date(date_str: str) -> ValidationResult:
        """Validate date format"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return ValidationResult(True)
        except ValueError:
            return ValidationResult(False, "Invalid date format. Use YYYY-MM-DD", "date")
    
    @staticmethod
    def validate_score(score_str: str) -> ValidationResult:
        """Validate score format"""
        if not re.match(r'^\d+-\d+$', score_str):
            return ValidationResult(False, "Invalid score format. Use X-Y", "score")
        return ValidationResult(True)
    
    @staticmethod
    def validate_number(value: str, field_name: str, min_val: int = None, max_val: int = None) -> ValidationResult:
        """Validate numeric field"""
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                return ValidationResult(False, f"{field_name} must be at least {min_val}", field_name)
            if max_val is not None and num > max_val:
                return ValidationResult(False, f"{field_name} must be at most {max_val}", field_name)
            return ValidationResult(True)
        except ValueError:
            return ValidationResult(False, f"{field_name} must be a number", field_name)


# ============================================================================
# FILE: utils/auth.py  
# ============================================================================
"""
Authentication utilities
"""

import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def validate_password_strength(password: str) -> List[str]:
    """Validate password strength"""
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        errors.append("Password must contain uppercase letter")
    if not any(c.islower() for c in password):
        errors.append("Password must contain lowercase letter")
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain a number")
    return errors


# ============================================================================
# INSTALLATION INSTRUCTIONS
# ============================================================================
"""
SETUP INSTRUCTIONS:
-------------------

1. Create the project structure:
   mkdir -p sports_management/{config,database,models,ui,utils}
   
2. Create __init__.py in each folder:
   touch sports_management/{config,database,models,ui,utils}/__init__.py
   
3. Install required packages:
   pip install mysql-connector-python bcrypt

4. Create MySQL database:
   CREATE DATABASE sports_management_db;
   
5. Update config/settings.py with your MySQL credentials

6. Run the application:
   python main.py

DATABASE SCHEMA:
----------------
The database will be automatically created with these tables:
- games (enhanced with game_type, time, venue, attendance, notes)
- players (first_name, last_name, sport, jersey_number, position, dob, nationality, height, weight)
- teams (name, sport, league, city, country, founded_year, home_venue)
- admin_users (username, email, password_hash, full_name, is_active)

FEATURES:
---------
✅ Multi-sport support (10+ sports)
✅ Player management with detailed profiles
✅ Enhanced game tracking with venue, time, attendance
✅ Team management
✅ Advanced analytics
✅ User authentication
✅ Modern dark theme UI
✅ Search and filter capabilities
✅ Data validation
✅ Secure password hashing
"""
