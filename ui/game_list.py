import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from database.interfaces import IDataManager
from config.settings import LEAGUE_OPTIONS

class GameList(ttk.Frame):
    """
    Games List Widget.
    Theme: Casual Cyan-Green (Eco-Modern)
    """

    def __init__(self, parent, data_manager: IDataManager):
        super().__init__(parent, style='Card.TFrame', padding=20)
        self.data_manager = data_manager
        self.all_games = []
        self.filtered_games = []
        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        header = ttk.Frame(self, style='Card.TFrame')
        header.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(header, text="Current Records", style='Header.TLabel').pack(side=tk.LEFT)
        self.stats_lbl = ttk.Label(header, text="0 Items", style='Stats.TLabel')
        self.stats_lbl.pack(side=tk.RIGHT)

        # --- Filter Bar (Custom Green Styling) ---
        bar = tk.Frame(self, bg='#23332e', height=50)
        bar.pack(fill=tk.X, pady=(0, 15))

        # Styles for filter widgets
        lbl_style = {'bg': '#23332e', 'fg': '#b0bec5', 'font': ('Segoe UI', 10)}

        # Search
        tk.Label(bar, text="Search:", **lbl_style).pack(side=tk.LEFT, padx=10)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)

        # Manual styling for Entry to match casual theme
        search_entry = tk.Entry(bar, textvariable=self.search_var,
                              bg='#2c3e39', fg='white', insertbackground='white',
                              bd=0, highlightthickness=1, highlightbackground='#26a69a',
                              font=('Segoe UI', 10))
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4, ipadx=5) # Spacious input

        # Filter Combos
        self.sport_filter = ttk.Combobox(bar, values=["All Sports"], state="readonly", width=12)
        self.sport_filter.set("All Sports")
        self.sport_filter.pack(side=tk.LEFT, padx=10, pady=10)
        self.sport_filter.bind('<<ComboboxSelected>>', self.apply_filters)

        self.league_filter = ttk.Combobox(bar, values=["All Leagues"] + LEAGUE_OPTIONS, state="readonly", width=15)
        self.league_filter.set("All Leagues")
        self.league_filter.pack(side=tk.LEFT, padx=5, pady=10)
        self.league_filter.bind('<<ComboboxSelected>>', self.apply_filters)

        # Action Buttons (Using ttk style from main)
        ttk.Button(bar, text="Reset", command=self.reset_filters).pack(side=tk.LEFT, padx=10)
        ttk.Button(bar, text="Export CSV", command=self.export_csv).pack(side=tk.RIGHT, padx=10)
        ttk.Button(bar, text="Standings", command=self.show_standings).pack(side=tk.RIGHT, padx=0)

        # --- Treeview (The Table) ---
        tree_frame = ttk.Frame(self, style='Card.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("ID", "Date", "Sport", "League", "Match", "Score", "Winner")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")

        # Scrollbar
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # Table Styling (The "Cyan Green" effect)
        style = ttk.Style()
        style.configure("Treeview",
                        background="#23332e",
                        fieldbackground="#23332e",
                        foreground="#e8f5e9",
                        rowheight=30, # Casual spacing
                        font=('Segoe UI', 10),
                        borderwidth=0)

        style.configure("Treeview.Heading",
                        background="#182421",
                        foreground="#26a69a", # Cyan Green text
                        font=('Segoe UI', 10, 'bold'),
                        borderwidth=0)

        style.map("Treeview",
                  background=[('selected', '#26a69a')],
                  foreground=[('selected', 'white')])

        # Config Columns
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Sport", width=100, anchor="center")
        self.tree.column("League", width=150)
        self.tree.column("Match", width=250)
        self.tree.column("Score", width=80, anchor="center")
        self.tree.column("Winner", width=150)

        for c in cols: self.tree.heading(c, text=c, command=lambda _c=c: self.sort_col(_c))

        # Context Menu
        self.menu = tk.Menu(self, tearoff=0, bg='#23332e', fg='white', activebackground='#26a69a')
        self.menu.add_command(label="❌ Delete Record", command=self.delete_game)
        self.tree.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root))

        self.refresh_games()

    def refresh_games(self):
        try:
            self.all_games = self.data_manager.fetch_games()

            # Update sports filter dynamically
            sports = ["All Sports"]
            if hasattr(self.data_manager, 'fetch_sports'):
                sports += self.data_manager.fetch_sports()
            self.sport_filter['values'] = sports

            self.apply_filters()
        except: pass

    def apply_filters(self, event=None):
        s_filter = self.sport_filter.get()
        l_filter = self.league_filter.get()
        search = self.search_var.get().lower()

        self.filtered_games = []
        for g in self.all_games:
            if s_filter != "All Sports" and g['sport'] != s_filter: continue
            if l_filter != "All Leagues" and g['league'] != l_filter: continue

            full_str = f"{g['sport']} {g['league']} {g['team1']} {g['team2']}".lower()
            if search and search not in full_str: continue

            self.filtered_games.append(g)

        self.populate_tree()

    def populate_tree(self):
        for i in self.tree.get_children(): self.tree.delete(i)

        for g in self.filtered_games:
            match = f"{g['team1']} vs {g['team2']}"
            winner = self.get_winner(g)
            self.tree.insert("", "end", values=(g['id'], g['date'], g['sport'], g['league'], match, g['score'], winner))

        self.stats_lbl.config(text=f"{len(self.filtered_games)} Records")

    def get_winner(self, g):
        try:
            s1, s2 = map(int, g['score'].split('-'))
            if s1 > s2: return g['team1']
            elif s2 > s1: return g['team2']
            return "Draw"
        except: return "-"

    def on_search(self, *args):
        self.after(300, self.apply_filters)

    def reset_filters(self):
        self.search_var.set("")
        self.sport_filter.set("All Sports")
        self.league_filter.set("All Leagues")
        self.apply_filters()

    def delete_game(self):
        sel = self.tree.selection()
        if not sel: return

        item_id = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Delete", "Delete this record permanently?"):
            if self.data_manager.delete_game(item_id):
                self.refresh_games()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Sport", "League", "Team1", "Team2", "Score"])
                for g in self.filtered_games:
                    writer.writerow([g['id'], g['date'], g['sport'], g['league'], g['team1'], g['team2'], g['score']])
            messagebox.showinfo("Success", "Exported successfully.")

    def show_standings(self):
        league = self.league_filter.get()
        if league == "All Leagues":
            messagebox.showinfo("Info", "Please select a specific League first.")
            return

        # Simple standings logic
        scores = {}
        for g in self.filtered_games:
            t1, t2 = g['team1'], g['team2']
            if t1 not in scores: scores[t1] = 0
            if t2 not in scores: scores[t2] = 0

            try:
                s1, s2 = map(int, g['score'].split('-'))
                if s1 > s2: scores[t1] += 3
                elif s2 > s1: scores[t2] += 3
                else:
                    scores[t1] += 1
                    scores[t2] += 1
            except: pass

        # Popup
        top = tk.Toplevel(self)
        top.title(f"Standings: {league}")
        top.geometry("400x400")
        top.configure(bg='#182421')

        tk.Label(top, text=f"{league} Ranking", font=('Segoe UI', 14, 'bold'),
                bg='#182421', fg='#26a69a').pack(pady=15)

        frame = tk.Frame(top, bg='#23332e', padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        sorted_teams = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        for idx, (team, pts) in enumerate(sorted_teams, 1):
            row = tk.Frame(frame, bg='#23332e')
            row.pack(fill=tk.X, pady=5)
            tk.Label(row, text=f"{idx}.", font=('Segoe UI', 11, 'bold'), fg='#26a69a', bg='#23332e', width=3).pack(side=tk.LEFT)
            tk.Label(row, text=team, font=('Segoe UI', 11), fg='white', bg='#23332e').pack(side=tk.LEFT)
            tk.Label(row, text=f"{pts} pts", font=('Segoe UI', 11, 'bold'), fg='#66bb6a', bg='#23332e').pack(side=tk.RIGHT)

    def sort_col(self, col):
        pass # sorting placeholder
