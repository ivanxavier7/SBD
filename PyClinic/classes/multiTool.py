import os
from os import system, sys, name
from PyQt5.QtWidgets import QMessageBox
def Logout():                                               # Log off session function
    """
        Logs off from the user's session

        Args:
            self (undefined): The object itself
        Vars:
            os: Operating System commands

    """
    os.execl(sys.executable, sys.executable, *sys.argv)     # Restart app at logout

def about_section():                                        # Show an "about" message screen
    """
        Shows the information about the software itself

        Args:
            self (undefined): The object itself
        Vars:
            abtoutM: The variable that holds the popup with the message that will be shown.

    """
    abtoutM = QMessageBox()
    abtoutM.setWindowTitle("Acerca de:")
    abtoutM.setText("Software de gestão de uma clínica criado para um projecto académico na Escola Superior de Tecnologia de Águeda, 2021. Este projecto foi realizado com recurso à linguagem Python e à framework PyQt5 usando Qt Designer.")
    abtoutM.setIcon(QMessageBox.Information)
    abtoutM.exec_()

def clearScreen():
    """
        Clears the screen

        Args:
            self (undefined): The object itself
        Vars:
            name: Different for each Operating System

    """
    if name == 'nt':                                        # For windows os
        _ = system('cls')
    else:
        _ = system('clear')                                 # For mac and linux os(The name is posix)