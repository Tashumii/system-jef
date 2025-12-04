import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any

from database.interfaces import IDataManager
from models.sports import Soccer, Basketball
from config.settings import LEAGUE_OPTIONS
from utils.validation import SportsDataValidator, ValidationResult


class GameForm(ttk.Frame):
    """
    Game Entry Form Widget.

    Provides a user interface for entering new sports games.
    Includes validation, auto-complete, and modern dark theme styling.
    Supports multiple sports with sport-specific validation rules.
    """

    def __init__(self, parent, data_manager: IDataManager, game_list):
        super().__init__(parent, style='Card.TFrame', padding=20)

        self.data_manager = data_manager
        self.game_list = game_list

        # Create sports dictionary for polymorphism
        self.sports = {
            "Soccer": Soccer(),
            "Basketball": Basketball()
        }

        # Cache for auto-complete
        self.team_cache = set()
        self.league_cache = set()
        self.load_caches()

        # Keyboard shortcuts
        self.bind('<Control-s>', lambda e: self.add_game())
        self.bind('<Control-r>', lambda e: self.clear_form())

        self.setup_form()

    def setup_form(self):
        """Set up the form widgets with modern features."""
        # Header with title and quick actions
        header_frame = ttk.Frame(self, style='Card.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2,
                          pady=(0, 20), sticky='ew')

        title = ttk.Label(header_frame, text="⚽ Add New Game",
                          style='Header.TLabel')
        title.pack(side=tk.LEFT, pady=15)

        # Quick templates
        ttk.Button(header_frame, text="📋 Quick Templates",
                   command=self.show_templates).pack(side=tk.RIGHT, padx=(10, 15), pady=15)

        ttk.Button(header_frame, text="📚 Recent Teams",
                   command=self.show_recent_teams).pack(side=tk.RIGHT, padx=(0, 5), pady=15)

        # Sport selection
        ttk.Label(self, text="🏆 Sport:").grid(
            row=1, column=0, sticky="e", padx=(0, 10))
        self.sport_var = tk.StringVar()
        self.sport_combo = ttk.Combobox(self, textvariable=self.sport_var,
                                        values=list(self.sports.keys()), state="readonly", style='TCombobox')
        self.sport_combo.grid(row=1, column=1, sticky="ew", pady=(0, 10))
        self.sport_combo.set("Soccer")  # Default value

        # League selection
        ttk.Label(self, text="🏟️ League:").grid(
            row=2, column=0, sticky="e", padx=(0, 10))
        self.league_var = tk.StringVar()
        self.league_combo = ttk.Combobox(self, textvariable=self.league_var,
                                         values=LEAGUE_OPTIONS,
                                         state="readonly", style='TCombobox')
        self.league_combo.grid(row=2, column=1, sticky="ew", pady=(0, 10))

        # Team 1
        ttk.Label(self, text="👥 Team 1:").grid(
            row=3, column=0, sticky="e", padx=(0, 10))
        self.team1_var = tk.StringVar()
        self.team1_entry = ttk.Entry(
            self, textvariable=self.team1_var, style='TEntry')
        self.team1_entry.grid(row=3, column=1, sticky="ew", pady=(0, 10))

        # Team 1 validation label
        self.team1_validation = ttk.Label(
            self, text="", style='TLabel', foreground='#ff6b6b')
        self.team1_validation.grid(row=3, column=2, sticky="w", padx=(5, 0))

        # Team 2
        ttk.Label(self, text="👥 Team 2:").grid(
            row=4, column=0, sticky="e", padx=(0, 10))
        self.team2_var = tk.StringVar()
        self.team2_entry = ttk.Entry(
            self, textvariable=self.team2_var, style='TEntry')
        self.team2_entry.grid(row=4, column=1, sticky="ew", pady=(0, 10))

        # Team 2 validation label
        self.team2_validation = ttk.Label(
            self, text="", style='TLabel', foreground='#ff6b6b')
        self.team2_validation.grid(row=4, column=2, sticky="w", padx=(5, 0))

        # Score
        ttk.Label(self, text="📊 Score:").grid(
            row=5, column=0, sticky="e", padx=(0, 10))
        self.score_var = tk.StringVar()
        self.score_entry = ttk.Entry(
            self, textvariable=self.score_var, style='TEntry')
        self.score_entry.grid(row=5, column=1, sticky="ew", pady=(0, 10))

        # Date
        ttk.Label(self, text="📅 Date (YYYY-MM-DD):").grid(row=6,
                                                          column=0, sticky="e", padx=(0, 10))
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(
            self, textvariable=self.date_var, style='TEntry')
        self.date_entry.grid(row=6, column=1, sticky="ew", pady=(0, 10))

        # Add Game button
        self.add_button = ttk.Button(
            self, text="⚽ Add Game", command=self.add_game)
        self.add_button.grid(row=7, column=0, columnspan=2, pady=(20, 0))

        # Configure column weights for proper stretching
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)  # Validation column

        # Add validation labels for remaining fields
        self.league_validation = ttk.Label(
            self, text="", style='TLabel', foreground='#ff6b6b')
        self.league_validation.grid(row=2, column=2, sticky="w", padx=(5, 0))

        # Score validation
        self.score_validation = ttk.Label(
            self, text="", style='TLabel', foreground='#ff6b6b')
        self.score_validation.grid(row=5, column=2, sticky="w", padx=(5, 0))

        # Date validation
        self.date_validation = ttk.Label(
            self, text="", style='TLabel', foreground='#ff6b6b')
        self.date_validation.grid(row=6, column=2, sticky="w", padx=(5, 0))

        # Auto-complete setup
        self.setup_autocomplete()

        # Real-time validation setup
        self.setup_validation()

    def load_caches(self):
        """Load data for auto-complete caches."""
        try:
            games = self.data_manager.fetch_games()
            for game in games:
                self.team_cache.add(game['team1'])
                self.team_cache.add(game['team2'])
                self.league_cache.add(game['league'])
        except:
            pass  # Silently fail if database is empty

    def setup_autocomplete(self):
        """Setup auto-complete for team and league fields."""
        # Team 1 auto-complete
        self.team1_var.trace(
            'w', lambda *args: self.update_team1_autocomplete())

        # Team 2 auto-complete
        self.team2_var.trace(
            'w', lambda *args: self.update_team2_autocomplete())

        # League auto-complete
        self.league_var.trace(
            'w', lambda *args: self.update_league_autocomplete())

    def update_team1_autocomplete(self):
        """Update team1 auto-complete suggestions."""
        current = self.team1_var.get().lower()
        if len(current) < 2:
            return

        matches = [team for team in self.team_cache if current in team.lower()]
        if matches:
            # Show first match as suggestion (could be enhanced with dropdown)
            pass

    def update_team2_autocomplete(self):
        """Update team2 auto-complete suggestions."""
        current = self.team2_var.get().lower()
        if len(current) < 2:
            return

        matches = [team for team in self.team_cache if current in team.lower()]
        if matches:
            pass

    def update_league_autocomplete(self):
        """Update league auto-complete suggestions."""
        current = self.league_var.get().lower()
        if len(current) < 2:
            return

        matches = [
            league for league in self.league_cache if current in league.lower()]
        if matches:
            pass

    def show_templates(self):
        """Show quick game templates."""
        templates = {
            "Soccer Match": {
                "sport": "Soccer",
                "league": "Premier League",
                "team1": "Arsenal",
                "team2": "Chelsea",
                "score": "2-1",
                "date": "2024-01-15"
            },
            "Basketball Game": {
                "sport": "Basketball",
                "league": "NBA",
                "team1": "Lakers",
                "team2": "Celtics",
                "score": "105-98",
                "date": "2024-01-16"
            },
            "Champions League": {
                "sport": "Soccer",
                "league": "Champions League",
                "team1": "Real Madrid",
                "team2": "Barcelona",
                "score": "3-1",
                "date": "2024-01-17"
            }
        }

        # Create template selection dialog
        template_window = tk.Toplevel(self)
        template_window.title("Quick Game Templates")
        template_window.geometry("400x300")
        template_window.configure(bg='#1a1a1a')

        ttk.Label(template_window, text="Choose a template:",
                  style='Header.TLabel').pack(pady=20)

        for name, data in templates.items():
            btn = ttk.Button(template_window, text=name,
                             command=lambda d=data: self.apply_template(d, template_window))
            btn.pack(pady=5, padx=20, fill=tk.X)

    def apply_template(self, template_data, window):
        """Apply selected template to form."""
        self.sport_var.set(template_data["sport"])
        self.league_var.set(template_data["league"])
        self.team1_var.set(template_data["team1"])
        self.team2_var.set(template_data["team2"])
        self.score_var.set(template_data["score"])
        self.date_var.set(template_data["date"])
        window.destroy()
        messagebox.showinfo("Template Applied",
                            "Game template has been applied to the form!")

    def show_recent_teams(self):
        """Show recently used teams for quick selection."""
        if not self.team_cache:
            messagebox.showinfo("No Recent Teams",
                                "No teams found in database.")
            return

        # Create recent teams dialog
        teams_window = tk.Toplevel(self)
        teams_window.title("Recent Teams")
        teams_window.geometry("300x400")
        teams_window.configure(bg='#1a1a1a')

        ttk.Label(teams_window, text="Select Team:",
                  style='Header.TLabel').pack(pady=10)

        # Create scrollable list of teams
        frame = ttk.Frame(teams_window, style='Card.TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, bg='#2d2d2d', fg='#e0e0e0',
                             selectbackground='#00d4aa', font=('SF Pro Display', 10),
                             yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for team in sorted(self.team_cache):
            listbox.insert(tk.END, team)

        scrollbar.config(command=listbox.yview)

        # Buttons
        btn_frame = ttk.Frame(teams_window, style='TFrame')
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        ttk.Button(btn_frame, text="Set as Team 1",
                   command=lambda: self.set_team_from_list(listbox, 1, teams_window)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Set as Team 2",
                   command=lambda: self.set_team_from_list(listbox, 2, teams_window)).pack(side=tk.LEFT)

    def set_team_from_list(self, listbox, team_num, window):
        """Set selected team from list."""
        selection = listbox.curselection()
        if selection:
            team_name = listbox.get(selection[0])
            if team_num == 1:
                self.team1_var.set(team_name)
            else:
                self.team2_var.set(team_name)
            window.destroy()

    def setup_validation(self):
        """Setup real-time validation for form fields."""
        # Bind validation events
        self.team1_var.trace(
            'w', lambda *args: self.validate_field_realtime('team1'))
        self.team2_var.trace(
            'w', lambda *args: self.validate_field_realtime('team2'))
        self.league_var.trace(
            'w', lambda *args: self.validate_field_realtime('league'))
        self.score_var.trace(
            'w', lambda *args: self.validate_field_realtime('score'))
        self.date_var.trace(
            'w', lambda *args: self.validate_field_realtime('date'))

        # Bind focus out events for final validation
        self.team1_entry.bind(
            '<FocusOut>', lambda e: self.validate_field_final('team1'))
        self.team2_entry.bind(
            '<FocusOut>', lambda e: self.validate_field_final('team2'))
        self.score_entry.bind(
            '<FocusOut>', lambda e: self.validate_field_final('score'))
        self.date_entry.bind(
            '<FocusOut>', lambda e: self.validate_field_final('date'))

    def validate_field_realtime(self, field_name):
        """Real-time validation for individual fields."""
        value = self.get_field_value(field_name)
        sport = self.sport_var.get()

        if not value.strip():
            self.set_validation_message(field_name, "")
            return

        try:
            if field_name == 'team1':
                result = SportsDataValidator.validate_team_name(value, sport)
            elif field_name == 'team2':
                result = SportsDataValidator.validate_team_name(value, sport)
            elif field_name == 'league':
                result = SportsDataValidator.validate_league_name(value)
            elif field_name == 'score':
                result = SportsDataValidator.validate_score(value, sport)
            elif field_name == 'date':
                result = SportsDataValidator.validate_date(value)
            else:
                return

            self.set_validation_message(
                field_name, result.message if not result.is_valid else "")

        except Exception as e:
            self.set_validation_message(
                field_name, f"Validation error: {str(e)}")

    def validate_field_final(self, field_name):
        """Final validation when field loses focus."""
        value = self.get_field_value(field_name)

        if not value.strip():
            # Only show required message if field is empty
            if field_name in ['team1', 'team2', 'league', 'score', 'date']:
                self.set_validation_message(
                    field_name, "This field is required")
            return

        # For final validation, we might want to check cross-field validations
        if field_name in ['team1', 'team2']:
            team1 = self.team1_var.get().strip()
            team2 = self.team2_var.get().strip()

            if team1 and team2 and team1.lower() == team2.lower():
                self.set_validation_message(
                    'team2', "Teams cannot be the same")
                return

    def get_field_value(self, field_name):
        """Get the current value of a field."""
        if field_name == 'team1':
            return self.team1_var.get()
        elif field_name == 'team2':
            return self.team2_var.get()
        elif field_name == 'league':
            return self.league_var.get()
        elif field_name == 'score':
            return self.score_var.get()
        elif field_name == 'date':
            return self.date_var.get()
        return ""

    def set_validation_message(self, field_name, message):
        """Set validation message for a field."""
        label_map = {
            'team1': self.team1_validation,
            'team2': self.team2_validation,
            'league': self.league_validation,
            'score': self.score_validation,
            'date': self.date_validation
        }

        if field_name in label_map:
            label = label_map[field_name]
            if message:
                label.config(text=f"⚠️ {message}", foreground='#ff6b6b')
            else:
                label.config(text="", foreground='#00d4aa')

    def clear_all_validation_messages(self):
        """Clear all validation messages."""
        for field in ['team1', 'team2', 'league', 'score', 'date']:
            self.set_validation_message(field, "")

    def validate_entire_form(self):
        """Comprehensive validation of the entire form."""
        # Clear previous messages
        self.clear_all_validation_messages()

        # Get form data
        game_data = {
            'sport': self.sport_var.get(),
            'league': self.league_var.get().strip(),
            'team1': self.team1_var.get().strip(),
            'team2': self.team2_var.get().strip(),
            'score': self.score_var.get().strip(),
            'date': self.date_var.get().strip()
        }

        # Get existing games for duplicate checking
        try:
            existing_games = self.data_manager.fetch_games()
        except Exception:
            existing_games = []

        # Validate all fields
        validation_results = SportsDataValidator.validate_game_data(
            game_data, existing_games)

        # Set validation messages
        errors = []
        warnings = []

        for result in validation_results:
            if not result.is_valid:
                if result.severity == 'error':
                    errors.append(result.message)
                    if result.field:
                        self.set_validation_message(
                            result.field, result.message)
                elif result.severity == 'warning':
                    warnings.append(result.message)
                    if result.field:
                        self.set_validation_message(
                            result.field, f"⚠️ {result.message}")

        return errors, warnings

    def add_game(self):
        """Validate input comprehensively and add game to database."""
        # Comprehensive form validation
        errors, warnings = self.validate_entire_form()

        # Show warnings if any
        if warnings:
            warning_msg = "Warnings detected:\n" + \
                "\n".join(f"• {w}" for w in warnings)
            warning_msg += "\n\nDo you want to continue anyway?"
            if not messagebox.askyesno("Validation Warnings", warning_msg):
                return

        # Show errors if any
        if errors:
            error_msg = "Please fix the following errors:\n" + \
                "\n".join(f"• {e}" for e in errors)
            messagebox.showerror("Validation Errors", error_msg)
            return

        # Get form data (already validated)
        sport = self.sport_var.get()
        league = self.league_var.get().strip()
        team1 = self.team1_var.get().strip()
        team2 = self.team2_var.get().strip()
        score = self.score_var.get().strip()
        date = self.date_var.get().strip()

        # Create game object
        game_obj = {
            'sport': sport,
            'league': league,
            'team1': team1,
            'team2': team2,
            'score': score,
            'date': date
        }

        # Abstraction: Use the data manager interface to add game
        if self.data_manager.add_game(game_obj):
            messagebox.showinfo("Success", "Game added successfully!")
            self.clear_form()
            self.clear_all_validation_messages()
            self.game_list.refresh_games()  # Refresh the game list
            self.load_caches()  # Update auto-complete caches
        else:
            messagebox.showerror("Error", "Failed to add game!")

    def clear_form(self):
        """Clear all form fields."""
        self.team1_var.set("")
        self.team2_var.set("")
        self.score_var.set("")
        self.date_var.set("")
