"""
Sports Management Dashboard - Main Entry Point

A secure GUI application for managing sports games with admin authentication.
Built using Object-Oriented Programming principles with Tkinter UI.

Author: AI Assistant
"""

import sys
import os
from tkinter import messagebox

# Add current directory to path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config.settings import DATABASE_CONFIG, APP_CONFIG
    from ui.main_application import MainApplication
    from database.mysql_manager import MySQLManager
except ImportError as e:
    # Fallback if modules are not found (e.g. run from wrong directory)
    print(f"Startup Error: {e}")
    print("Please run this script from the project root directory.")
    sys.exit(1)


def main():
    """
    Main application entry point.

    Initializes database connection and starts the GUI application.
    Handles startup errors gracefully with user-friendly messages.
    """
    try:
        # Initialize database manager using Abstraction pattern
        # This will also create the new tables (sports, participants) if they don't exist
        data_manager = MySQLManager(**DATABASE_CONFIG)

        # Connect to database
        data_manager.connect()

        # Verify database health before launching UI
        if not data_manager.check_database_health():
            raise Exception(
                "Database health check failed. Please check your MySQL server.")

        # Create and run the main application
        # The MainApplication handles the theme setup internally
        app = MainApplication(data_manager)

        # Set initial title (will be updated after login)
        app.title(APP_CONFIG['title'])

        # Start the application loop
        app.run()

    except Exception as e:
        # Ensure we show a graphical error since we are a GUI app
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Application Error",
                                 f"Failed to start application:\n{str(e)}\n\nPlease ensure MySQL is running.")
            root.destroy()
        except:
            # Fallback to console if Tkinter fails
            print(f"CRITICAL ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

