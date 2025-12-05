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
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def login_user(username_or_email: str, password: str, data_manager):
    """
    Login user by verifying credentials against database.
    Returns user object if successful, else None.
    """
    username_or_email = username_or_email.strip()

    # Fetch user from database (your IDataManager should have a method like get_user_by_username_or_email)
    user = data_manager.get_user_by_username_or_email(username_or_email)
    if not user:
        return None  # User not found

    # user['password'] should be the hashed password from DB
    hashed_password = user['password']

    # Verify password
    if verify_password(password, hashed_password):
        return user
    else:
        return None


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def validate_password_strength(password: str, allow_weak: bool = True) -> tuple[list[str], bool]:
    """
    Validate password meets security requirements.

    If `allow_weak` is True, the function will return a boolean flag indicating
    if the password is weak but still allow creation.

    Returns:
        errors: List of error messages
        can_proceed: True if user can create account (even with weak password if allowed)
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

    can_proceed = allow_weak or len(errors) == 0
    return errors, can_proceed


def validate_username(username: str) -> list[str]:
    """
    Validate username requirements.
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
    """
    errors = []

    if '@' not in email or '.' not in email:
        errors.append("Invalid email format")
    if len(email) > 100:
        errors.append("Email must be no more than 100 characters long")

    return errors
