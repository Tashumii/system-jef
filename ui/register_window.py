import tkinter as tk
from tkinter import ttk, messagebox
from database.interfaces import IDataManager
from utils.auth import hash_password, validate_username, validate_email, validate_password_strength


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent, data_manager: IDataManager, on_register_success):
        super().__init__(parent)
        self.parent = parent
        self.data_manager = data_manager
        self.on_register_success = on_register_success

        self.title("Register New Admin")
        self.geometry("400x350")
        self.configure(bg="#182421")
        self.resizable(False, False)
        self.grab_set()  # modal window
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Username:", fg="white", bg="#182421",
                 font=("Segoe UI", 10)).pack(pady=(20, 5))
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var, width=35).pack(pady=5)

        tk.Label(self, text="Email:", fg="white", bg="#182421",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        self.email_var = tk.StringVar()
        tk.Entry(self, textvariable=self.email_var, width=35).pack(pady=5)

        tk.Label(self, text="Password:", fg="white", bg="#182421",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        self.password_var = tk.StringVar()
        tk.Entry(self, textvariable=self.password_var,
                 show="*", width=35).pack(pady=5)

        tk.Label(self, text="Confirm Password:", fg="white",
                 bg="#182421", font=("Segoe UI", 10)).pack(pady=(10, 5))
        self.confirm_var = tk.StringVar()
        tk.Entry(self, textvariable=self.confirm_var,
                 show="*", width=35).pack(pady=5)

        ttk.Button(self, text="Register",
                   command=self.register_user).pack(pady=(20, 5))

    def register_user(self):
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        confirm = self.confirm_var.get().strip()

        warnings = []

        # Validate username
        user_errors = validate_username(username)
        if user_errors:
            warnings.extend(user_errors)

        # Validate email
        email_errors = validate_email(email)
        if email_errors:
            warnings.extend(email_errors)

        # Skip password strength validation (accept any password)

        # Password confirmation
        if password != confirm:
            warnings.append("Passwords do not match.")

        # Show warnings if any
        if warnings:
            messagebox.showwarning("Registration Error", "\n".join(warnings))
            return

        # Use data_manager's register_admin method
        success = self.data_manager.register_admin(username, email, password)
        if not success:
            return

        # Callback on success
        user_data = {"username": username,
                     "email": email, "password": password}
        self.on_register_success(user_data)
        self.destroy()
