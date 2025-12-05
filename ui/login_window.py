import tkinter as tk
from tkinter import ttk, messagebox
from database.interfaces import IDataManager


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, data_manager: IDataManager, success_callback):
        super().__init__(parent)
        self.parent = parent
        self.data_manager = data_manager
        self.success_callback = success_callback

        self.title("Admin Login")
        self.geometry("350x250")
        self.configure(bg="#182421")
        self.resizable(False, False)
        self.grab_set()  # modal
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Username:", fg="white", bg="#182421",
                 font=("Segoe UI", 10)).pack(pady=(20, 5))
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var, width=30).pack(pady=5)

        tk.Label(self, text="Password:", fg="white", bg="#182421",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        self.password_var = tk.StringVar()
        tk.Entry(self, textvariable=self.password_var,
                 show="*", width=30).pack(pady=5)

        # Login button
        ttk.Button(self, text="Login", command=self.login).pack(pady=(15, 5))

        # Register button
        tk.Button(
            self,
            text="Register New Admin",
            command=self.open_register,
            bg="#00acc1",
            fg="white",
            bd=0,
            padx=10,
            pady=5,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            activebackground="#007c91"
        ).pack(pady=(10, 10))

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Missing", "Please enter both fields.")
            return

        user = self.data_manager.authenticate_admin(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome, {user['username']}!")
            self.success_callback(user)
            self.destroy()
        else:
            messagebox.showerror("Failed", "Invalid username or password.")

    def open_register(self):
        from ui.register_window import RegisterWindow

        # Callback after successful registration
        def on_register_success(user):
            messagebox.showinfo(
                "Registered",
                f"User '{user['username']}' registered successfully!\nYou can now login."
            )
            self.username_var.set(user['username'])
            self.password_var.set("")  # Leave password empty for security

        # Open registration modal
        RegisterWindow(self, self.data_manager, on_register_success)
