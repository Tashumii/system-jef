"""
MySQL database manager implementation using Abstraction pattern.
Concrete implementation of IDataManager interface using MySQL.
"""

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from typing import List, Dict, Any

from .interfaces import IDataManager


class MySQLManager(IDataManager):
    """
    MySQL Database Manager Implementation.

    Concrete implementation of IDataManager for MySQL databases.
    Handles all database operations including games management and admin authentication.
    """

    def __init__(self, host: str = "localhost", port: int = 3306,
                 user: str = "root", password: str = "", database: str = "sports_db"):
        """
        Initialize MySQL database connection parameters.

        Args:
            host: MySQL server hostname (default: localhost)
            port: MySQL server port (default: 3306)
            user: MySQL username (default: root)
            password: MySQL password (default: empty)
            database: Database name (default: sports_db)
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> None:
        """
        Establish MySQL database connection and initialize schema.

        Creates connection to MySQL server and ensures all required tables exist.
        Tables created: games, admin_users.

        Raises:
            Exception: If connection fails or database operations error
        """
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

                # Create tables if they don't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS games (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        sport VARCHAR(50) NOT NULL,
                        league VARCHAR(100) NOT NULL,
                        team1 VARCHAR(100) NOT NULL,
                        team2 VARCHAR(100) NOT NULL,
                        score VARCHAR(20) NOT NULL,
                        date DATE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_games_date (date),
                        INDEX idx_games_sport (sport),
                        INDEX idx_games_league (league)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # Create admin_users table for authentication
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
                        INDEX idx_admin_username (username),
                        INDEX idx_admin_email (email)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                self.connection.commit()
                cursor.close()

        except Error as err:
            messagebox.showerror("MySQL Connection Error",
                                 f"Failed to connect to MySQL database: {err}")
            raise

    def add_game(self, game_obj: Dict[str, Any]) -> bool:
        """
        Add a new game to the database with validation.

        Performs comprehensive validation including data integrity checks,
        duplicate prevention, and business rule validation before saving.

        Args:
            game_obj: Dictionary with game data (sport, league, team1, team2, score, date)

        Returns:
            True if game added successfully, False if validation failed or database error
        """
        cursor = None
        try:
            # Data integrity validation before saving
            validation_errors = self._validate_game_data_integrity(game_obj)
            if validation_errors:
                error_msg = "Data integrity validation failed:\n" + \
                    "\n".join(f"• {e}" for e in validation_errors)
                messagebox.showerror("Data Integrity Error", error_msg)
                return False

            cursor = self.connection.cursor()

            # Insert the game
            query = """
                INSERT INTO games (sport, league, team1, team2, score, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                game_obj['sport'],
                game_obj['league'],
                game_obj['team1'],
                game_obj['team2'],
                game_obj['score'],
                game_obj['date']
            ))
            self.connection.commit()
            return True

        except Error as err:
            messagebox.showerror(
                "Database Error", f"Failed to add game: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_games(self) -> List[Dict[str, Any]]:
        """Retrieve all games from the MySQL database."""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM games ORDER BY date DESC")

            games = cursor.fetchall()
            return games

        except Error as err:
            messagebox.showerror(
                "Database Error", f"Failed to fetch games: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    def _validate_game_data_integrity(self, game_obj: Dict[str, Any]) -> List[str]:
        """Perform data integrity checks before saving."""
        errors = []

        # Get existing games for duplicate checking
        try:
            existing_games = self.fetch_games()
        except:
            existing_games = []

        # Use comprehensive validation
        from utils.validation import SportsDataValidator
        validation_results = SportsDataValidator.validate_game_data(
            game_obj, existing_games)

        # Collect all error messages
        for result in validation_results:
            if not result.is_valid and result.severity == 'error':
                errors.append(result.message)

        return errors

    def check_database_health(self) -> bool:
        """Check if the database is healthy and accessible."""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                return False

            cursor = self.connection.cursor()

            # Test basic connectivity
            cursor.execute("SELECT 1")
            cursor.fetchone()

            # Check if required tables exist
            required_tables = ['games', 'admin_users']
            for table in required_tables:
                cursor.execute("SHOW TABLES LIKE %s", (table,))
                if not cursor.fetchone():
                    print(f"Warning: Required table '{table}' does not exist")
                    return False

            # Try to count records in each table (test data access)
            cursor.execute("SELECT COUNT(*) FROM games")
            cursor.fetchone()

            cursor.execute("SELECT COUNT(*) FROM admin_users")
            cursor.fetchone()

            # Test a more complex query to ensure indexes work
            cursor.execute("SELECT id FROM games LIMIT 1")
            cursor.fetchone()

            return True

        except Error as e:
            print(f"Database health check failed: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def register_admin(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        """
        Register a new admin user with secure password hashing.

        Checks for existing username/email, hashes password with bcrypt,
        and creates new admin user record.

        Args:
            username: Desired username (must be unique)
            email: Email address (must be unique)
            password: Plain text password (will be hashed)
            full_name: Optional full name

        Returns:
            True if registration successful, False if validation failed
        """
        from utils.auth import hash_password

        cursor = None
        try:
            cursor = self.connection.cursor()

            # Check if username or email already exists
            cursor.execute("SELECT id FROM admin_users WHERE username = %s OR email = %s",
                           (username, email))
            if cursor.fetchone():
                messagebox.showerror("Registration Error",
                                     "Username or email already exists")
                return False

            # Hash the password
            password_hash = hash_password(password)

            # Insert new admin user
            query = """
                INSERT INTO admin_users (username, email, password_hash, full_name)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (username, email, password_hash, full_name))
            self.connection.commit()

            messagebox.showinfo("Registration Successful",
                                f"Admin user '{username}' registered successfully!")
            return True

        except Error as err:
            messagebox.showerror(
                "Database Error", f"Failed to register admin: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def authenticate_admin(self, username: str, password: str) -> Dict[str, Any] | None:
        """Authenticate an admin user."""
        from utils.auth import verify_password

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Get user data
            cursor.execute("""
                SELECT id, username, email, password_hash, full_name, is_active, created_at, last_login
                FROM admin_users
                WHERE username = %s AND is_active = TRUE
            """, (username,))

            user = cursor.fetchone()
            if not user:
                return None

            # Verify password
            if verify_password(password, user['password_hash']):
                # Update last login
                self.update_admin_last_login(user['id'])
                return user
            else:
                return None

        except Error as err:
            print(f"Authentication database error: {err}")
            # Don't show database errors to user for security
            return None
        finally:
            if cursor:
                cursor.close()

    def update_admin_last_login(self, user_id: int) -> bool:
        """Update the last login timestamp for an admin user."""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE admin_users
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (user_id,))
            self.connection.commit()
            return True
        except Error as err:
            print(f"Failed to update last login: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def get_admin_by_username(self, username: str) -> Dict[str, Any] | None:
        """Get admin user data by username."""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, username, email, full_name, is_active, created_at, last_login
                FROM admin_users
                WHERE username = %s
            """, (username,))
            return cursor.fetchone()
        except Error as err:
            print(f"Failed to get admin by username: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
