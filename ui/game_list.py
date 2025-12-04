import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
from database.interfaces import IDataManager
from config.settings import LEAGUE_OPTIONS


class GameList(ttk.Frame):
    """
    Enhanced Game List with Filtering and PDF Export.
    """

    def __init__(self, parent, data_manager: IDataManager):
        super().__init__(parent, style='Card.TFrame', padding=20)
        self.data_manager = data_manager
        self.all_games = []
        self.filtered_games = []
        self.setup_ui()
        self.refresh_games()

    def setup_ui(self):
        # Header
        header = ttk.Frame(self, style='Card.TFrame')
        header.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header, text="Records Database",
                  style='Header.TLabel').pack(side=tk.LEFT)

        # Toolbar
        toolbar = tk.Frame(self, bg='#2d2d2d', height=50)
        toolbar.pack(fill=tk.X, pady=(0, 15))

        # Search
        tk.Label(toolbar, text="Search:", bg='#2d2d2d',
                 fg='white').pack(side=tk.LEFT, padx=10)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        tk.Entry(toolbar, textvariable=self.search_var, bg='#404040', fg='white', bd=0,
                 insertbackground='white').pack(side=tk.LEFT, padx=5, ipady=3)

        # Buttons
        btn_style = {'bg': '#00acc1', 'fg': 'white',
                     'bd': 0, 'padx': 15, 'pady': 5}

        tk.Button(toolbar, text="🔄 Refresh", command=self.refresh_games,
                  **btn_style).pack(side=tk.RIGHT, padx=5)
        tk.Button(toolbar, text="🗑 Delete", command=self.delete_game, bg='#ef5350',
                  fg='white', bd=0, padx=15, pady=5).pack(side=tk.RIGHT, padx=5)

        # Table
        columns = ("ID", "Date", "Sport", "League", "Home", "Away", "Score")
        self.tree = ttk.Treeview(
            self, columns=columns, show='headings', selectmode='browse')

        # Scrollbar
        sb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "ID" else 40)

    def refresh_games(self):
        self.all_games = self.data_manager.fetch_games()
        self.apply_filters()

    def on_search(self, *args):
        self.apply_filters()

    def apply_filters(self):
        query = self.search_var.get().lower()
        self.filtered_games = [
            g for g in self.all_games
            if query in g['team1'].lower() or query in g['team2'].lower() or query in g['league'].lower()
        ]
        self.populate_tree()

    def populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for g in self.filtered_games:
            self.tree.insert('', 'end', values=(
                g['id'], g['date'], g['sport'], g['league'],
                g['team1'], g['team2'], g['score']
            ))

    def delete_game(self):
        sel = self.tree.selection()
        if not sel:
            return

        item_id = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this record?"):
            if self.data_manager.delete_game(item_id):
                self.refresh_games()
