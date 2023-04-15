# This is a sample Python script.
import sqlite3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt5 import QtWidgets
import sys
from main_window import Ui_MainWindow
from ui.login_ui import Ui_Form
from ui.failed_auth import Ui_Dialog


class LoginWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skills In Motion")
        self.login_ui = Ui_Form()
        self.login_ui.setupUi(self)
        self.con = sqlite3.connect("attendance_db.sqlite")
        self.cur = self.con.cursor()
        self.login_ui.pushButton.clicked.connect(self.check_user)

    def check_user(self):
        username = self.login_ui.lineEdit.text()
        password = self.login_ui.lineEdit_2.text()
        login_query = "select * from userdata where username = ? and password = ?;"
        res = self.cur.execute(login_query, (username, password)).fetchone()
        if res != None:
            self.main_window = QtWidgets.QMainWindow()
            self.main_ui = Ui_MainWindow()
            self.main_ui.setupUi(self.main_window)
            self.main_window.show()
            login_window.close()
        else:
            self.failed_auth_window = QtWidgets.QDialog()
            self.failed_auth_ui = Ui_Dialog()
            self.failed_auth_ui.setupUi(self.failed_auth_window)
            self.failed_auth_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
