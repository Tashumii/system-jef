"""
Main application window using Inheritance pattern.
MainApplication inherits from tk.Tk for the root window with modern design and analytics.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import defaultdict
import datetime
import json

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
    Theme: Casual Cyan-Green (Eco-Modern)
    """

    def __init__(self, data_manager: IDataManager):
        super().__init__()

        self.data_manager = data_manager
        self.current_user = None

        self.withdraw()
        self.show_login()

    def show_login(self):
        """Display the login window for user authentication."""
        from ui.auth import LoginWindow

        def on_login_success(user_data):
            self.current_user = user_data
            self.initialize_main_app()

        LoginWindow(self, self.data_manager, on_login_success)

    def initialize_main_app(self):
        """Initialize the main application after successful login."""
        self.title(f"{APP_CONFIG['title']} - {self.current_user['username']}")
        self.geometry("1300x850")  # Consistent casual size
        self.resizable(True, True)

        # Apply Theme
        self._setup_theme()

        # Create Menu Bar
        self.create_menu()

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set(f"Ready • {datetime.datetime.now().strftime('%B %d, %Y')}")

        self.setup_ui()
        self.deiconify()

    def _setup_theme(self):
        """Setup the Casual Cyan-Green Theme (Eco-Modern)."""
        self.style = ttk.Style()

        # --- Palette Definition ---
        BG_MAIN = '#182421'      # Deep Slate Green
        BG_CARD = '#23332e'      # Lighter Slate Green for cards
        FG_TEXT = '#e8f5e9'      # Soft White/Mint
        ACCENT  = '#26a69a'      # Teal/Cyan-Green
        ACTIVE  = '#00897b'      # Darker Teal for active states
        FONT_MAIN = ('Segoe UI', 10)
        FONT_HEAD = ('Segoe UI', 16, 'bold')

        self.configure(bg=BG_MAIN)
        self.style.theme_use('clam')

        # Frames and Labels
        self.style.configure('TFrame', background=BG_MAIN)
        self.style.configure('TLabel', background=BG_MAIN, foreground=FG_TEXT, font=FONT_MAIN)

        # Cards
        self.style.configure('Card.TFrame', background=BG_CARD, relief='flat', borderwidth=0)

        # Headers
        self.style.configure('Header.TLabel', font=FONT_HEAD, foreground=ACCENT, background=BG_CARD)
        self.style.configure('Stats.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#66bb6a', background=BG_CARD)

        # Buttons
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), background=ACCENT, foreground='white',
                             borderwidth=0, focuscolor=BG_CARD, padding=(15, 8))
        self.style.map('TButton', background=[('active', ACTIVE), ('pressed', '#004d40')])

        # Notebook (Tabs)
        self.style.configure('TNotebook', background=BG_MAIN, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=BG_MAIN, foreground='#b0bec5', padding=(20, 12), font=('Segoe UI', 11))
        self.style.map('TNotebook.Tab', background=[('selected', BG_CARD)], foreground=[('selected', ACCENT)])

        # Inputs
        self.style.configure('TEntry', fieldbackground='#2c3e39', foreground='white', insertcolor='white', borderwidth=0, padding=5)
        self.style.map('TEntry', fieldbackground=[('focus', '#2c3e39')])

        self.style.configure('TCombobox', fieldbackground='#2c3e39', background=ACCENT, foreground='white', arrowcolor='white', borderwidth=0, padding=5)
        self.style.map('TCombobox', fieldbackground=[('readonly', '#2c3e39')])

        # Scrollbars
        self.style.configure('TScrollbar', background=BG_CARD, troughcolor=BG_MAIN, borderwidth=0, arrowcolor=ACCENT)
        self.style.map('TScrollbar', background=[('active', ACCENT)])

    def create_menu(self):
        """Create top system menu with custom green styling."""
        # Menu colors need to be set on the widget itself, ttk doesn't control native menus easily
        menubar = tk.Menu(self, bg='#23332e', fg='#e8f5e9', activebackground='#26a69a', activeforeground='white', relief='flat')

        file_menu = tk.Menu(menubar, tearoff=0, bg='#23332e', fg='#e8f5e9', activebackground='#26a69a', activeforeground='white')
        file_menu.add_command(label="💾  Backup Database", command=self.backup_data)
        file_menu.add_separator()
        file_menu.add_command(label="🚪  Logout", command=self.quit_app)
        file_menu.add_command(label="❌  Exit", command=self.quit)
        menubar.add_cascade(label="  File  ", menu=file_menu)

        tools_menu = tk.Menu(menubar, tearoff=0, bg='#23332e', fg='#e8f5e9', activebackground='#26a69a', activeforeground='white')
        tools_menu.add_command(label="🔄  Refresh All", command=self.refresh_all)
        menubar.add_cascade(label="  Tools  ", menu=tools_menu)

        self.config(menu=menubar)

    def backup_data(self):
        """Backup all games to a JSON file."""
        try:
            games = self.data_manager.fetch_games()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                initialfile=f"backup_{timestamp}.json",
                filetypes=[("JSON Files", "*.json")],
                title="Save Backup"
            )

            if filename:
                serializable_games = []
                for g in games:
                    g_copy = g.copy()
                    if isinstance(g_copy.get('date'), (datetime.date, datetime.datetime)):
                        g_copy['date'] = str(g_copy['date'])
                    # Cleanup keys
                    for k in ['created_at', 'updated_at']:
                        if k in g_copy: del g_copy[k]
                    serializable_games.append(g_copy)

                with open(filename, 'w') as f:
                    json.dump({"data": serializable_games, "meta": {"exported_at": timestamp}}, f, indent=4)

                messagebox.showinfo("Backup Successful", f"Saved {len(games)} records.")
        except Exception as e:
            messagebox.showerror("Backup Failed", f"Error: {str(e)}")

    def setup_ui(self):
        """Set up the main UI components."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Components
        self.game_list = GameList(self.notebook, self.data_manager)
        self.game_form = GameForm(self.notebook, self.data_manager, self.game_list)
        self.analytics_dashboard = AnalyticsDashboard(self.notebook, self.data_manager)

        # Tabs with spacing
        self.notebook.add(self.game_form, text="  ➕ New Entry  ")
        self.notebook.add(self.game_list, text="  📋 Records  ")
        self.notebook.add(self.analytics_dashboard, text="  📊 Insights  ")

        self.create_status_bar()

        # Load initial data
        self.refresh_all()

        # Bind refresh events
        self.bind('<F5>', lambda e: self.refresh_all())
        self.bind('<Control-r>', lambda e: self.refresh_all())
        self.bind('<Control-q>', lambda e: self.quit_app())
        self.bind('<F1>', lambda e: self.show_help())

    def refresh_all(self):
        self.game_list.refresh_games()
        self.analytics_dashboard.refresh_analytics()

    def quit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()

    def create_status_bar(self):
        """Create modern status bar."""
        status_frame = ttk.Frame(self, style='Card.TFrame')
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Status label
        ttk.Label(status_frame, textvariable=self.status_var,
                  foreground='#80cbc4', font=('Segoe UI', 9), background='#23332e').pack(side=tk.LEFT, padx=15, pady=8)

        # Database status
        ttk.Label(status_frame, text="Connected to Database",
                  foreground='#80cbc4', font=('Segoe UI', 9), background='#23332e').pack(side=tk.RIGHT, padx=15, pady=8)

    def show_help(self):
        """Show keyboard shortcuts."""
        help_text = """
🎯 Shortcuts:
• F5 / Ctrl+R : Refresh Data
• Ctrl+Q : Exit
• Ctrl+S : Save (in form)
        """
        messagebox.showinfo("Help", help_text)


class AnalyticsDashboard(ttk.Frame):
    """
    Analytics Dashboard Widget.
    Theme: Casual Cyan-Green
    """

    def __init__(self, parent, data_manager: IDataManager):
        super().__init__(parent, style='Card.TFrame')
        self.data_manager = data_manager
        self.stats_labels = {}
        self.setup_dashboard()

    def setup_dashboard(self):
        # Header
        try:
            header = ttk.Label(self, text="Performance Overview", style='Header.TLabel')
        except:
            header = tk.Label(self, text="Performance Overview", fg='#26a69a', bg='#23332e', font=('Segoe UI', 16, 'bold'))
        header.pack(pady=(25, 20))

        # Stats container
        stats_frame = ttk.Frame(self, style='Card.TFrame')
        stats_frame.pack(fill=tk.X, padx=30, pady=10)

        self.create_stats_cards(stats_frame)

        # Charts container
        charts_frame = ttk.Frame(self, style='Card.TFrame')
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        self.create_charts(charts_frame)
        self.sports_canvas = None
        self.trends_canvas = None

        # Refresh button
        ttk.Button(self, text="Refresh Data", command=self.refresh_analytics).pack(pady=10)

    def create_stats_cards(self, parent):
        """Create casual statistics cards."""
        metrics = [
            ("Total Games", "total_games", "#26a69a"),
            ("Active Teams", "active_teams", "#66bb6a"),
            ("Win Rate", "win_rate", "#29b6f6"),
            ("Avg Score", "avg_goals", "#ffa726")
        ]

        for i in range(4): parent.columnconfigure(i, weight=1)

        for col, (title, key, color) in enumerate(metrics):
            # Card styling using standard Frame for background control
            card = tk.Frame(parent, bg='#2c3e39', padx=20, pady=15)
            card.grid(row=0, column=col, padx=10, sticky='ew')

            # Value
            val = tk.Label(card, text="0", font=('Segoe UI', 26, 'bold'), fg=color, bg='#2c3e39')
            val.pack()
            self.stats_labels[key] = val

            # Title
            tk.Label(card, text=title, font=('Segoe UI', 10), fg='#b0bec5', bg='#2c3e39').pack()

    def create_charts(self, parent):
        # Left and Right frames for charts
        self.sports_frame = tk.Frame(parent, bg='#23332e')
        self.sports_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.trends_frame = tk.Frame(parent, bg='#23332e')
        self.trends_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

    def refresh_analytics(self):
        try:
            games = self.data_manager.fetch_games() or []
            self.update_stats(games)
            self.update_charts(games)
        except Exception as e:
            print(f"Analytics error: {e}")

    def update_stats(self, games):
        if not games: return

        total = len(games)
        teams = set()
        goals = 0
        valid_scores = 0

        for g in games:
            teams.add(g['team1'])
            teams.add(g['team2'])
            try:
                s1, s2 = map(int, g['score'].split('-'))
                goals += (s1 + s2)
                valid_scores += 1
            except: pass

        avg = f"{(goals/valid_scores):.1f}" if valid_scores else "0.0"

        self.stats_labels['total_games'].config(text=str(total))
        self.stats_labels['active_teams'].config(text=str(len(teams)))
        self.stats_labels['win_rate'].config(text="100%") # Placeholder
        self.stats_labels['avg_goals'].config(text=avg)

    def update_charts(self, games):
        # Clear old charts
        if self.sports_canvas:
            self.sports_canvas.get_tk_widget().destroy()
            plt.close(self.sports_canvas.figure)
        if self.trends_canvas:
            self.trends_canvas.get_tk_widget().destroy()
            plt.close(self.trends_canvas.figure)

        if not games or not MATPLOTLIB_AVAILABLE: return

        # Theme Colors
        colors = ['#26a69a', '#66bb6a', '#29b6f6', '#ffa726', '#ef5350', '#ab47bc']
        bg_color = '#23332e'
        text_color = '#e8f5e9'

        # 1. Pie Chart
        counts = defaultdict(int)
        for g in games: counts[g['sport']] += 1

        fig1, ax1 = plt.subplots(figsize=(5, 4), facecolor=bg_color)
        ax1.pie(counts.values(), labels=counts.keys(), colors=colors, autopct='%1.1f%%',
                textprops={'color': text_color})
        ax1.set_title('Games by Sport', color=text_color)

        self.sports_canvas = FigureCanvasTkAgg(fig1, self.sports_frame)
        self.sports_canvas.draw()
        self.sports_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 2. Bar Chart
        dates = defaultdict(int)
        for g in games:
            try:
                d = g['date']
                if isinstance(d, str): d = datetime.datetime.strptime(d, '%Y-%m-%d')
                dates[d.strftime('%Y-%m')] += 1
            except: pass

        if dates:
            s_dates = sorted(dates.items())
            ks, vs = zip(*s_dates)

            fig2, ax2 = plt.subplots(figsize=(5, 4), facecolor=bg_color)
            ax2.set_facecolor(bg_color)
            ax2.bar(ks, vs, color=colors[0])
            ax2.set_title('Monthly Activity', color=text_color)
            ax2.tick_params(colors=text_color)
            ax2.spines['bottom'].set_color(text_color)
            ax2.spines['left'].set_color(text_color)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)

            self.trends_canvas = FigureCanvasTkAgg(fig2, self.trends_frame)
            self.trends_canvas.draw()
            self.trends_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _determine_winner(self, game):
        return None
