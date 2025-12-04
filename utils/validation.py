"""
Comprehensive validation utilities for the Sports Management System.
Handles all types of validation: form data, business logic, data integrity.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
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
    """

    # Enhanced mappings for new sports
    LEAGUE_SPORT_MAPPING = {
        # Soccer
        "Premier League": "Soccer", "La Liga": "Soccer", "Serie A": "Soccer",
        "Bundesliga": "Soccer", "Champions League": "Soccer", "Europa League": "Soccer",
        # Basketball
        "NBA": "Basketball", "EuroLeague": "Basketball", "WNBA": "Basketball",
        "College Basketball": "Basketball",
        # F1
        "F1 World Championship": "Formula 1", "Monaco Grand Prix": "Formula 1",
        "British Grand Prix": "Formula 1", "Italian Grand Prix": "Formula 1",
        # Billiards
        "World Pool Championship": "Billiards", "Mosconi Cup": "Billiards",
        "US Open Pool Championship": "Billiards"
    }

    @staticmethod
    def validate_team_name(name: str, sport: str) -> ValidationResult:
        """
        Validate participant name (Team, Driver, or Player).
        """
        if not name or not name.strip():
            return ValidationResult(False, "Participant name cannot be empty", "team_name")

        name = name.strip()

        if len(name) < 2:
            return ValidationResult(False, "Name must be at least 2 characters", "team_name")

        if len(name) > 50:
            return ValidationResult(False, "Name cannot exceed 50 characters", "team_name")

        # Check for dangerous characters (SQL injection / XSS prevention basics)
        if any(char in name for char in ['<', '>', ';', '{', '}']):
            return ValidationResult(False, "Name contains invalid characters", "team_name")

        return ValidationResult(True, "Valid")

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

        return ValidationResult(True, "Valid")

    @staticmethod
    def validate_date(date_str: str) -> ValidationResult:
        """Validate date format (YYYY-MM-DD)."""
        if not date_str or not date_str.strip():
            return ValidationResult(False, "Date cannot be empty", "date")

        try:
            date_obj = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        except ValueError:
            return ValidationResult(False, "Invalid format. Use YYYY-MM-DD", "date")

        now = datetime.now()
        min_date = now - timedelta(days=365*20)  # 20 years ago
        max_date = now + timedelta(days=365*2)   # 2 years in future

        if date_obj < min_date:
            return ValidationResult(False, "Date cannot be more than 20 years ago", "date")

        if date_obj > max_date:
            return ValidationResult(False, "Date cannot be more than 2 years in the future", "date")

        if date_obj > now:
            return ValidationResult(True, "Future date detected (Scheduled Game)", "date", "info")

        return ValidationResult(True, "Valid")

    @staticmethod
    def validate_score(score_str: str, sport: str) -> ValidationResult:
        """
        Validate score format and ranges based on the sport.
        Format expected: X-Y
        """
        if not score_str or not score_str.strip():
            return ValidationResult(False, "Score cannot be empty", "score")

        try:
            parts = score_str.split('-')
            if len(parts) != 2:
                return ValidationResult(False, "Score must be format 'X-Y' (e.g. 2-1)", "score")

            s1 = int(parts[0].strip())
            s2 = int(parts[1].strip())

            if s1 < 0 or s2 < 0:
                return ValidationResult(False, "Scores cannot be negative", "score")

            # --- Smart Sport Heuristics ---

            if sport == "Soccer":
                if s1 > 30 or s2 > 30:
                    return ValidationResult(True, "Unusually high score for Soccer", "score", "warning")

            elif sport == "Basketball":
                # Basketball scores are rarely single digits unless it's very early/forfeit
                if (s1 < 30 or s2 < 30) and (s1 + s2 > 0):
                    return ValidationResult(True, "Unusually low score for Basketball", "score", "warning")

            elif sport == "Formula 1":
                # F1 'scores' in this app are finishing positions (1st vs 2nd)
                if s1 > 25 or s2 > 25:
                    return ValidationResult(True, "F1 positions are typically 1-20", "score", "info")
                if s1 == s2:
                    return ValidationResult(True, "Drivers rarely finish in exact same position", "score", "warning")

            elif sport == "Billiards":
                if s1 > 50 or s2 > 50:
                    return ValidationResult(True, "High rack count for Billiards", "score", "info")

            return ValidationResult(True, "Valid")

        except ValueError:
            return ValidationResult(False, "Score must contain only numbers", "score")

    @staticmethod
    def validate_league_sport_compatibility(league: str, sport: str) -> ValidationResult:
        """Warn if a league doesn't match the selected sport."""
        expected_sport = SportsDataValidator.LEAGUE_SPORT_MAPPING.get(league)

        if expected_sport and expected_sport != sport:
            return ValidationResult(
                True,
                f"'{league}' is typically a {expected_sport} league, not {sport}",
                "league",
                "warning"
            )

        return ValidationResult(True, "Valid")

    @staticmethod
    def validate_game_data(game_data: Dict[str, Any], existing_games: Optional[List[Dict[str, Any]]] = None) -> List[ValidationResult]:
        """
        Perform comprehensive validation on the entire game object.
        """
        results = []

        # Extract fields
        sport = game_data.get('sport', '')
        league = game_data.get('league', '')
        team1 = game_data.get('team1', '')
        team2 = game_data.get('team2', '')
        score = game_data.get('score', '')
        date = game_data.get('date', '')

        # 1. Required Check
        for field in ['sport', 'league', 'team1', 'team2', 'score', 'date']:
            if not game_data.get(field):
                results.append(ValidationResult(
                    False, f"{field.title()} is required", field))

        # Return early if missing data to avoid crash in detailed checks
        if any(not r.is_valid for r in results):
            return results

        # 2. Individual Field Validations
        results.append(SportsDataValidator.validate_team_name(team1, sport))
        results.append(SportsDataValidator.validate_team_name(team2, sport))
        results.append(SportsDataValidator.validate_league_name(league))
        results.append(SportsDataValidator.validate_date(date))
        results.append(SportsDataValidator.validate_score(score, sport))

        # 3. Logical Checks
        if team1.strip().lower() == team2.strip().lower():
            results.append(ValidationResult(
                False, "Participant 1 and 2 cannot be the same", "team2"))

        # 4. Business Logic Warnings
        results.append(
            SportsDataValidator.validate_league_sport_compatibility(league, sport))

        # 5. Duplicate Check
        if existing_games:
            for game in existing_games:
                # Check for exact duplicate match
                if (game['team1'] == team1 and game['team2'] == team2 and
                        game['league'] == league and game['date'] == date):
                    results.append(ValidationResult(
                        False, "This match record already exists", "general"))
                    break

        return results
