import tkinter as tk
from tkinter import ttk, messagebox

from database.interfaces import IDataManager
from config.settings import APP_CONFIG
from ui.game_list import GameList  # make sure this is the cleaned version


class MainApplication(tk.Tk):
    """
    Midnight Teal Themed Sidebar Application
    Fully fixed version with .run() method
    """

    def __init__(self, data_manager: IDataManager):
        super().__init__()

        self.data_manager = data_manager
        self.current_view = None
        self.current_user = {"username": "Admin"}  # temporary

        self.withdraw()  # Hide flashing
        self._setup_window()
        self._setup_styles()
        self._build_layout()
        self._build_sidebar()

        self.show_view("dashboard")

        self.deiconify()  # Show app without flicker

    # -------------------------
    # WINDOW + THEME SETUP
    # -------------------------
    def _setup_window(self):
        self.title(APP_CONFIG.get("title", "Sports Management Dashboard"))
        self.geometry(APP_CONFIG.get("geometry", "1280x800"))
        self.configure(bg="#1e1e1e")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        bg = "#1e1e1e"
        fg = "#ffffff"
        accent = "#00acc1"

        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("Header.TLabel",
                        font=("Segoe UI", 24, "bold"),
                        foreground=accent)

        # Treeview table styling
        style.configure("Treeview",
                        background="#2d2d2d",
                        fieldbackground="#2d2d2d",
                        foreground="white",
                        rowheight=30)
        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground=accent,
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", accent)])

    # -------------------------
    # LAYOUT
    # -------------------------
    def _build_layout(self):
        # Sidebar (left)
        self.sidebar = tk.Frame(self, bg="#252526", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Main content (right)
        self.content_area = tk.Frame(self, bg="#1e1e1e")
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def _build_sidebar(self):
        tk.Label(
            self.sidebar,
            text="🏅 SPORTIFY",
            bg="#252526",
            fg="#00acc1",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=40)

        self._add_nav_button("📊  Dashboard", "dashboard")
        self._add_nav_button("📝  New Entry", "entry")
        self._add_nav_button("📁  Records", "records")
        self._add_nav_button("⚔️  Head-to-Head", "h2h")

        tk.Button(
            self.sidebar,
            text="⚙ Settings",
            bg="#252526",
            fg="#aaaaaa",
            bd=0,
            cursor="hand2",
            activebackground="#252526"
        ).pack(side=tk.BOTTOM, pady=20)

    def _add_nav_button(self, text: str, target: str):
        btn = tk.Button(
            self.sidebar,
            text=text,
            bg="#252526",
            fg="white",
            bd=0,
            font=("Segoe UI", 11),
            anchor="w",
            padx=30,
            pady=12,
            activebackground="#333333",
            activeforeground="#00acc1",
            cursor="hand2",
            command=lambda: self.show_view(target)
        )
        btn.pack(fill=tk.X)

    # -------------------------
    # VIEW SWITCHING SYSTEM
    # -------------------------
    def show_view(self, view_name: str):
        """Safely load any view while preventing crashes."""
        # Clear existing view
        for widget in self.content_area.winfo_children():
            widget.destroy()

        try:
            if view_name == "dashboard":
                from ui.analytics_dashboard import AnalyticsDashboard
                view = AnalyticsDashboard(self.content_area, self.data_manager)

            elif view_name == "records":
                from ui.game_list import GameList
                view = GameList(self.content_area, self.data_manager)
                view.refresh_games()  # ensure latest games are fetched

            elif view_name == "entry":
                from ui.game_form import GameForm
                # Pass GameList instance to GameForm for auto-refresh
                from ui.game_list import GameList
                records_view = GameList(self.content_area, self.data_manager)
                records_view.refresh_games()
                view = GameForm(
                    self.content_area,
                    self.data_manager,
                    game_list=records_view  # ✅ pass the instance
                )

            elif view_name == "h2h":
                from ui.head_to_head import HeadToHeadView
                view = HeadToHeadView(self.content_area, self.data_manager)

            else:
                raise Exception(f"Unknown view: {view_name}")

            view.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
            self.current_view = view  # track current view

        except Exception as e:
            messagebox.showerror(
                "View Load Error", f"Failed to load view '{view_name}':\n\n{str(e)}")
    # -------------------------
    # ADD RUN() METHOD
    # -------------------------

    def run(self):
        """Start Tkinter main loop safely."""
        try:
            self.mainloop()
        except Exception as e:
            messagebox.showerror("Application Error", str(e))
