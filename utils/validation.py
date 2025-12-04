"""
Comprehensive validation utilities for the Sports Management System.
Handles all types of validation: form data, business logic, data integrity.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    message: str
    field: Optional[str] = None
    severity: str = "error"  # error, warning, info


class ValidationError(Exception):
    """Custom exception for validation errors."""

    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(message)


class SportsDataValidator:
    """
    Sports Data Validation Engine.

    Provides comprehensive validation for all sports-related data including:
    - Game data integrity and business rules
    - Team name validation and uniqueness
    - Score format validation by sport
    - League-sport compatibility checks
    - Date range and format validation
    """

    # League-sport mappings for validation
    LEAGUE_SPORT_MAPPING = {
        "Premier League": "Soccer",
        "La Liga": "Soccer",
        "Serie A": "Soccer",
        "Bundesliga": "Soccer",
        "Champions League": "Soccer",
        "Europa League": "Soccer",
        "NBA": "Basketball",
        "EuroLeague": "Basketball",
        "College Basketball": "Basketball",
        "WNBA": "Basketball"
    }

    # Team name patterns for different sports
    TEAM_NAME_PATTERNS = {
        "Soccer": r"^[A-Za-z\s\-\.\'&À-ÿ]{2,50}$",
        "Basketball": r"^[A-Za-z\s\-\.\d'&À-ÿ]{2,50}$"
    }

    # League name validation pattern
    LEAGUE_NAME_PATTERN = r"^[A-Za-z\s\-\.\d'&À-ÿ]{2,100}$"

    # Score patterns for different sports
    SCORE_PATTERNS = {
        "Soccer": r"^\d{1,2}-\d{1,2}$",
        "Basketball": r"^\d{2,3}-\d{2,3}$"
    }

    @staticmethod
    def validate_team_name(team_name: str, sport: str) -> ValidationResult:
        """
        Validate team name format and length for a specific sport.

        Args:
            team_name: Name of the team to validate
            sport: Sport type (Soccer, Basketball, etc.)

        Returns:
            ValidationResult indicating if team name is valid
        """
        """Validate team name format and length."""
        if not team_name or not team_name.strip():
            return ValidationResult(False, "Team name cannot be empty", "team_name")

        team_name = team_name.strip()

        if len(team_name) < 2:
            return ValidationResult(False, "Team name must be at least 2 characters", "team_name")

        if len(team_name) > 50:
            return ValidationResult(False, "Team name cannot exceed 50 characters", "team_name")

        # Check for pattern if sport is specified
        if sport in SportsDataValidator.TEAM_NAME_PATTERNS:
            pattern = SportsDataValidator.TEAM_NAME_PATTERNS[sport]
            if not re.match(pattern, team_name):
                return ValidationResult(False,
                                        f"Team name contains invalid characters for {sport}", "team_name")

        # Check for potentially problematic characters
        if any(char in team_name for char in ['<', '>', '"', "'", ';', '--']):
            return ValidationResult(False, "Team name contains invalid characters", "team_name")

        return ValidationResult(True, "Team name is valid")

    @staticmethod
    def validate_league_name(league_name: str) -> ValidationResult:
        """Validate league name format."""
        if not league_name or not league_name.strip():
            return ValidationResult(False, "League name cannot be empty", "league")

        league_name = league_name.strip()

        if len(league_name) < 2:
            return ValidationResult(False, "League name must be at least 2 characters", "league")

        if len(league_name) > 100:
            return ValidationResult(False, "League name cannot exceed 100 characters", "league")

        if not re.match(SportsDataValidator.LEAGUE_NAME_PATTERN, league_name):
            return ValidationResult(False, "League name contains invalid characters", "league")

        return ValidationResult(True, "League name is valid")

    @staticmethod
    def validate_date(date_str: str) -> ValidationResult:
        """Validate date format and range."""
        if not date_str or not date_str.strip():
            return ValidationResult(False, "Date cannot be empty", "date")

        try:
            date_obj = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        except ValueError:
            return ValidationResult(False, "Invalid date format. Use YYYY-MM-DD", "date")

        now = datetime.now()
        min_date = now - timedelta(days=365*10)  # 10 years ago
        max_date = now + timedelta(days=365)     # 1 year in future

        if date_obj < min_date:
            return ValidationResult(False, "Date cannot be more than 10 years ago", "date")

        if date_obj > max_date:
            return ValidationResult(False, "Date cannot be more than 1 year in the future", "date")

        # Warn about future dates
        if date_obj > now:
            return ValidationResult(True, "Future date detected", "date", "warning")

        return ValidationResult(True, "Date is valid")

    @staticmethod
    def validate_score(score_str: str, sport: str) -> ValidationResult:
        """Validate score format and ranges."""
        if not score_str or not score_str.strip():
            return ValidationResult(False, "Score cannot be empty", "score")

        score_str = score_str.strip()

        # Check format pattern
        if sport in SportsDataValidator.SCORE_PATTERNS:
            pattern = SportsDataValidator.SCORE_PATTERNS[sport]
            if not re.match(pattern, score_str):
                return ValidationResult(False,
                                        f"Invalid score format for {sport}. Use format: X-Y", "score")

        # Parse scores
        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return ValidationResult(False, "Score must be in format X-Y", "score")

            score1 = int(parts[0].strip())
            score2 = int(parts[1].strip())

            if score1 < 0 or score2 < 0:
                return ValidationResult(False, "Scores cannot be negative", "score")

        except (ValueError, IndexError):
            return ValidationResult(False, "Invalid score format. Use numbers only", "score")

        # Sport-specific validation
        if sport == "Soccer":
            if score1 > 15 or score2 > 15:
                return ValidationResult(False, "Soccer scores rarely exceed 15 goals", "score", "warning")
            elif score1 > 10 or score2 > 10:
                return ValidationResult(True, "High scoring game detected", "score", "info")

        elif sport == "Basketball":
            if score1 < 50 or score2 < 50:
                return ValidationResult(False, "Basketball scores are typically above 50", "score")
            elif score1 > 200 or score2 > 200:
                return ValidationResult(False, "Basketball scores rarely exceed 200 points", "score", "warning")

        return ValidationResult(True, "Score is valid")

    @staticmethod
    def validate_league_sport_compatibility(league: str, sport: str) -> ValidationResult:
        """Validate that league is appropriate for the sport."""
        expected_sport = SportsDataValidator.LEAGUE_SPORT_MAPPING.get(league)

        if expected_sport and expected_sport != sport:
            return ValidationResult(False,
                                    f"'{league}' is typically a {expected_sport} league, not {sport}", "league", "warning")

        return ValidationResult(True, "League-sport combination is valid")

    @staticmethod
    def validate_unique_game(team1: str, team2: str, league: str, date: str,
                             existing_games: List[Dict[str, Any]], exclude_id: Optional[int] = None) -> ValidationResult:
        """Check for duplicate games."""
        for game in existing_games:
            if exclude_id and game.get('id') == exclude_id:
                continue

            # Check if same teams, league, and date
            if (game['team1'] == team1 and game['team2'] == team2 and
                    game['league'] == league and game['date'] == date):
                return ValidationResult(False,
                                        "A game between these teams in this league already exists on this date", "general")

            # Check reverse team order
            if (game['team1'] == team2 and game['team2'] == team1 and
                    game['league'] == league and game['date'] == date):
                return ValidationResult(False,
                                        "A game between these teams in this league already exists on this date", "general")

        return ValidationResult(True, "Game is unique")

    @staticmethod
    def validate_game_data(game_data: Dict[str, Any], existing_games: Optional[List[Dict[str, Any]]] = None,
                           exclude_game_id: Optional[int] = None) -> List[ValidationResult]:
        """
        Perform comprehensive validation on game data.

        Validates all aspects of game data including format, business rules,
        uniqueness constraints, and data integrity.

        Args:
            game_data: Dictionary containing game information
            existing_games: List of existing games for uniqueness checks
            exclude_game_id: Game ID to exclude from duplicate checks (for updates)

        Returns:
            List of ValidationResult objects with all validation issues
        """
        results = []

        # Required fields
        required_fields = ['sport', 'league',
                           'team1', 'team2', 'score', 'date']
        for field in required_fields:
            if field not in game_data or not game_data[field]:
                results.append(ValidationResult(
                    False, f"{field} is required", field))

        if not all(field in game_data and game_data[field] for field in required_fields):
            return results  # Don't continue if required fields are missing

        # Individual field validations
        sport = game_data['sport']
        league = game_data['league']
        team1 = game_data['team1']
        team2 = game_data['team2']
        score = game_data['score']
        date = game_data['date']

        # Team validations
        results.append(SportsDataValidator.validate_team_name(team1, sport))
        results.append(SportsDataValidator.validate_team_name(team2, sport))

        # Same team check
        if team1.strip().lower() == team2.strip().lower():
            results.append(ValidationResult(
                False, "Team 1 and Team 2 cannot be the same", "team2"))

        # League validation
        results.append(SportsDataValidator.validate_league_name(league))

        # League-sport compatibility
        results.append(
            SportsDataValidator.validate_league_sport_compatibility(league, sport))

        # Score validation
        results.append(SportsDataValidator.validate_score(score, sport))

        # Date validation
        results.append(SportsDataValidator.validate_date(date))

        # Uniqueness check
        if existing_games is not None:
            results.append(SportsDataValidator.validate_unique_game(
                team1, team2, league, date, existing_games, exclude_id))

        return results

    @staticmethod
    def validate_batch_games(games_data: List[Dict[str, Any]]) -> Tuple[List[ValidationResult], int]:
        """Validate a batch of games, checking for duplicates within the batch."""
        results = []
        valid_count = 0

        # First, validate each game individually
        for i, game_data in enumerate(games_data):
            game_results = SportsDataValidator.validate_game_data(game_data)
            for result in game_results:
                if not result.is_valid and result.severity == "error":
                    # Add game index to field name for batch context
                    field_name = f"game_{i+1}.{result.field}" if result.field != "general" else f"game_{i+1}"
                    results.append(ValidationResult(
                        result.is_valid, result.message, field_name, result.severity))
                else:
                    results.append(result)

            # Count valid games
            error_count = sum(
                1 for r in game_results if not r.is_valid and r.severity == "error")
            if error_count == 0:
                valid_count += 1

        # Check for duplicates within the batch
        for i, game1 in enumerate(games_data):
            for j, game2 in enumerate(games_data[i+1:], i+1):
                if (game1.get('team1') == game2.get('team1') and
                    game1.get('team2') == game2.get('team2') and
                    game1.get('league') == game2.get('league') and
                        game1.get('date') == game2.get('date')):
                    results.append(ValidationResult(False,
                                                    f"Duplicate games found between games {i+1} and {j+1}", f"game_{i+1}"))
                    valid_count -= 1

        return results, valid_count

    @staticmethod
    def get_validation_summary(results: List[ValidationResult]) -> Dict[str, int]:
        """Get summary of validation results."""
        summary = {
            'total': len(results),
            'errors': 0,
            'warnings': 0,
            'info': 0,
            'valid': 0
        }

        for result in results:
            if result.is_valid:
                summary['valid'] += 1
            elif result.severity == 'error':
                summary['errors'] += 1
            elif result.severity == 'warning':
                summary['warnings'] += 1
            elif result.severity == 'info':
                summary['info'] += 1

        return summary
