import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any
import datetime
from tkcalendar import DateEntry

from database.interfaces import IDataManager
from models.sports import Soccer, Basketball, Billiards, Formula1, CustomSport
from config.settings import LEAGUE_OPTIONS


class GameForm(ttk.Frame):
    """
    Game Entry Form Widget.
    Theme: Casual Cyan-Green (Eco-Modern)
    """

    def __init__(self, parent, data_manager: IDataManager, game_list=None):
        super().__init__(parent, style='Card.TFrame', padding=30)

        self.data_manager = data_manager
        self.game_list = game_list

        # Initialize supported sports
        self.sports = {
            "Soccer": Soccer(),
            "Basketball": Basketball(),
            "Billiards": Billiards(),
            "Formula 1": Formula1()
        }

        self.team_cache = set()
        self.league_cache = set()
        self.load_caches()
        self.setup_form()

    def setup_form(self):
        """Set up the form widgets with modern casual design."""
        self.columnconfigure(1, weight=1)

        # --- Header ---
        header_frame = ttk.Frame(self, style='Card.TFrame')
        header_frame.grid(row=0, column=0, columnspan=3,
                          pady=(0, 30), sticky='ew')
        title = ttk.Label(
            header_frame, text="Create New Entry", style='Header.TLabel')
        title.pack(side=tk.LEFT)

        actions_frame = tk.Frame(header_frame, bg='#23332e')
        actions_frame.pack(side=tk.RIGHT)
        for text, cmd in [("📚 History", self.show_recent_teams)]:
            tk.Button(actions_frame, text=text, command=cmd,
                      bg='#2c3e39', fg='#e8f5e9', activebackground='#26a69a',
                      activeforeground='white', bd=0, padx=12, pady=6, font=('Segoe UI', 9)).pack(side=tk.RIGHT, padx=5)

        # --- Form Fields ---
        self._create_label("🏆 Sport", 1)
        sport_container = tk.Frame(self, bg='#23332e')
        sport_container.grid(row=1, column=1, sticky='ew', pady=10)

        self.sport_var = tk.StringVar()
        self.sport_combo = ttk.Combobox(sport_container, textvariable=self.sport_var,
                                        values=list(self.sports.keys()), font=('Segoe UI', 11))
        self.sport_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self.sport_combo.set("Soccer")
        self.sport_combo.bind('<<ComboboxSelected>>', self.update_labels)
        self.sport_combo.bind('<KeyRelease>', self.update_labels)

        tk.Button(sport_container, text="➕", command=self.add_new_sport,
                  bg='#26a69a', fg='white', bd=0, width=4, font=('Segoe UI', 10, 'bold')).pack(side=tk.RIGHT, padx=(10, 0))

        # League
        self._create_label("🏟️ League", 2)
        self.league_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.league_var, values=LEAGUE_OPTIONS,
                     font=('Segoe UI', 11)).grid(row=2, column=1, sticky='ew', pady=10, ipady=4)
        self.league_validation = self._create_validation_label(2)

        # Participant 1
        self.lbl_p1 = self._create_label("👥 Team 1", 3)
        self.team1_var = tk.StringVar()
        self._create_participant_row(3, self.team1_var, 1)
        self.team1_validation = self._create_validation_label(3)

        # Participant 2
        self.lbl_p2 = self._create_label("👥 Team 2", 4)
        self.team2_var = tk.StringVar()
        self._create_participant_row(4, self.team2_var, 2)
        self.team2_validation = self._create_validation_label(4)

        # Score
        self._create_label("📊 Score (e.g. 2-1)", 5)
        self.score_var = tk.StringVar()
        self.score_entry = ttk.Entry(
            self, textvariable=self.score_var, font=('Segoe UI', 11))
        self.score_entry.grid(row=5, column=1, sticky='ew', pady=10, ipady=4)
        self.score_validation = self._create_validation_label(5)

        # Date using tkcalendar
        self._create_label("📅 Date", 6)
        self.date_var = tk.StringVar()
        self.date_entry = DateEntry(
            self,
            textvariable=self.date_var,
            date_pattern='yyyy-mm-dd',  # Ensures YYYY-MM-DD format
            font=('Segoe UI', 11),
            background='#26a69a',
            foreground='white',
            borderwidth=2
        )
        self.date_entry.grid(row=6, column=1, sticky='ew', pady=10, ipady=4)
        self.date_validation = self._create_validation_label(6)

        # Submit Button
        ttk.Button(self, text="SAVE RECORD", command=self.add_game,
                   width=25).grid(row=7, column=0, columnspan=3, pady=40)

        self.setup_autocomplete()
        self.setup_validation()
        self.update_labels()

    # ------------------------- Helper Widgets -------------------------
    def _create_label(self, text, row):
        lbl = ttk.Label(self, text=text, font=(
            'Segoe UI', 11), foreground='#b0bec5')
        lbl.grid(row=row, column=0, sticky='e', padx=(0, 20), pady=10)
        return lbl

    def _create_participant_row(self, row, var, p_num):
        frame = tk.Frame(self, bg='#23332e')
        frame.grid(row=row, column=1, sticky='ew', pady=10)
        entry = ttk.Entry(frame, textvariable=var, font=('Segoe UI', 11))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        if p_num == 1:
            self.team1_entry = entry
        else:
            self.team2_entry = entry
        tk.Button(frame, text="➕", command=lambda: self.add_new_participant(p_num),
                  bg='#26a69a', fg='white', bd=0, width=4, font=('Segoe UI', 10, 'bold')).pack(side=tk.RIGHT, padx=(10, 0))

    def _create_validation_label(self, row):
        lbl = ttk.Label(self, text="", style='TLabel',
                        foreground='#ef5350', font=('Segoe UI', 9))
        lbl.grid(row=row, column=2, sticky="w", padx=(10, 0))
        return lbl

    # ------------------------- Logic Methods -------------------------
    def update_labels(self, event=None):
        current_sport_name = self.sport_var.get().strip()
        sport_obj = self.sports.get(current_sport_name)
        label_type = "Team"
        if sport_obj:
            label_type = sport_obj.participant_label
        else:
            s = current_sport_name.lower()
            if any(x in s for x in ["tennis", "boxing", "pool", "billiards"]):
                label_type = "Player"
            elif any(x in s for x in ["racing", "f1", "driver"]):
                label_type = "Driver"
        if label_type == "Player":
            self.lbl_p1.config(text="👤 Player 1")
            self.lbl_p2.config(text="👤 Player 2")
        elif label_type == "Driver":
            self.lbl_p1.config(text="🏎️ Driver 1")
            self.lbl_p2.config(text="🏎️ Driver 2")
        else:
            self.lbl_p1.config(text="👥 Home Team")
            self.lbl_p2.config(text="👥 Away Team")

    def load_caches(self):
        try:
            if hasattr(self.data_manager, 'fetch_sports'):
                db_sports = self.data_manager.fetch_sports()
                for s in db_sports:
                    if s not in self.sports:
                        self.sports[s] = CustomSport(s)
            if hasattr(self.data_manager, 'fetch_participants'):
                parts = self.data_manager.fetch_participants()
                for p in parts:
                    self.team_cache.add(p)
            games = self.data_manager.fetch_games()
            for g in games:
                self.team_cache.add(g['team1'])
                self.team_cache.add(g['team2'])
                self.league_cache.add(g['league'])
        except:
            pass

    def add_new_sport(self):
        self._show_custom_dialog("Add Sport", self.sport_var,
                                 lambda v: self.data_manager.add_sport(v) if hasattr(self.data_manager, 'add_sport') else None)
        self.after(100, lambda: self.sport_combo.config(
            values=list(self.sports.keys())))

    def add_new_participant(self, num):
        target = self.team1_var if num == 1 else self.team2_var
        sport = self.sport_var.get()

        def save(name):
            if hasattr(self.data_manager, 'add_participant'):
                self.data_manager.add_participant(name, sport)
            self.team_cache.add(name)
        self._show_custom_dialog("Add Participant", target, save)

    def _show_custom_dialog(self, title, target_var, save_callback):
        d = tk.Toplevel(self)
        d.title(title)
        d.geometry("350x180")
        d.configure(bg='#182421')
        d.transient(self)
        d.grab_set()
        d.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width()//2) - 175
        y = self.winfo_rooty() + (self.winfo_height()//2) - 90
        d.geometry(f"+{x}+{y}")
        tk.Label(d, text="Enter Name:", fg='#b0bec5', bg='#182421',
                 font=('Segoe UI', 11)).pack(pady=(20, 5))
        entry = tk.Entry(d, bg='#2c3e39', fg='white', font=('Segoe UI', 11),
                         insertbackground='white', bd=0, highlightthickness=1, highlightbackground='#26a69a')
        entry.pack(pady=5, padx=30, fill=tk.X, ipady=3)
        entry.focus()

        def on_save():
            val = entry.get().strip()
            if val:
                save_callback(val)
                if title == "Add Sport":
                    self.sports[val] = CustomSport(val)
                target_var.set(val)
                d.destroy()
        tk.Button(d, text="SAVE", command=on_save,
                  bg='#26a69a', fg='white', bd=0, padx=20, pady=5, font=('Segoe UI', 10, 'bold')).pack(pady=20)
        d.bind('<Return>', lambda e: on_save())

    def setup_autocomplete(self):
        pass  # placeholder

    def show_recent_teams(self):
        if not self.team_cache:
            return
        d = tk.Toplevel(self)
        d.title("History")
        d.geometry("300x400")
        d.configure(bg='#182421')
        lb = tk.Listbox(d, bg='#2c3e39', fg='white',
                        bd=0, font=('Segoe UI', 10))
        lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for t in sorted(self.team_cache):
            lb.insert(tk.END, t)

        def use(num):
            if lb.curselection():
                val = lb.get(lb.curselection()[0])
                (self.team1_var if num == 1 else self.team2_var).set(val)
                d.destroy()
        f = tk.Frame(d, bg='#182421')
        f.pack(fill=tk.X, pady=10)
        tk.Button(f, text="Set #1", command=lambda: use(1),
                  bg='#26a69a', fg='white', bd=0).pack(side=tk.LEFT, padx=20)
        tk.Button(f, text="Set #2", command=lambda: use(2),
                  bg='#26a69a', fg='white', bd=0).pack(side=tk.RIGHT, padx=20)

    def setup_validation(self):
        self.team1_entry.bind(
            '<FocusOut>', lambda e: self.validate_field('team1'))
        self.team2_entry.bind(
            '<FocusOut>', lambda e: self.validate_field('team2'))
        self.score_entry.bind(
            '<FocusOut>', lambda e: self.validate_field('score'))

    def validate_field(self, field):
        val = ""
        lbl = None
        if field == 'team1':
            val, lbl = self.team1_var.get(), self.team1_validation
        elif field == 'team2':
            val, lbl = self.team2_var.get(), self.team2_validation
        elif field == 'score':
            val, lbl = self.score_var.get(), self.score_validation
        if not val.strip():
            lbl.config(text="Required", foreground='#ef5350')
        else:
            lbl.config(text="✓", foreground='#66bb6a')

    # ------------------------- Main Add Game Method -------------------------
    def add_game(self):
        sport_name = self.sport_var.get().strip()
        if not sport_name:
            messagebox.showwarning("Missing", "Please enter a sport.")
            return

        if sport_name not in self.sports:
            if hasattr(self.data_manager, 'add_sport'):
                self.data_manager.add_sport(sport_name)
            self.sports[sport_name] = CustomSport(sport_name)
            self.sport_combo['values'] = list(self.sports.keys())

        p1 = self.team1_var.get().strip()
        p2 = self.team2_var.get().strip()
        if not p1 or not p2:
            messagebox.showerror("Error", "Participants cannot be empty.")
            return

        if hasattr(self.data_manager, 'add_participant'):
            self.data_manager.add_participant(p1, sport_name)
            self.data_manager.add_participant(p2, sport_name)

        score = self.score_var.get().strip()
        if "-" not in score or len(score.split("-")) != 2:
            messagebox.showerror(
                "Invalid Score", "Score must be in format X-Y")
            return

        date_value = self.date_var.get().strip()
        try:
            datetime.datetime.strptime(date_value, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date", "Please select a valid date from the calendar.")
            return

        game_obj = {
            'sport': sport_name,
            'league': self.league_var.get().strip(),
            'team1': p1,
            'team2': p2,
            'score': score,
            'date': date_value
        }

        if self.data_manager.add_game(game_obj):
            messagebox.showinfo("Success", "Result added successfully!")
            self.clear_form()
            self.load_caches()
            if self.game_list:
                self.game_list.refresh_games()  
        else:
            messagebox.showerror("Error", "Failed to save result.")

    def clear_form(self):
        self.team1_var.set("")
        self.team2_var.set("")
        self.score_var.set("")
        self.date_entry.set_date(datetime.date.today())
        for l in [self.team1_validation, self.team2_validation, self.score_validation]:
            l.config(text="")
