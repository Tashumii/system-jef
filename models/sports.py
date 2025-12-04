"""
Sport models using Polymorphism pattern.
Base Sport class with concrete implementations for different sports.
"""

from abc import ABC, abstractmethod


class Sport(ABC):
    """
    Base Sport Class.
    """

    def __init__(self, name: str, participant_label: str = "Team"):
        """
        Initialize sport with name and participant type.

        Args:
            name: Name of the sport (e.g., "Soccer")
            participant_label: Label for participants (e.g., "Team", "Player", "Driver")
        """
        self.name = name
        self.participant_label = participant_label

    @abstractmethod
    def validate_score(self, score_str: str) -> bool:
        """
        Validate if a score string is valid for this sport.
        """
        pass

    def get_name(self) -> str:
        return self.name


class Soccer(Sport):
    """Soccer Sport Implementation."""

    def __init__(self):
        super().__init__("Soccer", "Team")

    def validate_score(self, score_str: str) -> bool:
        """Validate soccer score (0-30 goals)."""
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            return 0 <= int(parts[0].strip()) <= 30 and 0 <= int(parts[1].strip()) <= 30
        except ValueError:
            return False


class Basketball(Sport):
    """Basketball Sport Implementation."""

    def __init__(self):
        super().__init__("Basketball", "Team")

    def validate_score(self, score_str: str) -> bool:
        """Validate basketball score (30-250 points)."""
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            return 30 <= int(parts[0].strip()) <= 250 and 30 <= int(parts[1].strip()) <= 250
        except ValueError:
            return False


class Billiards(Sport):
    """Billiards/Pool Implementation (Individual Sport)."""

    def __init__(self):
        # Sets label to "Player" for the UI
        super().__init__("Billiards", "Player")

    def validate_score(self, score_str: str) -> bool:
        """Validate billiards score (0-50 racks)."""
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            return 0 <= int(parts[0].strip()) <= 50 and 0 <= int(parts[1].strip()) <= 50
        except ValueError:
            return False


class Formula1(Sport):
    """F1 Implementation (Individual Sport)."""

    def __init__(self):
        # Sets label to "Driver" for the UI
        super().__init__("Formula 1", "Driver")

    def validate_score(self, score_str: str) -> bool:
        """Validate F1 results (Positions 1-2 or Points)."""
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            # Flexible validation: Ensure inputs are numbers
            return parts[0].strip().isdigit() and parts[1].strip().isdigit()
        except ValueError:
            return False


class CustomSport(Sport):
    """
    Custom Sport Implementation.
    Allows for user-defined sports with generic validation logic.
    """

    def __init__(self, name: str):
        # Default generic label "Participant" for unknown sports
        super().__init__(name, "Participant")

    def validate_score(self, score_str: str) -> bool:
        """Generic validation: Just checks for 'number-number' format."""
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return False
            return parts[0].strip().isdigit() and parts[1].strip().isdigit()
        except ValueError:
            return False
