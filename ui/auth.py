import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any
from database.interfaces import IDataManager
from utils.auth import validate_password_strength, validate_username, validate_email


class LoginWindow(tk.Toplevel):
    """Login window for admin authentication."""

    def __init__(self, parent, data_manager: IDataManager, on_login_success: Callable[[Dict[str, Any]], None]):
        super().__init__(parent)
        self.data_manager = data_manager
        self.on_login_success = on_login_success

        self.title("Admin Login - Sports Management Dashboard")
        self.geometry("500x450")
        self.resizable(False, False)
        self.configure(bg='#1a1a1a')

        self.center_window()
        self._setup_dark_theme()
        self._create_ui()

        self.bind('<Return>', lambda e: self._attempt_login())
        self.bind('<Escape>', lambda e: self.destroy())
        self.username_entry.focus()

    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _setup_dark_theme(self):
        style = ttk.Style()
        style.configure('Auth.TFrame', background='#2d2d2d')
        style.configure('Auth.TLabel', background='#2d2d2d',
                        foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.configure('Auth.TEntry', fieldbackground='#404040', borderwidth=1, relief='solid',
                        insertcolor='#00d4aa', foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.map('Auth.TEntry', fieldbackground=[
                  ('focus', '#4a4a4a'), ('!focus', '#404040')])

    def _create_ui(self):
        main_frame = ttk.Frame(self, style='Auth.TFrame', padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="🔐 Admin Login", font=('SF Pro Display', 16, 'bold'), style='Auth.TLabel')\
            .pack(pady=(0, 20))

        # Username
        ttk.Label(main_frame, text="👤 Username:",
                  style='Auth.TLabel').pack(anchor='w')
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            main_frame, textvariable=self.username_var, style='Auth.TEntry')
        self.username_entry.pack(fill=tk.X, pady=(5, 10))

        # Password
        ttk.Label(main_frame, text="🔒 Password:",
                  style='Auth.TLabel').pack(anchor='w')
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            main_frame, textvariable=self.password_var, style='Auth.TEntry', show='•')
        self.password_entry.pack(fill=tk.X, pady=(5, 20))

        # Buttons
        login_btn = tk.Button(main_frame, text="🚀 Login", command=self._attempt_login,
                              bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                              activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                              relief='flat', borderwidth=0, padx=20, pady=12)
        login_btn.pack(fill=tk.X, pady=(0, 10))

        register_btn = tk.Button(main_frame, text="📝 Register", command=self._show_register,
                                 bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                                 activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                                 relief='flat', borderwidth=0, padx=20, pady=12)
        register_btn.pack(fill=tk.X)

    def _attempt_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror(
                "Login Error", "Please enter both username and password")
            return

        user_data = self.data_manager.authenticate_admin(username, password)
        if user_data:
            self.on_login_success(user_data)
            self.destroy()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid username or password")

    def _show_register(self):
        RegisterWindow(self, self.data_manager)


class RegisterWindow(tk.Toplevel):
    """Registration window for new admin accounts."""

    def __init__(self, parent, data_manager: IDataManager):
        super().__init__(parent)
        self.data_manager = data_manager

        self.title("Admin Registration - Sports Management Dashboard")
        self.geometry("550x650")
        self.resizable(False, False)
        self.configure(bg='#1a1a1a')

        self.center_window()
        self._setup_dark_theme()
        self._create_ui()

        self.bind('<Return>', lambda e: self._attempt_register())
        self.bind('<Escape>', lambda e: self.destroy())
        self.username_entry.focus()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _setup_dark_theme(self):
        style = ttk.Style()
        style.configure('Auth.TFrame', background='#2d2d2d')
        style.configure('Auth.TLabel', background='#2d2d2d',
                        foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.configure('Auth.TEntry', fieldbackground='#404040', borderwidth=1, relief='solid',
                        insertcolor='#00d4aa', foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.map('Auth.TEntry', fieldbackground=[
                  ('focus', '#4a4a4a'), ('!focus', '#404040')])

    def _create_ui(self):
        main_frame = ttk.Frame(self, style='Auth.TFrame', padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="📝 Admin Registration", font=('SF Pro Display', 16, 'bold'), style='Auth.TLabel')\
            .pack(pady=(0, 20))

        self._create_field(main_frame, "👤 Username:",
                           "username", required=True)
        self._create_field(main_frame, "📧 Email:", "email", required=True)
        self._create_field(main_frame, "👨 Full Name:", "full_name")
        self._create_field(main_frame, "🔒 Password:",
                           "password", show='•', required=True)
        self._create_field(main_frame, "🔒 Confirm Password:",
                           "confirm_password", show='•', required=True)

        self.validation_labels = {}
        for name in ['username', 'email', 'full_name', 'password', 'confirm_password']:
            lbl = ttk.Label(main_frame, text="",
                            foreground='#ff6b6b', font=('SF Pro Display', 8))
            lbl.pack(anchor='w', pady=(0, 5))
            self.validation_labels[name] = lbl

        register_btn = tk.Button(main_frame, text="📝 Create Account", command=self._attempt_register,
                                 bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                                 activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                                 relief='flat', borderwidth=0, padx=20, pady=12, height=2)
        register_btn.pack(fill=tk.X, pady=(30, 10))

        back_btn = tk.Button(main_frame, text="⬅️ Back to Login", command=self.destroy,
                             bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                             activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                             relief='flat', borderwidth=0, padx=20, pady=12, height=2)
        back_btn.pack(fill=tk.X, pady=(0, 20))

    def _create_field(self, parent, label_text, field_name, show=None, required=False):
        ttk.Label(parent, text=f"{label_text}{' *' if required else ''}",
                  style='Auth.TLabel').pack(anchor='w')
        var = tk.StringVar()
        setattr(self, f"{field_name}_var", var)
        entry = ttk.Entry(parent, textvariable=var,
                          style='Auth.TEntry', font=('SF Pro Display', 11))
        if show:
            entry.configure(show=show)
        entry.pack(fill=tk.X, pady=(5, 0))
        setattr(self, f"{field_name}_entry", entry)

    def _attempt_register(self):
        # Clear previous validation
        for lbl in self.validation_labels.values():
            lbl.config(text="")

        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        full_name = self.full_name_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        errors = []

        if not username:
            errors.append(('username', "Username is required"))
        else:
            e = validate_username(username)
            if e:
                errors.append(('username', e[0]))

        if not email:
            errors.append(('email', "Email is required"))
        else:
            e = validate_email(email)
            if e:
                errors.append(('email', e[0]))

        if password:
            e = validate_password_strength(password)
            if e:
                errors.append(('password', e[0]))
            elif password != confirm_password:
                errors.append(('confirm_password', "Passwords do not match"))
        else:
            errors.append(('password', "Password is required"))

        # Show validation
        if errors:
            for field, msg in errors:
                self.validation_labels[field].config(text=f"⚠️ {msg}")
            return

        if self.data_manager.register_admin(username, email, password, full_name):
            messagebox.showinfo("Registration Successful",
                                "Your admin account has been created!\nYou can now log in.")
            self.destroy()
