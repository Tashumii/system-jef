"""
Authentication Utilities Module.

Provides secure password hashing, verification, and validation functions.
Uses bcrypt for industry-standard password security.
Includes input validation for usernames, emails, and passwords.
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with salt.

    Uses bcrypt algorithm to securely hash passwords with automatic salt generation.
    This provides protection against rainbow table attacks.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string (includes salt)
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        # If there's any error in verification, return False
        return False


def validate_password_strength(password: str) -> list[str]:
    """
    Validate password meets security requirements.

    Checks for minimum length, character variety, and complexity rules
    to ensure passwords are resistant to common attacks.

    Args:
        password: Password string to validate

    Returns:
        List of error messages (empty list if password is valid)
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        errors.append("Password must contain at least one special character")

    return errors


def validate_username(username: str) -> list[str]:
    """
    Validate username requirements.

    Args:
        username: Username to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if len(username) < 3:
        errors.append("Username must be at least 3 characters long")

    if len(username) > 50:
        errors.append("Username must be no more than 50 characters long")

    if not username.replace('_', '').replace('-', '').isalnum():
        errors.append(
            "Username can only contain letters, numbers, underscores, and hyphens")

    if username.startswith('_') or username.startswith('-') or username.endswith('_') or username.endswith('-'):
        errors.append("Username cannot start or end with underscore or hyphen")

    return errors


def validate_email(email: str) -> list[str]:
    """
    Basic email validation.

    Args:
        email: Email to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if '@' not in email or '.' not in email:
        errors.append("Invalid email format")

    if len(email) > 100:
        errors.append("Email must be no more than 100 characters long")

    return errors
