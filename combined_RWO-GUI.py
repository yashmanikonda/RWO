import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RWO")
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

        driver.maximize_window()
        driver.get('https://github.com/login')

        username_element = driver.find_element(By.ID, 'login_field')
        username_element.clear()
        username_element.send_keys(username)

        password_element = driver.find_element(By.ID, 'password')
        password_element.clear()
        password_element.send_keys(password)

        sign_in_button = driver.find_element(By.CLASS_NAME, 'js-sign-in-button')
        sign_in_button.click()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
