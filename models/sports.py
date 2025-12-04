"""
Sport models using Polymorphism pattern.
Base Sport class with concrete implementations for different sports.
"""

from abc import ABC, abstractmethod


class Sport(ABC):
    """
    Base Sport Class.

    Abstract base class defining the interface for all sports.
    Uses polymorphism to allow different sports to have different
    score validation rules while maintaining a common interface.
    """

    def __init__(self, name: str):
        """
        Initialize sport with name.

        Args:
            name: Name of the sport (e.g., "Soccer", "Basketball")
        """
        self.name = name

    @abstractmethod
    def validate_score(self, score_str: str) -> bool:
        """
        Validate if a score string is valid for this sport.

        Different sports have different score formats and ranges.
        This method implements sport-specific validation logic.

        Args:
            score_str: Score string to validate (e.g., "2-1")

        Returns:
            True if score is valid for this sport, False otherwise
        """
        pass

    def get_name(self) -> str:
        """
        Get the name of this sport.

        Returns:
            Sport name as string
        """
        return self.name


class Soccer(Sport):
    """
    Soccer Sport Implementation.

    Validates soccer scores which typically range from 0-5 goals per team.
    Uses format "home_score-away_score" (e.g., "2-1").
    """

    def __init__(self):
        """Initialize soccer sport with default name."""
        super().__init__("Soccer")

    def validate_score(self, score_str: str) -> bool:
        """
        Validate soccer score format and range.

        Soccer scores are typically low numbers (0-5 goals per team).
        Format must be "X-Y" where X and Y are integers 0-5.

        Args:
            score_str: Score string to validate

        Returns:
            True if valid soccer score, False otherwise
        """
        """Validate soccer score format (e.g., '2-1')."""
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False

            score1, score2 = int(parts[0].strip()), int(parts[1].strip())

            # Soccer typically has lower scores (rarely above 10)
            return 0 <= score1 <= 15 and 0 <= score2 <= 15

        except ValueError:
            return False


class Basketball(Sport):
    """
    Basketball Sport Implementation.

    Validates basketball scores which typically range from 50-150 points per team.
    Uses format "home_score-away_score" (e.g., "105-98").
    """

    def __init__(self):
        """Initialize basketball sport with default name."""
        super().__init__("Basketball")

    def validate_score(self, score_str: str) -> bool:
        """
        Validate basketball score format and range.

        Basketball scores are typically high numbers (50-150 points per team).
        Format must be "X-Y" where X and Y are integers 50-150.

        Args:
            score_str: Score string to validate

        Returns:
            True if valid basketball score, False otherwise
        """
        """Validate basketball score format (e.g., '105-98')."""
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False

            score1, score2 = int(parts[0].strip()), int(parts[1].strip())

            # Basketball typically has higher scores (rarely below 50)
            return 50 <= score1 <= 200 and 50 <= score2 <= 200

        except ValueError:
            return False
