import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType

import classes.adminWindow as adminWindow
import classes.connection as connect
import classes.crypto as crypto
import classes.medicWindow as medicWindow
import classes.multiTool as MT
import classes.nurseWindow as nurseWindow
import classes.receptionistWindow as receptionistWindow

qss_file = open('CSS/qdarkstyle/style.qss').read()                          # Load QSS theme
login_ui, _ = loadUiType('UI/login.ui')                                     # Load UI's

class Login(QtWidgets.QMainWindow, login_ui):                               # create login class
    """
    Login window Class

    Attributes:
        user_id (type):

    Inheritance:
        QMainWindow: Main QT Window
        ui: User Interface that will be used

    Args:
        user_id (Integer): Global variable with the user's ID number
        user_name (String): Global variable with the user's log in name

    """
    def __init__(self, parent = None):
        """
        Initializer for the class Login

        Args:
            self (undefined): The object itself
        Vars:
            QMainWindow.__init__: Initialize the Window
            action*: Creating buttons on the window
            input_Password: Sets the text bar with hidden characters
            login_Button: Sets a shortcut for that button when the user presses "Return" key

        """
        QMainWindow.__init__(self)
        self.setupUi(self)
        loadUiType("UI/login.ui",self)                                      # load ui file
        self.setWindowTitle("Pyclinic")                                     # setup the window title
        self.login_Button.clicked.connect(self.loginFunction)               # connect push button to function
        self.actionQuit.setStatusTip('Fechar o programa.')
        self.actionAbout.setStatusTip('Acerca deste software.')
        self.actionAbout.triggered.connect(lambda:MT.about_section())
        self.actionQuit.triggered.connect(lambda:QApplication.quit())
        self.statusBar()
        self.input_Password.setEchoMode(QtWidgets.QLineEdit.Password)       # makes passwords occult
        self.login_Button.setShortcut("Return")                             # setup keypress shortcut

    def loginFunction(self):
        """
        Starts the login process, checking if the user exists in the database and fetching the necessary information
        for the login to occurr

        Args:
            self (undefined): The object itself
        Vars:
            cipher: crypto class Instance
            username: User's Log in name
            password: User's Log in password
            textBrowser:

        """
        cipher = crypto.passwordHandling()
        self.textBrowser.clear()                                            # Clearing the information text
        username = self.input_UserName.text()
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT utilizador_nome, palavra_passe, funcionario_numero, profissao
                                    FROM `funcionario`
                                    INNER JOIN `id_funcionario`
                                    ON `numero`
                                    LIKE `funcionario_numero`
                                    WHERE (`utilizador_nome` like %s);''', username)
        user = self.cur.fetchone()
        if user:
            password = cipher.hashing(self.input_Password.text(), user[2])
            if user[1] == password[0].decode():
                print("Login Successful")
                self.input_UserName.clear()                                 # Clears string so as not to remain typed after logout
                self.input_Password.clear()
                if user[3] == "Médico":
                   self.goToMedicMainWindow(user[2], user[0])                        # Maybe the number of the employee should be saved somewhere for the session
                elif user[3] == "Funcionário":
                   self.goToReceptionistMainWindow(user[2], user[0])
                elif user[3] == "Administrativo":
                    self.goToAdminMainWindow(user[2], user[0])
                elif user[3] == "Enfermeiro":
                    self.goToNurseMainWindow(user[2], user[0])
            else:
                self.textBrowser.clear()
                self.textBrowser.insertPlainText("Error: Wrong username or password")
        else:
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error: Wrong username or password")


    def goToAdminMainWindow(self, user_id, user_name):                        # Initiate root admin window and closes login window
        """
        Starts the admin window class, so the user sees the admin screen

        Args:
            self (undefined): The object itself
        Vars:
            window: The variable that will hold the admin class instance

        """
        self.window = adminWindow.MainApp(user_id, user_name)

        self.window.show()
        windowLogin.close()

    def goToMedicMainWindow(self, user_id, user_name):
        """
        Starts the meidc window class, so the user sees the medic screen

        Args:
            self (undefined): The object itself
        Vars:
            medicWindow: The variable that will hold the medic class instance

        """
        self.medicWindow = medicWindow.MainApp(user_id, user_name)
        self.medicWindow.show()
        windowLogin.close()

    def goToReceptionistMainWindow(self, user_id, user_name):
        """
        Starts the receptionist window class, so the user sees the receptionist screen

        Args:
            self (undefined): The object itself
        Vars:
            employeeWindow: The variable that will hold the receptionist class instance

        """
        self.employeeWindow = receptionistWindow.MainApp(user_id, user_name)
        self.employeeWindow.show()
        windowLogin.close()

    def goToNurseMainWindow(self, user_id, user_name):
        """
        Starts the nurse window class, so the user sees the nurse screen

        Args:
            self (undefined): The object itself
        Vars:
            employeeWindow: The variable that will hold the nurse class instance

        """
        self.employeeWindow = nurseWindow.MainApp(user_id, user_name)
        self.employeeWindow.show()
        windowLogin.close()

if __name__ == '__main__':
    MT.clearScreen ()                                                      # OS friendly screen clearing
    PyClinic = QApplication(sys.argv)
    windowLogin = Login()
    PyClinic.setStyle('Fusion')                                            # Backup theme
    windowLogin.show()
    sys.exit(PyClinic.exec_())
