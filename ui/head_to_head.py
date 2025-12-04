import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.interfaces import IDataManager


class HeadToHeadView(ttk.Frame):
    """
    Advanced Analytics: Head to Head Comparison.
    """

    def __init__(self, parent, data_manager: IDataManager):
        super().__init__(parent, style='TFrame')
        self.data_manager = data_manager
        self.setup_ui()

    def setup_ui(self):
        # Header
        ttk.Label(self, text="Head-to-Head Analysis",
                  style='Header.TLabel').pack(anchor='w', pady=(0, 20))

        # Controls
        control_frame = ttk.Frame(self, style='Card.TFrame', padding=20)
        control_frame.pack(fill=tk.X, pady=(0, 20))

        participants = self.data_manager.fetch_participants()

        # Team A Selection
        ttk.Label(control_frame, text="Team A:",
                  background='#2d2d2d').pack(side=tk.LEFT, padx=10)
        self.team_a = ttk.Combobox(control_frame, values=participants)
        self.team_a.pack(side=tk.LEFT, padx=10)

        ttk.Label(control_frame, text="VS", font=('Segoe UI', 12, 'bold'),
                  background='#2d2d2d', foreground='#ef5350').pack(side=tk.LEFT, padx=20)

        # Team B Selection
        ttk.Label(control_frame, text="Team B:",
                  background='#2d2d2d').pack(side=tk.LEFT, padx=10)
        self.team_b = ttk.Combobox(control_frame, values=participants)
        self.team_b.pack(side=tk.LEFT, padx=10)

        # Analyze Button
        tk.Button(control_frame, text="Compare", bg='#00acc1', fg='white', bd=0,
                  padx=20, command=self.run_analysis).pack(side=tk.LEFT, padx=30)

        # Results Area
        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(fill=tk.BOTH, expand=True)

    def run_analysis(self):
        t1 = self.team_a.get()
        t2 = self.team_b.get()

        if not t1 or not t2:
            return

        # Fetch Data
        games = self.data_manager.get_head_to_head(t1, t2)

        # Clear previous
        for w in self.results_frame.winfo_children():
            w.destroy()

        if not games:
            ttk.Label(self.results_frame,
                      text="No match history found.").pack(pady=20)
            return

        # Calculate Stats
        wins_a, wins_b, draws = 0, 0, 0
        total_score_a, total_score_b = 0, 0

        for g in games:
            try:
                s1, s2 = map(int, g['score'].split('-'))
                # Normalize score relative to Team A
                score_a = s1 if g['team1'] == t1 else s2
                score_b = s2 if g['team1'] == t1 else s1

                total_score_a += score_a
                total_score_b += score_b

                if score_a > score_b:
                    wins_a += 1
                elif score_b > score_a:
                    wins_b += 1
                else:
                    draws += 1
            except:
                pass

        # Display Stats Cards
        stats_container = ttk.Frame(self.results_frame)
        stats_container.pack(fill=tk.X, pady=20)

        self._create_stat_card(
            stats_container, f"{t1} Wins", wins_a, "#66bb6a")
        self._create_stat_card(stats_container, "Draws", draws, "#bdbdbd")
        self._create_stat_card(
            stats_container, f"{t2} Wins", wins_b, "#ef5350")

        # Graph
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        bars = ax.bar([t1, "Draw", t2], [wins_a, draws, wins_b],
                      color=['#66bb6a', '#bdbdbd', '#ef5350'])
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        canvas = FigureCanvasTkAgg(fig, self.results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _create_stat_card(self, parent, title, value, color):
        f = tk.Frame(parent, bg='#2d2d2d', padx=20, pady=15)
        f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        tk.Label(f, text=str(value), font=('Segoe UI', 24, 'bold'),
                 fg=color, bg='#2d2d2d').pack()
        tk.Label(f, text=title, font=('Segoe UI', 10),
                 fg='#b0bec5', bg='#2d2d2d').pack()
