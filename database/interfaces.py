"""
Database Abstraction Layer

Defines interfaces for database operations using the Abstraction design pattern.
This allows different database implementations (MySQL, SQLite, etc.) to be
swapped without changing the application code.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IDataManager(ABC):
    """
    Abstract database manager interface.

    Defines the contract for all database operations that the application needs.
    Concrete implementations must provide all these methods.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Establish connection to the database.

        Should initialize connection and create necessary tables if they don't exist.
        Raises exception if connection fails.
        """
        pass

    @abstractmethod
    def add_game(self, game_obj: Dict[str, Any]) -> bool:
        """
        Add a new game to the database.

        Args:
            game_obj: Dictionary containing game data (sport, league, teams, score, date)

        Returns:
            True if game was added successfully, False otherwise
        """
        pass

    @abstractmethod
    def fetch_games(self) -> List[Dict[str, Any]]:
        """
        Retrieve all games from the database.

        Returns:
            List of dictionaries, each representing a game record
        """
        pass

    # Authentication methods
    @abstractmethod
    def register_admin(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        """
        Register a new admin user with secure password hashing.

        Args:
            username: Unique username for the admin
            email: Email address for the admin
            password: Plain text password (will be hashed)
            full_name: Optional full name for the admin

        Returns:
            True if registration successful, False if username/email already exists
        """
        pass

    @abstractmethod
    def authenticate_admin(self, username: str, password: str) -> Dict[str, Any] | None:
        """
        Authenticate an admin user with username and password.

        Args:
            username: Admin username
            password: Plain text password to verify

        Returns:
            User data dictionary if authentication successful, None if failed
        """
        pass

    @abstractmethod
    def update_admin_last_login(self, user_id: int) -> bool:
        """
        Update the last login timestamp for an admin user.

        Args:
            user_id: The admin user's ID

        Returns:
            True if update successful, False otherwise
        """
        pass

    @abstractmethod
    def get_admin_by_username(self, username: str) -> Dict[str, Any] | None:
        """
        Retrieve admin user data by username.

        Args:
            username: Username to search for

        Returns:
            User data dictionary if found, None if user doesn't exist
        """
        pass
