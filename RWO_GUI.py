import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from login_test import get_login_credentials

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("GitHub Login")
        self.setGeometry(500, 500, 300, 150)

        self.username_label = QLabel("GitHub Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("GitHub Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.login_button.clicked.connect(self.on_login)

    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            get_login_credentials(username, password)
        else:
            print("Please enter both a username and a password.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())

