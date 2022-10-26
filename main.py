import sys
import re
import sqlite3
from PyQt6.uic import loadUi
from mainconverter import Mainconverter
import edit_database
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QStackedWidget,
    QMessageBox
)


class Ui_currency_converter_frame(QWidget):
    def __init__(self):
        super(Ui_currency_converter_frame, self).__init__()
        loadUi('qt_ui.ui', self)

        self.email_entry = self.findChild(QLineEdit, "email_entry")
        self.password_entry = self.findChild(QLineEdit, "password_entry")
        self.email_entry_register = self.findChild(QLineEdit, "email_entry_register")
        self.password_entry_register = self.findChild(QLineEdit, "password_entry_register")
        self.confirm_password_entry = self.findChild(QLineEdit, "confirm_password_entry")
        self.register_button = self.findChild(QPushButton, "register_button")
        self.signin_button = self.findChild(QPushButton, "signin_button")
        self.signin_page = self.findChild(QWidget, "signin_page")
        self.signin_page_button = self.findChild(QPushButton, "signin_page_button")
        self.register_page = self.findChild(QWidget, "register_page")
        self.register_page_button = self.findChild(QPushButton, "register_page_button")
        self.stacked = self.findChild(QStackedWidget, "stackedWidget")

        self.stacked.setCurrentIndex(0)

        self.register_page_button.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        self.signin_page_button.clicked.connect(lambda: self.stacked.setCurrentIndex(0))


        self.signin_button.clicked.connect(self.validate_signin)
        self.register_button.clicked.connect(self.validate_register)

    def create_window(self):
        self.window = Mainconverter()
        Mainconverter.setUp(self.window)
        self.window.show()
    def validate_signin(self):
        msg = QMessageBox()
        msg.setWindowTitle("Sign in")
        username = self.email_entry.text()
        password = self.password_entry.text()

        conn = sqlite3.connect('customers.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM customers ")

        for item in c.fetchall():
            if username == item[0] and password == item[1]:
                msg.setText(f"Welcome in {username}")
                edit_database.update_logged_in(username)
                self.create_window()
                break
            else:
                msg.setText("Incorrect username and/or password")

        x = msg.exec()

        conn.commit()
        conn.close()

    def validate_register(self):
        cannot_continue = False
        msg = QMessageBox()
        msg.setWindowTitle("Register")
        register_username = self.email_entry_register.text()
        register_password = self.password_entry_register.text()
        register_confirm_password = self.confirm_password_entry.text()

        conn = sqlite3.connect('customers.db')
        c = conn.cursor()

        c.execute("SELECT * FROM customers")

        for item in c.fetchall():
            if item[0] == register_username:
                cannot_continue = True

        if cannot_continue == False:
            if register_username and register_password and register_confirm_password == register_password:
                if re.search("@.+", register_username):
                        c.execute(f"INSERT INTO customers VALUES ('{register_username}', '{register_password}')")
                        msg.setText(f"An email has been sent to {register_username} to confirm your details")

                        changed_username = register_username.replace("@", "_at_").replace(".", "_dot_")

                        c.execute(f"""CREATE TABLE {changed_username} (
                                pair_one text NOT NULL,
                                preference_one text NOT NULL,
                                preference_two text NOT NULL,
                                preference_three text NOT NULL,
                                preference_four text NOT NULL,
                                preference_five text NOT NULL,
                                preference_six text NOT NULL,
                                preference_seven text NOT NULL,
                                preference_eight text NOT NULL
                            )""")

                        c.execute(f"""INSERT INTO {changed_username} VALUES (
                                'GBP', 'USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CNY', 'HKD'
                        )""")
                                
                        print(register_username + " has been imported into database as " + changed_username)

                        self.stacked.setCurrentIndex(0)

                else:
                    msg.setText("Email must follow the format: 123@example.com")
            else:
                msg.setText("Passwords do not match")
        else:
            msg.setText("User is already registered")

        y = msg.exec()

        self.email_entry_register.clear()
        self.password_entry_register.clear()
        self.confirm_password_entry.clear()

        conn.commit()
        conn.close()

if __name__ == "__main__":
    app = QApplication([])
    window = Ui_currency_converter_frame()
    window.show()
    sys.exit(app.exec())
