"""
Main application window using Inheritance pattern.
MainApplication inherits from tk.Tk for the root window with modern design and analytics.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
import datetime

# Import matplotlib with fallback
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: Matplotlib not available. Charts will not be displayed.")

from database.interfaces import IDataManager
from config.settings import APP_CONFIG
from ui.game_form import GameForm
from ui.game_list import GameList


class MainApplication(tk.Tk):
    """
    Main Application Window.

    Root window for the Sports Management Dashboard application.
    Manages the overall application lifecycle, authentication flow,
    and main UI components with modern dark theme design.
    """

    def __init__(self, data_manager: IDataManager):
        """
        Initialize the main application window.

        Sets up the root Tkinter window, initializes data manager,
        and starts the authentication flow.

        Args:
            data_manager: Database manager instance for data operations
        """
        super().__init__()

        # Initialize data manager
        self.data_manager = data_manager
        self.current_user = None

        # Don't show main window yet - login will handle this
        self.withdraw()

        # Show login window first
        self.show_login()

    def show_login(self):
        """
        Display the login window for user authentication.

        Creates and shows the LoginWindow modal dialog.
        Upon successful login, calls initialize_main_app().
        """
        from ui.auth import LoginWindow

        def on_login_success(user_data):
            """
            Handle successful user login.

            Called by LoginWindow when authentication succeeds.
            Stores user data and initializes the main application.

            Args:
                user_data: Dictionary containing authenticated user information
            """
            self.current_user = user_data
            self.initialize_main_app()

        LoginWindow(self, self.data_manager, on_login_success)

    def initialize_main_app(self):
        """Initialize the main application after successful login."""
        # Setup main window
        self.title(
            f"{APP_CONFIG['title']} - Logged in as {self.current_user['username']}")
        self.geometry("1400x900")
        self.resizable(True, True)

        # Apply dark theme
        self._setup_dark_theme()

        # Create status bar variable
        self.status_var = tk.StringVar()
        self.status_var.set(
            f"Logged in as {self.current_user['username']} - Press F1 for help")

        # Setup UI
        self.setup_ui()

        # Show the main window
        self.deiconify()

    def _setup_dark_theme(self):
        """Setup the complete dark theme for the main application."""
        self.style = ttk.Style()
        self.configure(bg='#1a1a1a')

        # Main application styling
        self.style.configure('TFrame', background='#1a1a1a')
        self.style.configure('TLabel',
                             background='#1a1a1a',
                             foreground='#e0e0e0',
                             font=('SF Pro Display', 10))
        self.style.configure('TButton',
                             font=('SF Pro Display', 10, 'bold'),
                             padding=[12, 8],
                             relief='flat',
                             borderwidth=0)
        self.style.map('TButton',
                       background=[('active', '#007acc'),
                                   ('pressed', '#005999')],
                       foreground=[('active', '#ffffff'),
                                   ('pressed', '#cccccc')])

        # Modern card styling with subtle borders
        self.style.configure('Card.TFrame',
                             background='#2d2d2d',
                             relief='solid',
                             borderwidth=1,
                             lightcolor='#404040',
                             darkcolor='#404040')

        # Header styling - modern and clean
        self.style.configure('Header.TLabel',
                             font=('SF Pro Display', 18, 'bold'),
                             foreground='#00d4aa',
                             background='#2d2d2d')

        # Statistics label styling
        self.style.configure('Stats.TLabel',
                             font=('SF Pro Display', 13, 'bold'),
                             foreground='#ff6b6b',
                             background='#2d2d2d')

        # Modern notebook styling
        self.style.configure('TNotebook',
                             background='#1a1a1a',
                             borderwidth=0,
                             tabmargins=[0, 0, 0, 0])
        self.style.configure('TNotebook.Tab',
                             background='#333333',
                             foreground='#cccccc',
                             font=('SF Pro Display', 11),
                             padding=[20, 10],
                             relief='flat',
                             borderwidth=0,
                             focuscolor='#00d4aa')
        self.style.map('TNotebook.Tab',
                       background=[('selected', '#00d4aa'),
                                   ('active', '#404040')],
                       foreground=[('selected', '#ffffff'),
                                   ('active', '#ffffff')],
                       relief=[('selected', 'flat'),
                               ('active', 'flat')])

        # Entry field styling
        self.style.configure('TEntry',
                             fieldbackground='#404040',
                             borderwidth=1,
                             relief='solid',
                             insertcolor='#00d4aa',
                             font=('SF Pro Display', 10))
        self.style.map('TEntry',
                       fieldbackground=[('focus', '#4a4a4a'),
                                        ('!focus', '#404040')])

        # Combobox styling
        self.style.configure('TCombobox',
                             fieldbackground='#404040',
                             background='#404040',
                             borderwidth=1,
                             relief='solid',
                             font=('SF Pro Display', 10))
        self.style.map('TCombobox',
                       fieldbackground=[('focus', '#4a4a4a'),
                                        ('!focus', '#404040')],
                       background=[('focus', '#4a4a4a'),
                                   ('!focus', '#404040')])

        # Modern scrollbar styling
        self.style.configure('TScrollbar',
                             background='#404040',
                             troughcolor='#2d2d2d',
                             borderwidth=0,
                             arrowcolor='#cccccc')
        self.style.map('TScrollbar',
                       background=[('active', '#4a4a4a')])

    def setup_ui(self):
        """Set up the main UI components with modern design."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create components
        self.game_list = GameList(self.notebook, self.data_manager)
        self.game_form = GameForm(
            self.notebook, self.data_manager, self.game_list)
        self.analytics_dashboard = AnalyticsDashboard(
            self.notebook, self.data_manager)

        # Add tabs with icons (text-based)
        self.notebook.add(self.game_form, text="➕ Add Game")
        self.notebook.add(self.game_list, text="📋 Games List")
        self.notebook.add(self.analytics_dashboard, text="📊 Analytics")

        # Status bar
        self.create_status_bar()

        # Load initial data
        self.game_list.refresh_games()
        self.analytics_dashboard.refresh_analytics()

        # Bind refresh events
        self.bind('<F5>', lambda e: self.refresh_all())
        self.bind('<Control-r>', lambda e: self.refresh_all())
        self.bind('<Control-n>', lambda e: self.focus_tab(0))  # Add Game
        self.bind('<Control-l>', lambda e: self.focus_tab(1))  # Games List
        self.bind('<Control-a>', lambda e: self.focus_tab(2))  # Analytics
        self.bind('<Control-q>', lambda e: self.quit_app())
        self.bind('<F1>', lambda e: self.show_help())

    def refresh_all(self):
        """Refresh all components."""
        self.game_list.refresh_games()
        self.analytics_dashboard.refresh_analytics()
        messagebox.showinfo("Refreshed", "All data has been refreshed!")

    def focus_tab(self, tab_index):
        """Focus on a specific tab."""
        self.notebook.select(tab_index)

    def quit_app(self):
        """Quit the application with confirmation."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.quit()

    def create_status_bar(self):
        """Create modern status bar with shortcuts info."""
        status_frame = ttk.Frame(self, style='Card.TFrame')
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        # Status indicator
        status_indicator = tk.Canvas(status_frame, width=12, height=12,
                                     bg='#2d2d2d', highlightthickness=0)
        status_indicator.create_oval(2, 2, 10, 10, fill='#00d4aa')
        status_indicator.pack(side=tk.LEFT, padx=(10, 5), pady=8)

        # Status label
        status_label = ttk.Label(
            status_frame, textvariable=self.status_var, anchor='w')
        status_label.pack(side=tk.LEFT, pady=5)

        # Database indicator
        db_indicator = tk.Canvas(status_frame, width=12, height=12,
                                 bg='#2d2d2d', highlightthickness=0)
        db_indicator.create_oval(2, 2, 10, 10, fill='#4CAF50')
        db_indicator.pack(side=tk.RIGHT, padx=(10, 5), pady=8)

        # Database status
        db_label = ttk.Label(status_frame, text="MySQL Connected", anchor='e')
        db_label.pack(side=tk.RIGHT, pady=5)

        # Keyboard shortcuts
        shortcuts_frame = ttk.Frame(status_frame, style='TFrame')
        shortcuts_frame.pack(side=tk.RIGHT, padx=20, pady=5)

        shortcuts = ["F1: Help", "F5: Refresh", "Ctrl+N: Add",
                     "Ctrl+L: List", "Ctrl+A: Analytics", "Ctrl+Q: Quit"]
        for shortcut in shortcuts:
            ttk.Label(shortcuts_frame, text=shortcut,
                      font=('SF Pro Display', 8), foreground='#888888').pack(side=tk.LEFT, padx=5)

    def show_help(self):
        """Show keyboard shortcuts and help."""
        help_text = """
🎯 Sports Management Dashboard - Keyboard Shortcuts

📋 Navigation:
  • Ctrl+N: Switch to Add Game tab
  • Ctrl+L: Switch to Games List tab
  • Ctrl+A: Switch to Analytics tab

🔄 Actions:
  • F5: Refresh all data
  • Ctrl+R: Refresh all data
  • Ctrl+S (in Add Game): Save game
  • Ctrl+Q: Quit application

🎮 Games List:
  • Double-click: Edit selected game
  • Delete key: Delete selected game
  • Right-click: Context menu
  • Enter: Edit selected game

⚡ Productivity Features:
  • Quick Templates: Pre-filled game forms
  • Recent Teams: Quick team selection
  • Auto-complete: Smart suggestions
  • Real-time Search: Instant filtering
  • CSV Export: Data export functionality
  • Analytics Dashboard: Real-time statistics

💡 Tips:
  • Use search bar for instant filtering
  • Sort by clicking column headers
  • Export filtered results to CSV
  • Templates save time for common games
        """

        help_window = tk.Toplevel(self)
        help_window.title("Help & Shortcuts")
        help_window.geometry("600x500")
        help_window.configure(bg='#1a1a1a')

        # Text widget with scrollbar
        text_frame = ttk.Frame(help_window, style='Card.TFrame')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, bg='#2d2d2d', fg='#e0e0e0',
                              font=('SF Pro Display', 10), yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text.strip())
        text_widget.config(state=tk.DISABLED)

        scrollbar.config(command=text_widget.yview)

        # Close button
        ttk.Button(help_window, text="Close",
                   command=help_window.destroy).pack(pady=(0, 20))

    def run(self):
        """Start the application main loop."""
        self.mainloop()


class AnalyticsDashboard(ttk.Frame):
    """
    Analytics Dashboard Widget.

    Displays real-time statistics and visualizations for sports games data.
    Includes pie charts for sport distribution and bar charts for trends.
    Uses matplotlib for chart rendering with dark theme styling.
    """

    def __init__(self, parent, data_manager: IDataManager):
        # Create styles before initializing the frame
        self.setup_styles()

        super().__init__(parent, style='Card.TFrame')

        self.data_manager = data_manager
        self.stats_labels = {}
        self.setup_dashboard()

    def setup_styles(self):
        """Setup modern ttk styles for the analytics dashboard."""
        try:
            self.style = ttk.Style()
            # Modern card styling
            self.style.configure('Card.TFrame',
                                 background='#2d2d2d',
                                 relief='solid',
                                 borderwidth=1,
                                 lightcolor='#404040',
                                 darkcolor='#404040')
            # Modern header
            self.style.configure('Header.TLabel',
                                 font=('SF Pro Display', 18, 'bold'),
                                 foreground='#00d4aa',
                                 background='#2d2d2d')
            # Modern stats labels
            self.style.configure('Stats.TLabel',
                                 font=('SF Pro Display', 13, 'bold'),
                                 foreground='#ff6b6b',
                                 background='#2d2d2d')
            # Modern regular labels
            self.style.configure('TLabel',
                                 background='#2d2d2d',
                                 foreground='#e0e0e0',
                                 font=('SF Pro Display', 10))
            # Modern buttons
            self.style.configure('TButton',
                                 font=('SF Pro Display', 10, 'bold'),
                                 padding=[12, 8],
                                 relief='flat',
                                 borderwidth=0)
            self.style.map('TButton',
                           background=[('active', '#007acc'),
                                       ('pressed', '#005999')],
                           foreground=[('active', '#ffffff'),
                                       ('pressed', '#cccccc')])
        except Exception as e:
            # Fallback styling if modern styles fail
            print(f"Warning: Could not setup modern styles: {e}")
            try:
                self.style.configure(
                    'Card.TFrame', background='#2d2d2d', relief='solid', borderwidth=1)
                self.style.configure('Header.TLabel', font=(
                    'Arial', 16, 'bold'), foreground='#00d4aa')
                self.style.configure('Stats.TLabel', font=(
                    'Arial', 12, 'bold'), foreground='#ff6b6b')
            except:
                pass

    def setup_dashboard(self):
        """Set up the analytics dashboard."""
        # Header
        try:
            header = ttk.Label(self, text="📊 Sports Analytics Dashboard",
                               style='Header.TLabel')
        except Exception:
            # Fallback to basic label
            header = tk.Label(self, text="📊 Sports Analytics Dashboard",
                              fg='#00d4aa', bg='#1a1a1a', font=('SF Pro Display', 16, 'bold'))

        header.pack(pady=(20, 30))

        # Stats cards container
        try:
            stats_frame = ttk.Frame(self, style='TFrame')
        except Exception:
            stats_frame = tk.Frame(self, bg='#2d2d2d')

        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Create stats cards
        self.create_stats_cards(stats_frame)

        # Charts container
        try:
            charts_frame = ttk.Frame(self, style='TFrame')
        except Exception:
            charts_frame = tk.Frame(self, bg='#2d2d2d')

        charts_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Create charts
        self.create_charts(charts_frame)

        # Store canvas references for proper cleanup
        self.sports_canvas = None
        self.trends_canvas = None

        # Refresh button
        try:
            refresh_btn = ttk.Button(self, text="🔄 Refresh Analytics",
                                     command=self.refresh_analytics)
        except Exception:
            refresh_btn = tk.Button(self, text="🔄 Refresh Analytics",
                                    command=self.refresh_analytics, bg='#00d4aa', fg='white')

        refresh_btn.pack(pady=(0, 20))

    def create_stats_cards(self, parent):
        """Create statistics cards."""
        # Stats data structure
        stats_config = [
            ("Total Games", "total_games", "#00d4aa"),
            ("Active Teams", "active_teams", "#ff6b6b"),
            ("Win Rate", "win_rate", "#4ecdc4"),
            ("Avg Goals/Game", "avg_goals", "#45b7d1"),
            ("Recent Games", "recent_games", "#f9ca24"),
            ("Top League", "top_league", "#f0932b")
        ]

        # Configure grid weights for all columns first
        try:
            for col in range(3):
                parent.grid_columnconfigure(col, weight=1)
        except Exception as e:
            # If grid_columnconfigure fails, continue without it
            print(f"Warning: Could not configure grid columns: {e}")
            pass

        # Create grid layout for cards
        for i, (label, key, color) in enumerate(stats_config):
            row, col = i // 3, i % 3

            # Card frame - use basic Frame if styled version fails
            try:
                card = ttk.Frame(parent, style='Card.TFrame')
            except Exception:
                # Fallback to basic frame
                card = tk.Frame(parent, bg='#3a3a3a',
                                relief='raised', borderwidth=2)

            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

            # Value label
            try:
                value_label = ttk.Label(card, text="0", font=('Segoe UI', 24, 'bold'),
                                        foreground=color)
            except Exception:
                # Fallback to basic label
                value_label = tk.Label(card, text="0", font=('Arial', 24, 'bold'),
                                       fg=color, bg='#3a3a3a')

            value_label.pack(pady=(15, 5))

            # Title label
            try:
                title_label = ttk.Label(card, text=label, style='TLabel')
            except Exception:
                # Fallback to basic label
                title_label = tk.Label(card, text=label, fg='white', bg='#3a3a3a',
                                       font=('Arial', 10))

            title_label.pack(pady=(0, 15))

            self.stats_labels[key] = value_label

    def create_charts(self, parent):
        """Create data visualization charts."""
        # Sports distribution chart
        try:
            sports_frame = ttk.Frame(parent, style='Card.TFrame')
            sports_label = ttk.Label(
                sports_frame, text="Games by Sport", style='Header.TLabel')
            self.sports_canvas_frame = ttk.Frame(sports_frame, style='TFrame')
        except Exception:
            sports_frame = tk.Frame(
                parent, bg='#3a3a3a', relief='raised', borderwidth=2)
            sports_label = tk.Label(sports_frame, text="Games by Sport", fg='#00d4aa', bg='#3a3a3a',
                                    font=('Arial', 12, 'bold'))
            self.sports_canvas_frame = tk.Frame(sports_frame, bg='#3a3a3a')

        sports_frame.pack(side=tk.LEFT, fill=tk.BOTH,
                          expand=True, padx=(0, 10))
        sports_label.pack(pady=10)
        self.sports_canvas_frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Monthly trends chart
        try:
            trends_frame = ttk.Frame(parent, style='Card.TFrame')
            trends_label = ttk.Label(
                trends_frame, text="Monthly Trends", style='Header.TLabel')
            self.trends_canvas_frame = ttk.Frame(trends_frame, style='TFrame')
        except Exception:
            trends_frame = tk.Frame(
                parent, bg='#3a3a3a', relief='raised', borderwidth=2)
            trends_label = tk.Label(trends_frame, text="Monthly Trends", fg='#00d4aa', bg='#3a3a3a',
                                    font=('Arial', 12, 'bold'))
            self.trends_canvas_frame = tk.Frame(trends_frame, bg='#3a3a3a')

        trends_frame.pack(side=tk.RIGHT, fill=tk.BOTH,
                          expand=True, padx=(10, 0))
        trends_label.pack(pady=10)
        self.trends_canvas_frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def refresh_analytics(self):
        """Refresh all analytics data."""
        try:
            games = self.data_manager.fetch_games()
            if games is None:
                games = []  # Ensure we have a list even if fetch fails
            self.update_stats(games)
            self.update_charts(games)
        except Exception as e:
            # Show error but don't crash the application
            print(f"Analytics refresh error: {e}")
            # Try to show at least empty stats
            try:
                self.update_stats([])
                self.update_charts([])
            except Exception:
                pass  # If even that fails, just continue

    def update_stats(self, games):
        """Update statistics cards."""
        if not games:
            # Reset all labels to 0
            for label in self.stats_labels.values():
                label.config(text="0")
            return

        # Calculate statistics
        total_games = len(games)

        # Active teams
        teams = set()
        for game in games:
            teams.add(game['team1'])
            teams.add(game['team2'])
        active_teams = len(teams)

        # Win rate calculation (percentage of games that have a winner vs draws)
        decisive_games = sum(
            1 for game in games if self._determine_winner(game) is not None)
        win_rate = f"{(decisive_games/total_games*100):.1f}%" if total_games > 0 else "0%"

        # Average goals per game
        total_goals = 0
        games_with_scores = 0
        for game in games:
            try:
                score_parts = game['score'].split('-')
                if len(score_parts) == 2:
                    goals = int(score_parts[0]) + int(score_parts[1])
                    total_goals += goals
                    games_with_scores += 1
            except (ValueError, IndexError):
                continue
        avg_goals = f"{(total_goals/games_with_scores):.1f}" if games_with_scores > 0 else "0.0"

        # Recent games (last 30 days)
        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        recent_games = 0
        for game in games:
            try:
                # Handle both string and date/datetime objects
                if isinstance(game['date'], str):
                    game_date = datetime.datetime.strptime(
                        game['date'], '%Y-%m-%d')
                elif isinstance(game['date'], (datetime.date, datetime.datetime)):
                    game_date = game['date']
                    if isinstance(game_date, datetime.date) and not isinstance(game_date, datetime.datetime):
                        game_date = datetime.datetime.combine(
                            game_date, datetime.time.min)
                else:
                    continue

                if game_date > thirty_days_ago:
                    recent_games += 1
            except (ValueError, KeyError, TypeError):
                continue

        # Top league
        league_counts = defaultdict(int)
        for game in games:
            league_counts[game['league']] += 1
        top_league = max(league_counts.items(), key=lambda x: x[1])[
            0] if league_counts else "None"

        # Update labels safely
        try:
            if 'total_games' in self.stats_labels:
                self.stats_labels['total_games'].config(text=str(total_games))
            if 'active_teams' in self.stats_labels:
                self.stats_labels['active_teams'].config(
                    text=str(active_teams))
            if 'win_rate' in self.stats_labels:
                self.stats_labels['win_rate'].config(text=win_rate)
            if 'avg_goals' in self.stats_labels:
                self.stats_labels['avg_goals'].config(text=avg_goals)
            if 'recent_games' in self.stats_labels:
                self.stats_labels['recent_games'].config(
                    text=str(recent_games))
            if 'top_league' in self.stats_labels:
                self.stats_labels['top_league'].config(text=top_league)
        except (KeyError, tk.TclError) as e:
            # Handle case where labels might not be initialized or destroyed
            print(f"Warning: Could not update stats labels: {e}")
            pass

    def update_charts(self, games):
        """Update data visualization charts."""
        # Clear existing charts and properly dispose of matplotlib figures
        self._clear_chart_frame(self.sports_canvas_frame)
        self._clear_chart_frame(self.trends_canvas_frame)

        if not games:
            return

        # Sports distribution chart
        self.create_sports_chart(games)

        # Monthly trends chart
        self.create_trends_chart(games)

    def _clear_chart_frame(self, frame):
        """Clear all widgets from a chart frame and properly dispose of matplotlib figures."""
        # Properly dispose of stored canvas references
        if hasattr(self, 'sports_canvas') and self.sports_canvas is not None:
            try:
                self.sports_canvas.figure.clear()
                plt.close(self.sports_canvas.figure)
            except (AttributeError, RuntimeError):
                pass
            self.sports_canvas = None

        if hasattr(self, 'trends_canvas') and self.trends_canvas is not None:
            try:
                self.trends_canvas.figure.clear()
                plt.close(self.trends_canvas.figure)
            except (AttributeError, RuntimeError):
                pass
            self.trends_canvas = None

        # Clear all widgets from the frame
        for widget in frame.winfo_children():
            try:
                widget.destroy()
            except (tk.TclError, RuntimeError):
                # Widget might already be destroyed
                pass

    def create_sports_chart(self, games):
        """Create sports distribution pie chart."""
        if not MATPLOTLIB_AVAILABLE:
            error_label = tk.Label(self.sports_canvas_frame,
                                   text="Matplotlib not available.\nInstall with: pip install matplotlib",
                                   bg='#2d2d2d', fg='#ff6b6b', font=('SF Pro Display', 10))
            error_label.pack(pady=20)
            return

        try:
            sport_counts = defaultdict(int)
            for game in games:
                sport_counts[game['sport']] += 1

            if not sport_counts:
                return

            # Create figure with dark theme
            fig, ax = plt.subplots(figsize=(6, 4), facecolor='#1a1a1a')
            ax.set_facecolor('#2d2d2d')

            colors = ['#00d4aa', '#ff6b6b', '#4ecdc4',
                      '#45b7d1', '#f9ca24', '#f0932b']

            wedges, texts, autotexts = ax.pie(sport_counts.values(),
                                              labels=sport_counts.keys(),
                                              autopct='%1.1f%%',
                                              colors=colors[:len(
                                                  sport_counts)],
                                              textprops={'color': 'white', 'fontsize': 10})

            ax.set_title('Games by Sport', color='white', fontsize=12, pad=20)

            # Add chart to canvas
            self.sports_canvas = FigureCanvasTkAgg(
                fig, master=self.sports_canvas_frame)
            self.sports_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.sports_canvas.draw()

        except Exception as e:
            # Handle matplotlib/chart creation errors gracefully
            error_label = tk.Label(self.sports_canvas_frame,
                                   text=f"Chart Error: {str(e)}",
                                   bg='#2d2d2d', fg='#ff6b6b', font=('SF Pro Display', 10))
            error_label.pack(pady=20)
            print(f"Sports chart creation error: {e}")

    def create_trends_chart(self, games):
        """Create monthly trends bar chart."""
        if not MATPLOTLIB_AVAILABLE:
            error_label = tk.Label(self.trends_canvas_frame,
                                   text="Matplotlib not available.\nInstall with: pip install matplotlib",
                                   bg='#2d2d2d', fg='#ff6b6b', font=('SF Pro Display', 10))
            error_label.pack(pady=20)
            return

        try:
            monthly_counts = defaultdict(int)

            for game in games:
                try:
                    # Handle both string and date/datetime objects
                    if isinstance(game['date'], str):
                        date = datetime.datetime.strptime(
                            game['date'], '%Y-%m-%d')
                    elif isinstance(game['date'], (datetime.date, datetime.datetime)):
                        date = game['date']
                        if isinstance(date, datetime.date) and not isinstance(date, datetime.datetime):
                            date = datetime.datetime.combine(
                                date, datetime.time.min)
                    else:
                        continue

                    month_key = f"{date.year}-{date.month:02d}"
                    monthly_counts[month_key] += 1
                except (ValueError, KeyError, TypeError):
                    continue

            if not monthly_counts:
                return

            # Sort by date
            sorted_months = sorted(monthly_counts.keys())
            counts = [monthly_counts[month] for month in sorted_months]

            # Create figure with dark theme
            fig, ax = plt.subplots(figsize=(6, 4), facecolor='#1a1a1a')
            ax.set_facecolor('#2d2d2d')

            bars = ax.bar(range(len(sorted_months)), counts,
                          color='#00d4aa', alpha=0.8, edgecolor='#00d4aa', linewidth=2)

            ax.set_xlabel('Month', color='white', fontsize=10)
            ax.set_ylabel('Games Count', color='white', fontsize=10)
            ax.set_title('Monthly Game Trends',
                         color='white', fontsize=12, pad=20)
            ax.set_xticks(range(len(sorted_months)))
            ax.set_xticklabels(sorted_months, rotation=45,
                               ha='right', color='white')
            ax.tick_params(colors='white')

            # Add value labels on bars
            for bar, count in zip(bars, counts):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(count), ha='center', va='bottom', color='white', fontweight='bold')

            plt.tight_layout()

            # Add chart to canvas
            self.trends_canvas = FigureCanvasTkAgg(
                fig, master=self.trends_canvas_frame)
            self.trends_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.trends_canvas.draw()

        except Exception as e:
            # Handle matplotlib/chart creation errors gracefully
            error_label = tk.Label(self.trends_canvas_frame,
                                   text=f"Chart Error: {str(e)}",
                                   bg='#2d2d2d', fg='#ff6b6b', font=('SF Pro Display', 10))
            error_label.pack(pady=20)
            print(f"Trends chart creation error: {e}")

    def _determine_winner(self, game):
        """Determine winner from game score (simplified logic)."""
        try:
            score_parts = game['score'].split('-')
            if len(score_parts) == 2:
                score1 = int(score_parts[0])
                score2 = int(score_parts[1])
                if score1 > score2:
                    return game['team1']
                elif score2 > score1:
                    return game['team2']
        except (ValueError, IndexError):
            pass
        return None
