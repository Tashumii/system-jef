"""
Sports Management Dashboard - Main Entry Point

A secure GUI application for managing sports games with admin authentication.
Built using Object-Oriented Programming principles with Tkinter UI.

Author: AI Assistant
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add current directory to path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config.settings import DATABASE_CONFIG, APP_CONFIG
    from ui.main_application import MainApplication
    from database.mysql_manager import MySQLManager
    from ui.login_window import LoginWindow
except ImportError as e:
    print(f"Startup Error: {e}")
    print("Please run this script from the project root directory.")
    sys.exit(1)


def main():
    """
    Main application entry point.

    Initializes database connection, shows login window first,
    and then launches the main GUI application after successful login.
    """
    try:
        # Initialize database manager
        data_manager = MySQLManager(**DATABASE_CONFIG)
        data_manager.connect()

        # Check database health
        if not data_manager.check_database_health():
            raise Exception(
                "Database health check failed. Please check your MySQL server.")

        # Create the main application (hidden initially)
        app = MainApplication(data_manager)
        app.withdraw()  # hide until login succeeds

        # Show login window
        def on_login_success(user):
            app.current_user = user
            app.deiconify()  # show main app
            app.show_view("dashboard")

        login = LoginWindow(app, data_manager, on_login_success)
        login.focus_set()
        login.grab_set()

        # Start the main loop
        app.run()

    except Exception as e:
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Application Error",
                f"Failed to start application:\n{str(e)}\n\nPlease ensure MySQL is running."
            )
            root.destroy()
        except:
            print(f"CRITICAL ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
