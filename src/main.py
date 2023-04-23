# Import necessary modules and libraries
import sqlite3
import sys
from PyQt5 import QtWidgets

# Import the UI classes from the relevant files
from ui.failed_auth import Ui_Dialog
from ui.login_ui import Ui_Form
from ui.main_window import Ui_MainWindow


# Create a new class called 'LoginWindow' that extends the 'QWidget' class
class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Set the window title to "Skills In Motion"
        self.setWindowTitle("Skills In Motion")
        # Initialize the UI from the 'login_ui.py' file
        self.login_ui = Ui_Form()
        self.login_ui.setupUi(self)
        # Connect to the 'attendance_db.sqlite' database
        self.con = sqlite3.connect("../attendance_db.sqlite")
        # Create a cursor object to interact with the database
        self.cur = self.con.cursor()
        # Connect the 'check_user' function to the 'Login' button's clicked signal
        self.login_ui.pushButton.clicked.connect(self.check_user)

    def check_user(self):
        # Get the username and password from the login form
        username = self.login_ui.lineEdit.text()
        password = self.login_ui.lineEdit_2.text()
        # Query the 'userdata' table to find a row with the given username and password
        login_query = "select * from userdata where username = ? and password = ?;"
        # Execute the query with the given parameters using the cursor object
        res = self.cur.execute(login_query, (username, password)).fetchone()
        # If a row is returned, the username and password are correct
        if res != None:
            # Create a new main window
            self.main_window = QtWidgets.QMainWindow()
            # Initialize the UI from the 'main_window.py' file
            self.main_ui = Ui_MainWindow()
            self.main_ui.setupUi(self.main_window)
            # Show the main window and close the login window
            self.main_window.show()
            login_window.close()
        # If no row is returned, the username and/or password are incorrect
        else:
            # Create a new failed authentication window
            self.failed_auth_window = QtWidgets.QDialog()
            # Initialize the UI from the 'failed_auth.py' file
            self.failed_auth_ui = Ui_Dialog()
            self.failed_auth_ui.setupUi(self.failed_auth_window)
            # Show the failed authentication window
            self.failed_auth_window.show()


# The main execution starts here
if __name__ == "__main__":
    # Create a new QApplication object
    app = QtWidgets.QApplication(sys.argv)
    # Create a new LoginWindow object
    login_window = LoginWindow()
    # Show the login window
    login_window.show()
    # Start the event loop and exit the application on exit signal
    sys.exit(app.exec_())
