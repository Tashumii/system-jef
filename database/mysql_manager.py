import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any
from tkinter import messagebox
from .interfaces import IDataManager
import bcrypt


class MySQLManager(IDataManager):
    """Enhanced MySQL Manager with authentication and analytics."""

    def __init__(self, host="localhost", port=3306, user="root", password="", database="sports_db"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=self.host, port=self.port, user=self.user,
                password=self.password, database=self.database
            )
            if self.connection.is_connected():
                self._init_schema()
        except Error as err:
            messagebox.showerror("Connection Error", f"Database Error: {err}")
            raise

    def _init_schema(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sport VARCHAR(50) NOT NULL,
                league VARCHAR(100) NOT NULL,
                team1 VARCHAR(100) NOT NULL,
                team2 VARCHAR(100) NOT NULL,
                score VARCHAR(20) NOT NULL,
                date DATE NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_search (team1, team2, league)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE,
                last_login TIMESTAMP NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS sports (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) UNIQUE)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS participants (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) UNIQUE, sport_type VARCHAR(50))")
        # Seed Sports
        cursor.execute("SELECT COUNT(*) FROM sports")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO sports (name) VALUES (%s)", [
                               ("Soccer",), ("Basketball",), ("Formula 1",), ("Tennis",), ("Billiards",)])
        self.connection.commit()
        cursor.close()

    # --- CRUD Games ---
    def add_game(self, game_obj: Dict[str, Any]) -> bool:
        cursor = None
        try:
            self.add_participant(game_obj['team1'], game_obj['sport'])
            self.add_participant(game_obj['team2'], game_obj['sport'])
            cursor = self.connection.cursor()
            query = """
                INSERT INTO games (sport, league, team1, team2, score, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (game_obj['sport'], game_obj['league'], game_obj['team1'],
                                   game_obj['team2'], game_obj['score'], game_obj['date']))
            self.connection.commit()
            return True
        except Error as err:
            print(f"Error adding game: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_games(self) -> List[Dict[str, Any]]:
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM games ORDER BY date DESC LIMIT 1000")
            return cursor.fetchall()
        except Error:
            return []
        finally:
            if cursor:
                cursor.close()

    def delete_game(self, game_id: int) -> bool:
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM games WHERE id=%s", (game_id,))
            self.connection.commit()
            return True
        except Error:
            return False
        finally:
            if cursor:
                cursor.close()

    # --- Sports / Participants ---
    def add_sport(self, name) -> bool:
        try:
            c = self.connection.cursor()
            c.execute("INSERT IGNORE INTO sports (name) VALUES (%s)", (name,))
            self.connection.commit()
            c.close()
            return True
        except:
            return False

    def fetch_sports(self) -> List[str]:
        c = self.connection.cursor()
        c.execute("SELECT name FROM sports")
        return [r[0] for r in c.fetchall()]

    def add_participant(self, name, sport):
        try:
            c = self.connection.cursor()
            c.execute(
                "INSERT IGNORE INTO participants (name, sport_type) VALUES (%s, %s)", (name, sport))
            self.connection.commit()
            c.close()
        except:
            pass

    def fetch_participants(self) -> List[str]:
        c = self.connection.cursor()
        c.execute("SELECT name FROM participants")
        return [r[0] for r in c.fetchall()]

    def check_database_health(self): return True

    # --- Admin Auth ---
    def register_admin(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT id FROM admin_users WHERE username=%s OR email=%s", (username, email))
            if cursor.fetchone():
                messagebox.showwarning(
                    "Registration Failed", "Username or email already exists.")
                return False
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode(), salt)
            cursor.execute("""
                INSERT INTO admin_users (username, email, password_hash, full_name, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, hashed.decode(), full_name, True))
            self.connection.commit()
            return True
        except Error as err:
            messagebox.showerror(
                "Database Error", f"Failed to register admin: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def authenticate_admin(self, username: str, password: str) -> Dict[str, Any] | None:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM admin_users WHERE username=%s AND is_active=1", (username,))
            user = cursor.fetchone()
            if not user:
                return None
            stored_hash = user['password_hash'].encode()
            if bcrypt.checkpw(password.encode(), stored_hash):
                cursor.execute(
                    "UPDATE admin_users SET last_login=NOW() WHERE id=%s", (user['id'],))
                self.connection.commit()
                return user
            return None
        except Error as err:
            messagebox.showerror(
                "Database Error", f"Authentication failed: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
