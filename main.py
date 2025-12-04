"""
Sports Management Dashboard - Main Entry Point

A secure GUI application for managing sports games with admin authentication.
Built using Object-Oriented Programming principles with Tkinter UI.

Author: AI Assistant
"""

from config.settings import DATABASE_CONFIG
from ui.main_application import MainApplication
from database.mysql_manager import MySQLManager
import sys
from tkinter import messagebox

# Add current directory to path for absolute imports
sys.path.insert(0, '.')


def main():
    """
    Main application entry point.

    Initializes database connection and starts the GUI application.
    Handles startup errors gracefully with user-friendly messages.
    """
    """Main application entry point."""
    try:
        # Initialize database manager using Abstraction pattern
        data_manager = MySQLManager(**DATABASE_CONFIG)

        # Connect to database
        data_manager.connect()

        # Create and run the main application
        app = MainApplication(data_manager)
        app.run()

    except Exception as e:
        messagebox.showerror("Application Error",
                             f"Failed to start application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
