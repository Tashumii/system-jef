import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AnalyticsDashboard(ttk.Frame):
    """
    Modern Analytics Dashboard with Interactive Charts.
    Theme: Midnight Teal
    """

    def __init__(self, parent, data_manager):
        super().__init__(parent, style='Card.TFrame')
        self.data_manager = data_manager
        self.setup_ui()

    def setup_ui(self):
        # --- Title ---
        ttk.Label(self, text="Dashboard Overview",
                  style='Header.TLabel').pack(anchor='w', pady=(0, 20))

        # --- Summary Cards ---
        self.stats_container = tk.Frame(self, bg='#2d2d2d')
        self.stats_container.pack(fill=tk.X, pady=(0, 30))
        self.card_labels = {}

        # --- Charts Area ---
        self.charts_container = tk.Frame(self, bg='#1e1e1e')
        self.charts_container.pack(fill=tk.BOTH, expand=True)

        # Initial Load
        self.refresh_analytics()

    def refresh_analytics(self):
        """Fetch latest games and update stats + charts."""
        games = self.data_manager.fetch_games()

        # Calculate stats
        total_games = len(games)
        teams = set()
        goals = 0
        for g in games:
            teams.add(g['team1'])
            teams.add(g['team2'])
            try:
                s1, s2 = map(int, g['score'].split('-'))
                goals += (s1 + s2)
            except:
                pass

        active_teams = len(teams)
        avg_goals = f"{goals / total_games:.1f}" if total_games else "0"

        # Update cards
        self._update_cards(total_games, active_teams, avg_goals)

        # Update charts
        self._draw_charts(games)

    def _update_cards(self, total, teams, goals):
        # Clear old cards
        for widget in self.stats_container.winfo_children():
            widget.destroy()

        # Create new cards
        self._create_card("Total Matches", str(total), "#00acc1")
        self._create_card("Active Teams", str(teams), "#7e57c2")
        self._create_card("Avg. Score", str(goals), "#ff7043")

    def _create_card(self, title, value, color):
        card = tk.Frame(self.stats_container, bg='#333333', padx=20, pady=15)
        card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        tk.Label(card, text=value, font=('Segoe UI', 26, 'bold'),
                 fg=color, bg='#333333').pack(anchor='w')
        tk.Label(card, text=title, font=('Segoe UI', 11),
                 fg='#cccccc', bg='#333333').pack(anchor='w')

    def _draw_charts(self, games):
        # Clear previous charts
        for widget in self.charts_container.winfo_children():
            widget.destroy()

        if not games:
            return

        # Aggregate data
        sport_counts = defaultdict(int)
        league_counts = defaultdict(int)
        for g in games:
            sport_counts[g['sport']] += 1
            league_counts[g['league']] += 1

        # --- Pie Chart (Sports) ---
        fig1, ax1 = plt.subplots(figsize=(5, 4), facecolor='#1e1e1e')
        wedges, texts, autotexts = ax1.pie(
            sport_counts.values(),
            labels=sport_counts.keys(),
            autopct='%1.1f%%',
            colors=['#00acc1', '#7e57c2', '#ff7043', '#66bb6a', '#29b6f6'],
            textprops=dict(color="white")
        )
        plt.setp(autotexts, size=9, weight="bold")
        ax1.set_title("Games by Sport", color='white', pad=20)

        canvas1 = FigureCanvasTkAgg(fig1, self.charts_container)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # --- Bar Chart (Top Leagues) ---
        fig2, ax2 = plt.subplots(figsize=(5, 4), facecolor='#1e1e1e')
        ax2.set_facecolor('#1e1e1e')

        leagues = list(league_counts.keys())[:5]
        counts = [league_counts[l] for l in leagues]

        ax2.bar(leagues, counts, color='#00acc1')
        ax2.tick_params(axis='x', colors='white', rotation=45)
        ax2.tick_params(axis='y', colors='white')
        ax2.spines['bottom'].set_color('white')
        ax2.spines['left'].set_color('white')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.set_title("Top Leagues", color='white')

        canvas2 = FigureCanvasTkAgg(fig2, self.charts_container)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
