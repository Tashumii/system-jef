"""
Enhanced game list widget using Inheritance pattern.
GameList inherits from ttk.Frame for displaying games in a table with filtering and search.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict, Any
import datetime

from database.interfaces import IDataManager


class GameList(ttk.Frame):
    """
    Games List Display Widget.

    Shows all sports games in a sortable, filterable table view.
    Supports search, sport/league filtering, and export functionality.
    Includes context menu for game management operations.
    """

    def __init__(self, parent, data_manager: IDataManager):
        super().__init__(parent, padding=20)

        self.data_manager = data_manager
        self.all_games = []  # Store all games for filtering
        self.filtered_games = []  # Store filtered results
        self.setup_list()

    def setup_list(self):
        """Set up the enhanced game list with filtering and search."""
        # Header with title and controls
        header_frame = ttk.Frame(self, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title
        title = ttk.Label(header_frame, text="🎯 Games Management Center",
                          style='Header.TLabel')
        title.pack(side=tk.LEFT, pady=15)

        # Quick stats
        self.stats_label = ttk.Label(header_frame, text="Total: 0 games",
                                     style='Stats.TLabel')
        self.stats_label.pack(side=tk.RIGHT, pady=15, padx=(0, 20))

        # Search and filter controls
        controls_frame = ttk.Frame(self, style='Card.TFrame')
        controls_frame.pack(fill=tk.X, pady=(0, 20))

        # Search bar
        ttk.Label(controls_frame, text="🔍 Search:").grid(
            row=0, column=0, padx=(15, 5), pady=10)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(controls_frame, textvariable=self.search_var,
                                 width=30, font=('Segoe UI', 10))
        search_entry.grid(row=0, column=1, padx=(0, 20), pady=10, sticky='ew')

        # Filters
        ttk.Label(controls_frame, text="🏆 Sport:").grid(
            row=0, column=2, padx=(0, 5), pady=10)
        self.sport_filter = ttk.Combobox(controls_frame, values=["All", "Soccer", "Basketball"],
                                         state="readonly", width=12)
        self.sport_filter.set("All")
        self.sport_filter.bind('<<ComboboxSelected>>',
                               lambda e: self.apply_filters())
        self.sport_filter.grid(row=0, column=3, padx=(0, 15), pady=10)

        ttk.Label(controls_frame, text="🏟️ League:").grid(
            row=0, column=4, padx=(0, 5), pady=10)
        self.league_filter = ttk.Combobox(
            controls_frame, values=["All"], state="readonly", width=15)
        self.league_filter.set("All")
        self.league_filter.bind('<<ComboboxSelected>>',
                                lambda e: self.apply_filters())
        self.league_filter.grid(row=0, column=5, padx=(0, 15), pady=10)

        # Sort options
        ttk.Label(controls_frame, text="📊 Sort by:").grid(
            row=0, column=6, padx=(0, 5), pady=10)
        self.sort_by = ttk.Combobox(controls_frame,
                                    values=[
                                        "Date (Newest)", "Date (Oldest)", "Sport", "League"],
                                    state="readonly", width=15)
        self.sort_by.set("Date (Newest)")
        self.sort_by.bind('<<ComboboxSelected>>',
                          lambda e: self.apply_sorting())
        self.sort_by.grid(row=0, column=7, padx=(0, 15), pady=10)

        # Action buttons
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.grid(row=0, column=8, padx=(10, 15), pady=10)

        ttk.Button(buttons_frame, text="🔄 Refresh",
                   command=self.refresh_games).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="📤 Export TXT",
                   command=self.export_txt).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="🗑️ Clear Filters",
                   command=self.clear_filters).pack(side=tk.LEFT)

        # Configure grid weights
        controls_frame.grid_columnconfigure(1, weight=1)

        # Create Treeview widget with enhanced styling
        tree_frame = ttk.Frame(self, style='Card.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Sport", "League", "Team 1",
                   "Team 2", "Score", "Date", "Winner")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=20)

        # Configure columns with better styling
        column_config = {
            "ID": {"width": 60, "anchor": "center"},
            "Sport": {"width": 100, "anchor": "center"},
            "League": {"width": 150, "anchor": "w"},
            "Team 1": {"width": 140, "anchor": "w"},
            "Team 2": {"width": 140, "anchor": "w"},
            "Score": {"width": 80, "anchor": "center"},
            "Date": {"width": 100, "anchor": "center"},
            "Winner": {"width": 120, "anchor": "w"}
        }

        for col, config in column_config.items():
            self.tree.heading(
                col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, **config)

        # Style the treeview with modern theme
        style = ttk.Style()
        style.configure("Treeview",
                        background="#2d2d2d",
                        foreground="#e0e0e0",
                        fieldbackground="#2d2d2d",
                        font=('SF Pro Display', 9),
                        borderwidth=0,
                        relief='flat')
        style.configure("Treeview.Heading",
                        background="#404040",
                        foreground="#ffffff",
                        font=('SF Pro Display', 10, 'bold'),
                        borderwidth=0,
                        relief='flat')
        style.map("Treeview",
                  background=[('selected', '#00d4aa'),
                              ('!selected', '#2d2d2d')],
                  foreground=[('selected', '#ffffff'),
                              ('!selected', '#e0e0e0')])

        # Modern scrollbar styling
        style.configure('TScrollbar',
                        background='#404040',
                        troughcolor='#2d2d2d',
                        borderwidth=0,
                        arrowcolor='#cccccc',
                        width=16)
        style.map('TScrollbar',
                  background=[('active', '#4a4a4a')])

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set)

        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind events
        self.tree.bind('<Double-1>', self.on_game_double_click)
        self.tree.bind('<Return>', lambda e: self.edit_selected_game())
        self.tree.bind('<Delete>', lambda e: self.delete_selected_game())

        # Context menu
        self.context_menu = tk.Menu(
            self, tearoff=0, bg='#2d2d2d', fg='#e0e0e0')
        self.context_menu.add_command(
            label="✏️ Edit Game", command=self.edit_selected_game)
        self.context_menu.add_command(
            label="🗑️ Delete Game", command=self.delete_selected_game)
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="📋 Copy Details", command=self.copy_game_details)

        self.tree.bind('<Button-3>', self.show_context_menu)

    def show_context_menu(self, event):
        """Show context menu on right click."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def on_game_double_click(self, event):
        """Handle double-click on game."""
        self.edit_selected_game()

    def edit_selected_game(self):
        """Edit the selected game."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                "No Selection", "Please select a game to edit.")
            return

        messagebox.showinfo(
            "Feature Not Available",
            "Edit functionality is not yet implemented.\n\n"
            "To modify a game, please delete it and add a new one.")

    def delete_selected_game(self):
        """Delete the selected game."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                "No Selection", "Please select a game to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this game?\n\nThis action cannot be undone."):
            item = selection[0]
            values = self.tree.item(item, 'values')
            game_id = values[0]

            # Actually delete the game
            if self.data_manager.delete_game(game_id):
                messagebox.showinfo("Success", "Game deleted successfully!")
                self.refresh_games()
            else:
                messagebox.showerror("Error", "Failed to delete game.")

    def copy_game_details(self):
        """Copy game details to clipboard."""
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.tree.item(item, 'values')
        details = f"Game ID: {values[0]}\nSport: {values[1]}\nLeague: {values[2]}\n{values[3]} vs {values[4]}\nScore: {values[5]}\nDate: {values[6]}"

        self.clipboard_clear()
        self.clipboard_append(details)
        messagebox.showinfo("Copied", "Game details copied to clipboard!")

    def on_search_change(self, *args):
        """Handle search input changes with debouncing."""
        self.after(300, self.apply_filters)  # Debounce search

    def apply_filters(self):
        """Apply search and filter criteria."""
        search_term = self.search_var.get().lower()
        sport_filter = self.sport_filter.get()
        league_filter = self.league_filter.get()

        self.filtered_games = []

        for game in self.all_games:
            # Apply filters
            if sport_filter != "All" and game['sport'] != sport_filter:
                continue
            if league_filter != "All" and game['league'] != league_filter:
                continue

            # Apply search
            if search_term:
                searchable_text = f"{game['sport']} {game['league']} {game['team1']} {game['team2']} {game['score']}".lower(
                )
                if search_term not in searchable_text:
                    continue

            self.filtered_games.append(game)

        self.apply_sorting()

    def apply_sorting(self):
        """Apply sorting to filtered games."""
        sort_option = self.sort_by.get()

        if sort_option == "Date (Newest)":
            self.filtered_games.sort(key=lambda x: x['date'], reverse=True)
        elif sort_option == "Date (Oldest)":
            self.filtered_games.sort(key=lambda x: x['date'])
        elif sort_option == "Sport":
            self.filtered_games.sort(key=lambda x: x['sport'])
        elif sort_option == "League":
            self.filtered_games.sort(key=lambda x: x['league'])

        self.display_games()

    def sort_by_column(self, col):
        """Sort by clicked column."""
        if col == "Date":
            current_sort = self.sort_by.get()
            if current_sort == "Date (Newest)":
                self.sort_by.set("Date (Oldest)")
            else:
                self.sort_by.set("Date (Newest)")
        elif col == "Sport":
            self.sort_by.set("Sport")
        elif col == "League":
            self.sort_by.set("League")
        else:
            return  # Don't sort by other columns

        self.apply_sorting()

    def display_games(self):
        """Display filtered games in treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add filtered games to treeview
        for game in self.filtered_games:
            winner = self.determine_winner(game)
            self.tree.insert("", tk.END, values=(
                game['id'],
                game['sport'],
                game['league'],
                game['team1'],
                game['team2'],
                game['score'],
                game['date'],
                winner
            ))

        # Update stats
        self.stats_label.config(
            text=f"Showing: {len(self.filtered_games)} games")

    def clear_filters(self):
        """Clear all filters and search."""
        self.search_var.set("")
        self.sport_filter.set("All")
        self.league_filter.set("All")
        self.sort_by.set("Date (Newest)")
        self.filtered_games = self.all_games.copy()
        self.display_games()

    def refresh_games(self):
        """Refresh the games list from database."""
        try:
            # Abstraction: Use the data manager interface to fetch games
            self.all_games = self.data_manager.fetch_games()
            self.filtered_games = self.all_games.copy()

            # Update league filter options
            leagues = sorted(set(game['league'] for game in self.all_games))
            self.league_filter['values'] = ["All"] + leagues
            if self.league_filter.get() not in self.league_filter['values']:
                self.league_filter.set("All")

            self.apply_filters()

        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Failed to refresh games: {e}")

    def export_txt(self):
        """Export filtered games to TXT file."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Games to TXT"
            )

            if filename:
                with open(filename, 'w', encoding='utf-8') as txtfile:
                    # Write header
                    txtfile.write(
                        "SPORTS MANAGEMENT DASHBOARD - GAMES EXPORT\n")
                    txtfile.write("=" * 50 + "\n\n")

                    # Write summary
                    txtfile.write(
                        f"Total Games Exported: {len(self.filtered_games)}\n")
                    txtfile.write(
                        f"Export Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                    # Write games
                    for i, game in enumerate(self.filtered_games, 1):
                        winner = self.determine_winner(game)
                        txtfile.write(f"Game #{i}\n")
                        txtfile.write("-" * 20 + "\n")
                        txtfile.write(f"Sport: {game['sport']}\n")
                        txtfile.write(f"League: {game['league']}\n")
                        txtfile.write(
                            f"Teams: {game['team1']} vs {game['team2']}\n")
                        txtfile.write(f"Score: {game['score']}\n")
                        txtfile.write(f"Date: {game['date']}\n")
                        txtfile.write(f"Winner: {winner}\n")
                        txtfile.write("\n")

                messagebox.showinfo(
                    "Export Complete", f"Exported {len(self.filtered_games)} games to {filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export TXT: {e}")

    def determine_winner(self, game) -> str:
        """Determine winner from game score."""
        try:
            score_parts = game['score'].split('-')
            if len(score_parts) == 2:
                score1 = int(score_parts[0])
                score2 = int(score_parts[1])
                if score1 > score2:
                    return game['team1']
                elif score2 > score1:
                    return game['team2']
                else:
                    return "Draw"
        except (ValueError, IndexError):
            pass
        return "Unknown"
