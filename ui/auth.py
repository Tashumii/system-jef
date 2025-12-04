"""
Authentication UI components for login and registration.
Provides secure admin authentication with dark theme styling.
"""

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

        # Center the window on screen
        self.center_window()

        # Apply dark theme
        self._setup_dark_theme()

        # Create UI
        self._create_ui()

        # Bind events
        self.bind('<Return>', lambda e: self._attempt_login())
        self.bind('<Escape>', lambda e: self.destroy())

        # Focus on username field
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
        """Setup dark theme styling for the login window."""
        style = ttk.Style()

        # Main styling
        style.configure('Auth.TFrame', background='#2d2d2d')
        style.configure('Auth.TLabel', background='#2d2d2d',
                        foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.configure('Auth.TButton', font=(
            'SF Pro Display', 10, 'bold'), padding=[12, 8],
            background='#404040', foreground='#e0e0e0', relief='flat', borderwidth=0)

        # Entry styling
        style.configure('Auth.TEntry', fieldbackground='#404040', borderwidth=1, relief='solid',
                        insertcolor='#00d4aa', foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.map('Auth.TEntry',
                  fieldbackground=[('focus', '#4a4a4a'), ('!focus', '#404040')])

        # Button styling with proper state mapping
        style.map('Auth.TButton',
                  background=[('active', '#007acc'), ('pressed',
                                                      '#005999'), ('!active', '#404040')],
                  foreground=[('active', '#ffffff'), ('pressed',
                                                      '#cccccc'), ('!active', '#e0e0e0')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'flat')])

    def _create_ui(self):
        """Create the login UI components."""
        # Main container
        main_frame = ttk.Frame(self, style='Auth.TFrame', padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(main_frame, text="🔐 Admin Login",
                                 font=('SF Pro Display', 16, 'bold'), style='Auth.TLabel')
        header_label.pack(pady=(0, 20))

        # Username field
        username_frame = ttk.Frame(main_frame, style='Auth.TFrame')
        username_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(username_frame, text="👤 Username:",
                  style='Auth.TLabel').pack(anchor='w')
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(username_frame, textvariable=self.username_var,
                                        style='Auth.TEntry')
        self.username_entry.pack(fill=tk.X, pady=(5, 0))

        # Password field
        password_frame = ttk.Frame(main_frame, style='Auth.TFrame')
        password_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(password_frame, text="🔒 Password:",
                  style='Auth.TLabel').pack(anchor='w')
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var,
                                        style='Auth.TEntry', show='•')
        self.password_entry.pack(fill=tk.X, pady=(5, 0))

        # Buttons
        button_frame = ttk.Frame(main_frame, style='Auth.TFrame')
        button_frame.pack(fill=tk.X, pady=(10, 0))

        login_btn = tk.Button(button_frame, text="🚀 Login", command=self._attempt_login,
                        bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                        activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                        relief='flat', borderwidth=0, padx=20, pady=12, height=2)
        login_btn.pack(side=tk.LEFT, expand=True, padx=(0, 5))

        register_btn = tk.Button(button_frame, text="📝 Register", command=self._show_register,
                         bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                         activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                         relief='flat', borderwidth=0, padx=20, pady=12, height=2)
        register_btn.pack(side=tk.LEFT, expand=True, padx=(5, 0))

        # Footer
        footer_label = ttk.Label(main_frame,
                                 text="Press Enter to login • Press Escape to cancel",
                                 font=('SF Pro Display', 8), foreground='#888888', style='Auth.TLabel')
        footer_label.pack(pady=(20, 0))

    def _attempt_login(self):
        """Attempt to authenticate the user."""
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror(
                "Login Error", "Please enter both username and password")
            return

        # Attempt authentication
        user_data = self.data_manager.authenticate_admin(username, password)

        if user_data:
            self.on_login_success(user_data)
            self.destroy()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid username or password")

    def _show_register(self):
        """Show the registration window."""
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

        # Center on screen
        self.center_window()

        # Apply dark theme
        self._setup_dark_theme()

        # Create UI
        self._create_ui()

        # Bind events
        self.bind('<Return>', lambda e: self._attempt_register())
        self.bind('<Escape>', lambda e: self.destroy())

        # Focus on username field
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
        """Setup dark theme styling for the registration window."""
        style = ttk.Style()

        # Main styling
        style.configure('Auth.TFrame', background='#2d2d2d')
        style.configure('Auth.TLabel', background='#2d2d2d',
                        foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.configure('Auth.TButton', font=(
            'SF Pro Display', 10, 'bold'), padding=[12, 8],
            background='#404040', foreground='#e0e0e0', relief='flat', borderwidth=0)

        # Entry styling
        style.configure('Auth.TEntry', fieldbackground='#404040', borderwidth=1, relief='solid',
                        insertcolor='#00d4aa', foreground='#e0e0e0', font=('SF Pro Display', 10))
        style.map('Auth.TEntry',
                  fieldbackground=[('focus', '#4a4a4a'), ('!focus', '#404040')])

        # Button styling with proper state mapping
        style.map('Auth.TButton',
                  background=[('active', '#007acc'), ('pressed',
                                                      '#005999'), ('!active', '#404040')],
                  foreground=[('active', '#ffffff'), ('pressed',
                                                      '#cccccc'), ('!active', '#e0e0e0')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'flat')])

    def _create_ui(self):
        """Create the registration UI components."""
        # Main container with scrollbar
        main_frame = ttk.Frame(self, style='Auth.TFrame', padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(main_frame, text="📝 Admin Registration",
                                 font=('SF Pro Display', 16, 'bold'), style='Auth.TLabel')
        header_label.pack(pady=(0, 20))

        # Username field
        self._create_field(main_frame, "👤 Username:",
                           "username", required=True)
        self.username_validation = self._create_validation_label(main_frame)

        # Email field
        self._create_field(main_frame, "📧 Email:", "email", required=True)
        self.email_validation = self._create_validation_label(main_frame)

        # Full Name field
        self._create_field(main_frame, "👨 Full Name:", "full_name")
        self.full_name_validation = self._create_validation_label(main_frame)

        # Password field
        self._create_field(main_frame, "🔒 Password:",
                           "password", show='•', required=True)
        self.password_validation = self._create_validation_label(main_frame)

        # Confirm Password field
        self._create_field(main_frame, "🔒 Confirm Password:",
                           "confirm_password", show='•', required=True)
        self.confirm_validation = self._create_validation_label(main_frame)

        # Register button - using tk.Button for better visibility
        register_btn = tk.Button(main_frame, text="📝 Create Account",
                                 command=self._attempt_register,
                                 bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                                 activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                                 relief='flat', borderwidth=0, padx=20, pady=12, height=2)
        register_btn.pack(fill=tk.X, pady=(30, 10))

        # Back to login button - using tk.Button for better visibility
        back_btn = tk.Button(main_frame, text="⬅️ Back to Login",
                             command=self.destroy,
                             bg='#404040', fg='#e0e0e0', activebackground='#007acc',
                             activeforeground='#ffffff', font=('SF Pro Display', 12, 'bold'),
                             relief='flat', borderwidth=0, padx=20, pady=12, height=2)
        back_btn.pack(fill=tk.X, pady=(0, 20))

    def _create_field(self, parent, label_text, field_name, show=None, required=False):
        """Create a labeled input field."""
        field_frame = ttk.Frame(parent, style='Auth.TFrame')
        field_frame.pack(fill=tk.X, pady=(0, 5))

        label_text_with_star = f"{label_text} *" if required else label_text
        ttk.Label(field_frame, text=label_text_with_star,
                  style='Auth.TLabel').pack(anchor='w')

        var = tk.StringVar()
        setattr(self, f"{field_name}_var", var)

        entry = ttk.Entry(field_frame, textvariable=var, style='Auth.TEntry', font=('SF Pro Display', 11))
        if show:
            entry.configure(show=show)
        entry.pack(fill=tk.X, pady=(5, 0))

        setattr(self, f"{field_name}_entry", entry)

    def _create_validation_label(self, parent):
        """Create a validation label for error messages."""
        label = ttk.Label(parent, text="", foreground='#ff6b6b',
                          font=('SF Pro Display', 8), style='Auth.TLabel')
        label.pack(anchor='w', pady=(0, 5))
        return label

    def _attempt_register(self):
        """Attempt to register a new admin user."""
        # Clear previous validation messages
        for label in [self.username_validation, self.email_validation,
                      self.full_name_validation, self.password_validation,
                      self.confirm_validation]:
            label.config(text="")

        # Get form data
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        full_name = self.full_name_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        # Validate required fields
        errors = []

        if not username:
            errors.append(("username_validation", "Username is required"))
        else:
            username_errors = validate_username(username)
            if username_errors:
                errors.append(("username_validation", username_errors[0]))

        if not email:
            errors.append(("email_validation", "Email is required"))
        else:
            email_errors = validate_email(email)
            if email_errors:
                errors.append(("email_validation", email_errors[0]))

        if not password:
            errors.append(("password_validation", "Password is required"))
        else:
            password_errors = validate_password_strength(password)
            if password_errors:
                errors.append(("password_validation", password_errors[0]))
            elif password != confirm_password:
                errors.append(("confirm_validation", "Passwords do not match"))

        # Show validation errors
        if errors:
            for field, message in errors:
                getattr(self, field).config(text=f"⚠️ {message}")
            return

        # Attempt registration
        if self.data_manager.register_admin(username, email, password, full_name):
            messagebox.showinfo("Registration Successful",
                                "Your admin account has been created successfully!\n\nYou can now log in.")
            self.destroy()
