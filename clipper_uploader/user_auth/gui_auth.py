# gui_auth.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QStackedLayout, QHBoxLayout
)
# Import new backend functions
from user_auth_backend import accounts, hash_password, update_username_backend, update_password_backend, delete_account_backend

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipper Authentication")
        self.setGeometry(300, 300, 300, 250) # Adjusted height to accommodate more buttons
        self.login_successful = False

        self.stack = QStackedLayout()

        self.login_widget = self.create_login_view()
        self.register_widget = self.create_register_view()
        self.manage_account_widget = self.create_manage_account_view() # New: Manage Account View

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.register_widget)
        self.stack.addWidget(self.manage_account_widget) # Add to stack

        container = QVBoxLayout()
        container.addLayout(self.stack)
        self.setLayout(container)

    def create_login_view(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Username")

        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Password")
        self.login_pass.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")
        manage_btn = QPushButton("Manage Account") # New: Manage Account Button

        login_btn.clicked.connect(self.handle_login)
        register_btn.clicked.connect(self.switch_to_register)
        manage_btn.clicked.connect(self.switch_to_manage_account) # New: Connect to manage account view

        layout.addWidget(QLabel("🔐 Login to Clipper"))
        layout.addWidget(self.login_user)
        layout.addWidget(self.login_pass)
        layout.addWidget(login_btn)

        # Use a horizontal layout for register and manage buttons
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.addWidget(register_btn)
        bottom_buttons_layout.addWidget(manage_btn)
        layout.addLayout(bottom_buttons_layout)

        widget.setLayout(layout)
        return widget

    def create_register_view(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("New Username")

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("New Password")
        self.reg_pass.setEchoMode(QLineEdit.Password)

        register_btn = QPushButton("Register")
        back_btn = QPushButton("Back to Login")

        register_btn.clicked.connect(self.handle_register)
        back_btn.clicked.connect(self.switch_to_login)

        layout.addWidget(QLabel("🆕 Register New Account"))
        layout.addWidget(self.reg_user)
        layout.addWidget(self.reg_pass)
        layout.addWidget(register_btn)
        layout.addWidget(back_btn)

        widget.setLayout(layout)
        return widget

    # New: Create Manage Account View
    def create_manage_account_view(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Update Username Section
        layout.addWidget(QLabel("✏️ Update Username"))
        self.update_user_current = QLineEdit()
        self.update_user_current.setPlaceholderText("Current Username")
        self.update_user_pass = QLineEdit()
        self.update_user_pass.setPlaceholderText("Password")
        self.update_user_pass.setEchoMode(QLineEdit.Password)
        self.update_user_new = QLineEdit()
        self.update_user_new.setPlaceholderText("New Username")
        update_username_btn = QPushButton("Update Username")
        update_username_btn.clicked.connect(self.handle_update_username)
        layout.addWidget(self.update_user_current)
        layout.addWidget(self.update_user_pass)
        layout.addWidget(self.update_user_new)
        layout.addWidget(update_username_btn)

        # Update Password Section
        layout.addWidget(QLabel("🔐 Update Password"))
        self.update_pass_user = QLineEdit()
        self.update_pass_user.setPlaceholderText("Username")
        self.update_pass_old = QLineEdit()
        self.update_pass_old.setPlaceholderText("Current Password")
        self.update_pass_old.setEchoMode(QLineEdit.Password)
        self.update_pass_new = QLineEdit()
        self.update_pass_new.setPlaceholderText("New Password")
        self.update_pass_new.setEchoMode(QLineEdit.Password)
        update_password_btn = QPushButton("Update Password")
        update_password_btn.clicked.connect(self.handle_update_password)
        layout.addWidget(self.update_pass_user)
        layout.addWidget(self.update_pass_old)
        layout.addWidget(self.update_pass_new)
        layout.addWidget(update_password_btn)

        # Delete Account Section
        layout.addWidget(QLabel("🗑️ Delete Account"))
        self.delete_user = QLineEdit()
        self.delete_user.setPlaceholderText("Username")
        self.delete_pass = QLineEdit()
        self.delete_pass.setPlaceholderText("Password")
        self.delete_pass.setEchoMode(QLineEdit.Password)
        delete_account_btn = QPushButton("Delete Account")
        delete_account_btn.clicked.connect(self.handle_delete_account)
        layout.addWidget(self.delete_user)
        layout.addWidget(self.delete_pass)
        layout.addWidget(delete_account_btn)

        back_to_login_btn = QPushButton("Back to Login")
        back_to_login_btn.clicked.connect(self.switch_to_login)
        layout.addWidget(back_to_login_btn)

        widget.setLayout(layout)
        return widget

    def switch_to_register(self):
        self.stack.setCurrentWidget(self.register_widget)

    def switch_to_login(self):
        self.stack.setCurrentWidget(self.login_widget)
        # Clear fields when switching back to login
        self.login_user.clear()
        self.login_pass.clear()
        self.reg_user.clear()
        self.reg_pass.clear()
        self.update_user_current.clear()
        self.update_user_pass.clear()
        self.update_user_new.clear()
        self.update_pass_user.clear()
        self.update_pass_old.clear()
        self.update_pass_new.clear()
        self.delete_user.clear()
        self.delete_pass.clear()


    # New: Switch to Manage Account
    def switch_to_manage_account(self):
        self.stack.setCurrentWidget(self.manage_account_widget)
        # Optionally pre-fill username if logged in, or ensure fields are clear
        self.update_user_current.clear()
        self.update_user_pass.clear()
        self.update_user_new.clear()
        self.update_pass_user.clear()
        self.update_pass_old.clear()
        self.update_pass_new.clear()
        self.delete_user.clear()
        self.delete_pass.clear()

    def handle_login(self):
        user = self.login_user.text().strip()
        pw = self.login_pass.text().strip()

        if not user or not pw:
            QMessageBox.warning(self, "Validation Error", "Username and password cannot be empty.")
            return

        found = accounts.find_one({"username": user})
        if found and found["password"] == hash_password(pw):
            QMessageBox.information(self, "✅ Login Successful", "Welcome!")
            self.login_successful = True
            self.close()
        else:
            QMessageBox.warning(self, "❌ Login Failed", "Invalid username or password.")

    def handle_register(self):
        user = self.reg_user.text().strip()
        pw = self.reg_pass.text().strip()

        if not user or not pw:
            QMessageBox.warning(self, "Validation Error", "Username and password cannot be empty.")
            return

        if accounts.find_one({"username": user}):
            QMessageBox.warning(self, "❌ Error", "Username already exists.")
            return

        accounts.insert_one({"username": user, "password": hash_password(pw)})
        QMessageBox.information(self, "✅ Registered", "Account created. Please log in.")
        self.switch_to_login()

    # New: Handlers for Update/Delete
    def handle_update_username(self):
        current_username = self.update_user_current.text().strip()
        password = self.update_user_pass.text().strip()
        new_username = self.update_user_new.text().strip()

        if not current_username or not password or not new_username:
            QMessageBox.warning(self, "Validation Error", "All fields are required for username update.")
            return
        
        if current_username == new_username:
            QMessageBox.warning(self, "Validation Error", "New username cannot be the same as current username.")
            return

        success, message = update_username_backend(current_username, password, new_username)
        if success:
            QMessageBox.information(self, "✅ Success", message)
            self.update_user_current.clear()
            self.update_user_pass.clear()
            self.update_user_new.clear()
        else:
            QMessageBox.warning(self, "❌ Error", message)

    def handle_update_password(self):
        username = self.update_pass_user.text().strip()
        old_password = self.update_pass_old.text().strip()
        new_password = self.update_pass_new.text().strip()

        if not username or not old_password or not new_password:
            QMessageBox.warning(self, "Validation Error", "All fields are required for password update.")
            return

        if old_password == new_password:
            QMessageBox.warning(self, "Validation Error", "New password cannot be the same as current password.")
            return

        success, message = update_password_backend(username, old_password, new_password)
        if success:
            QMessageBox.information(self, "✅ Success", message)
            self.update_pass_user.clear()
            self.update_pass_old.clear()
            self.update_pass_new.clear()
        else:
            QMessageBox.warning(self, "❌ Error", message)

    def handle_delete_account(self):
        username = self.delete_user.text().strip()
        password = self.delete_pass.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Username and password are required to delete account.")
            return

        reply = QMessageBox.question(self, 'Confirm Deletion', 
                                     f"Are you sure you want to delete the account '{username}'? This action cannot be undone.", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            success, message = delete_account_backend(username, password)
            if success:
                QMessageBox.information(self, "🗑️ Account Deleted", message)
                self.delete_user.clear()
                self.delete_pass.clear()
                self.switch_to_login() # Go back to login after deleting account
            else:
                QMessageBox.warning(self, "❌ Error", message)
        else:
            QMessageBox.information(self, "Canceled", "Account deletion canceled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    result = app.exec_()
    sys.exit(0 if window.login_successful else 1)