import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from typing import List, Dict, Any

from .interfaces import IDataManager


class MySQLManager(IDataManager):
    """
    MySQL Database Manager Implementation.
    """

    def __init__(self, host: str = "localhost", port: int = 3306,
                 user: str = "root", password: str = "", database: str = "sports_db"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> None:
        """Establish MySQL database connection and initialize schema."""
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

                # 1. Table: Games
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
                        INDEX idx_games_sport (sport)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # 2. Table: Admin Users
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS admin_users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        full_name VARCHAR(100),
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # 3. Table: Sports (For dropdown list)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sports (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # 4. Table: Participants (Teams, Drivers, Players)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS participants (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        sport_type VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # Seed default sports if table is empty
                cursor.execute("SELECT COUNT(*) FROM sports")
                if cursor.fetchone()[0] == 0:
                    cursor.executemany(
                        "INSERT INTO sports (name) VALUES (%s)",
                        [("Soccer",), ("Basketball",),
                         ("Formula 1",), ("Billiards",)]
                    )

                self.connection.commit()
                cursor.close()

        except Error as err:
            messagebox.showerror("MySQL Connection Error",
                                 f"Failed to connect to MySQL database: {err}")
            raise

    def add_sport(self, sport_name: str) -> bool:
        """Add a new sport to the database."""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO sports (name) VALUES (%s)", (sport_name,))
            self.connection.commit()
            return True
        except Error as err:
            # Ignore duplicate entry errors (error code 1062)
            if err.errno == 1062:
                return True
            print(f"Failed to add sport: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_sports(self) -> List[str]:
        """Fetch list of available sport names."""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sports ORDER BY name ASC")
            return [row[0] for row in cursor.fetchall()]
        except Error:
            return ["Soccer", "Basketball", "Formula 1", "Billiards"]
        finally:
            if cursor:
                cursor.close()

    def add_participant(self, name: str, sport_type: str = None) -> bool:
        """
        Add a new participant (Team/Driver/Player) to the database.
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            # Use INSERT IGNORE to handle duplicates gracefully
            cursor.execute(
                "INSERT IGNORE INTO participants (name, sport_type) VALUES (%s, %s)",
                (name, sport_type)
            )
            self.connection.commit()
            return True
        except Error as err:
            print(f"Failed to add participant: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_participants(self) -> List[str]:
        """Fetch list of all known participants."""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM participants ORDER BY name ASC")
            return [row[0] for row in cursor.fetchall()]
        except Error:
            return []
        finally:
            if cursor:
                cursor.close()

    def add_game(self, game_obj: Dict[str, Any]) -> bool:
        """Add a new game to the database."""
        cursor = None
        try:
            # 1. Ensure the sport exists
            self.add_sport(game_obj['sport'])

            # 2. Ensure participants exist (Auto-save new teams/players)
            self.add_participant(game_obj['team1'], game_obj['sport'])
            self.add_participant(game_obj['team2'], game_obj['sport'])

            # 3. Insert the game
            cursor = self.connection.cursor()
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

    def delete_game(self, game_id: int) -> bool:
        """
        Delete a game from the database by its ID.

        Args:
            game_id: The ID of the game record to delete.

        Returns:
            True if successful, False otherwise.
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
            self.connection.commit()
            return True
        except Error as err:
            print(f"Error deleting game: {err}")
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
            return cursor.fetchall()
        except Error as err:
            messagebox.showerror(
                "Database Error", f"Failed to fetch games: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    def check_database_health(self) -> bool:
        """Check if the database is healthy and accessible."""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                return False

            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return True

        except Error as e:
            print(f"Database health check failed: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def register_admin(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        """Register a new admin user."""
        from utils.auth import hash_password

        cursor = None
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT id FROM admin_users WHERE username = %s OR email = %s",
                           (username, email))
            if cursor.fetchone():
                messagebox.showerror("Registration Error",
                                     "Username or email already exists")
                return False

            password_hash = hash_password(password)

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

            cursor.execute("""
                SELECT id, username, email, password_hash, full_name, is_active, created_at, last_login
                FROM admin_users
                WHERE username = %s AND is_active = TRUE
            """, (username,))

            user = cursor.fetchone()
            if not user:
                return None

            if verify_password(password, user['password_hash']):
                self.update_admin_last_login(user['id'])
                return user
            else:
                return None

        except Error as err:
            print(f"Authentication database error: {err}")
            return None
        finally:
            if cursor:
                cursor.close()

    def update_admin_last_login(self, user_id: int) -> bool:
        """Update the last login timestamp."""
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
