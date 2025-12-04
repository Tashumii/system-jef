from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IDataManager(ABC):
    """Abstract base class for data management."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source."""
        pass

    @abstractmethod
    def add_game(self, game_obj: Dict[str, Any]) -> bool:
        """Add a new game to the database."""
        pass

    # NEW: Delete feature
    @abstractmethod
    def delete_game(self, game_id: int) -> bool:
        """Delete a game by its ID."""
        pass

    @abstractmethod
    def fetch_games(self) -> List[Dict[str, Any]]:
        """Fetch all games from the database."""
        pass

    @abstractmethod
    def add_sport(self, sport_name: str) -> bool:
        """Add a new sport to the persistent list."""
        pass

    @abstractmethod
    def fetch_sports(self) -> List[str]:
        """Fetch list of available sports."""
        pass

    @abstractmethod
    def add_participant(self, name: str, sport_type: str = None) -> bool:
        """Add a new participant (player/team/driver)."""
        pass

    @abstractmethod
    def fetch_participants(self) -> List[str]:
        """Fetch list of all participants."""
        pass

    @abstractmethod
    def check_database_health(self) -> bool:
        """Check if database connection is active."""
        pass

    @abstractmethod
    def register_admin(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        """Register a new admin user."""
        pass

    @abstractmethod
    def authenticate_admin(self, username: str, password: str) -> Dict[str, Any] | None:
        """Authenticate an admin user."""
        pass
