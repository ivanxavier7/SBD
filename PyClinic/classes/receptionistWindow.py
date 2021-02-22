import logging
import sys
from datetime import date

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import QDate
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import classes.connection as connect
import classes.crypto as crypto
import classes.multiTool as MT

ui, _ = loadUiType('UI/receptionistWindow.ui')


class Logger():
    """ 
    Creates logs for the user 

    Attributes:
        user_name: The name from the user's account
        message: The message to be displayed
        tipo: The type of message
    """

    def __init__(self, user_name, message, tipo):
        self.log = logging.getLogger(user_name)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler('loggers.log')
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

        if tipo == 'info':
            self.log.info(message)
        elif tipo == 'erro':
            self.log.error(message)


class MainApp(QMainWindow, ui):
    """
    Initializes everything so the window can be shown

    Attributes:
        user_id (type):

    Inheritance:
        QMainWindow: Main QT Window
        ui: User Interface that will be used

    Args:
        user_id (Integer): Global variable with the user's ID number
        user_name (String): Global variable with the user's log in name

    """
    def __init__(self, user_id, user_name):
        """
        Initializer for the class MainApp

        Args:
            self (undefined): The object itself
            user_id (Integer): Global variable with the user's ID number
            user_name (String): Global variable with the user's log in name
        Vars:
            QMainWindow.__init__: Initialize the Window
            action*: Creating buttons on the window

        """
        self.user_id = user_id
        self.user_name = user_name
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui_changes()
        self.setWindowTitle("Pyclinic")                                 # setup the window title
        self.actionQuit.setStatusTip('Fechar o programa.')
        self.actionLogout.setStatusTip('Sair desta sessão.')
        self.actionAbout.setStatusTip('Acerca deste software.')
        self.actionQuit.triggered.connect(lambda:QApplication.quit())
        self.actionAbout.triggered.connect(lambda:MT.about_section())
        self.actionLogout.triggered.connect(lambda:MT.Logout())
        self.statusBar()

    def handle_ui_changes(self):
        """
        Handles page changes, with the index and the widgets used

        Args:
            self (undefined):
        Vars:
            tabWidget*: tab widgets for the window
            date_today: time right now
            calendarScheduling: set the date range

        """
        self.handle_buttons()
        self.tabWidget_2.setCurrentIndex(4)
        date_today = date.today()
        date_today = date_today.strftime("%Y, %m, %d")
        date_today = tuple(map(int, date_today.split(', ')))
        self.calendarScheduling.setDateRange(QDate(date_today[0], date_today[1], date_today[2]), QDate(date_today[0]+1, date_today[1], date_today[2]),)
        self.user_profile()

    def handle_buttons(self):
        """
        This function mainly connects all the buttons that are in the UI to the functions they will run when clicked

        Args:
            self (undefined):
        Vars:
            add*: Connecting add buttons to their respective functions
            edit*: Connecting edit buttons to their respective functions
            delete*: Connecting delete buttons to their respective functions
            search*: Connecting search buttons to their respective functions
            sheet*: Buttons from the patient's sheet
            profile*: Buttons from the user's profile
            nameSearchBar.textEdited.connect(self.search_restore_trigger)
            confirmScheduling.clicked.connect(self.add_appointment)
            tabWidget_*: Disallow/Allow the tab

        """
        self.addPatient.clicked.connect(self.add_patient)
        self.editPatient.clicked.connect(self.edit_patient)
        self.deletePatient.clicked.connect(self.delete_patient)
        self.nameSearchBar.textEdited.connect(self.search_trigger)
        self.searchPatient.clicked.connect(self.search_patient)
        self.confirmScheduling.clicked.connect(self.add_appointment)
        self.searchPatients.clicked.connect(self.check_user_exists)
        self.sheetPatientAppointment.clicked.connect(self.patient_make_appointment)
        self.tabWidget_2.setTabEnabled(3, False)
        self.searchPatient.setEnabled(False)
        self.sheetPatientEdit.clicked.connect(self.search_edit_patient)
        self.sheetPatientAppointmentList.clicked.connect(self.appointment_history)
        self.sheetPatientAppointment.clicked.connect(self.patient_make_appointment)
        self.patient_search_table()
        self.profileChangePass.clicked.connect(self.change_pass)
        self.profileChangeEmail.clicked.connect(self.change_email)
        self.giveJust.clicked.connect(self.appointment_justification)
        self.app_cancel.clicked.connect(self.appointment_cancelation)
        self.searchPatientTrigger.clicked.connect(self.search_trigger)
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap("standardImage.png")
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.graphicsView.setScene(scene)

    # Pop up
    def show_info(self, message):
        """
        This function shows informative messages to the user

        Args:
            self (undefined):
            message (String): Message to be shown in the information pop up
        Vars:
            logger: Instance of Logger()

        """
        logger = Logger(self.user_name, message, "info")
        self.messageLog.clear()
        self.messageLog.setText(message)

    def show_erro(self, message):
        """
        This function shows error messages to the user as a pop up

        Args:
            self (undefined):
            message (String): Message to be shown in the error pop up
        Vars:
            logger: Instance of Logger()

        """
        Logger(self.user_name, message, "erro")
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def user_profile(self):
        """
        Fetches and shows all the information from the current user

        Args:
            self (undefined):
        Vars:
            userIdentificationBox: Sets the number and the name of the employee in the identification box
            profile*: Sets the text box with the user's information

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            numero_funcionario = self.user_id

            self.cur.execute('''SELECT funcionario_numero,
                                    nome,
                                    nr_cartao_cidadao,
                                    nif,
                                    nr_seguranca_social,
                                    data_nascimento,
                                    telefone,
                                    telemovel,
                                    email,
                                    morada,
                                    profissao,
                                    ativo,
                                    utilizador_nome
                                    from id_funcionario inner join funcionario on funcionario_numero = numero where funcionario_numero = %s''', numero_funcionario)
            number = self.cur.fetchone()
            self.userIdentificationBox.setText(str(number[1]) + " | Nr: " + str(numero_funcionario))
            self.profileUserName.setText(str(number[11]))
            self.profileNumber.setText(str(numero_funcionario))
            self.profileName.setText(number[1])
            self.profileIDNr.setText(str(number[2]))
            self.profileNIF.setText(str(number[3]))
            self.profileSocialNr.setText(str(number[4]))
            self.profileDate.setText(str(number[5]))
            self.profileaPhoneNr.setText(str(number[6]))
            self.profileMobileNr.setText(str(number[7]))
            self.profileEmail.setText(number[8])
            self.profileAdress.setText(number[9])
            self.profileJob.setText(number[10])

        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]  # saves the exception on the variable e
            print("An Error Occurred while search profile: %s" % e)  # prints the exception
            self.show_erro("An Error Occurred while search profile: %s " % e)


    def patient_make_appointment(self):
        """
        Sets the number of the patient into the appointment window

        Args:
            self (undefined):
        Vars:
            tabWidget*:
            app_nrUtente: Name of the textbox for the patient's number

        """
        self.tabWidget_2.setTabEnabled(0, True)
        self.tabWidget_2.setCurrentIndex(0)
        self.Consulta.setCurrentIndex(1)
        self.app_nrUtente.setText(self.items[0].text())

    def search_patient(self):
        """
        Shows all the information of the selected patient

        Args:
            self (undefined):
        Vars:
            scen: Initializing the QT widget GraphicsScene
            tabWidget*: Changing or setting the visibility of the tab
            items: selected items on the showPatientsTable
            sheetPatient*: Setting the text of those boxes to the values that came from the Patient Table
        """
        if self.comboBox_2.currentText() == "Utente":
            self.items = self.showPatientsTable.selectedItems()
            self.tabWidget_2.setCurrentIndex(1)
            self.tabWidget_7.setCurrentIndex(1)
            self.sheetPatientNumber.setText(self.items[0].text())
            self.sheetPatientName.setText(self.items[1].text())
            self.sheetPatientIDNr.setText(self.items[2].text())
            self.sheetPatientSocialNr.setText(self.items[3].text())
            self.sheetPatientNIF.setText(self.items[4].text())
            self.sheetPatientDate.setText(self.items[5].text())
            self.sheetPatientPhoneNr.setText(self.items[6].text())
            self.sheetPatientMobileNr.setText(self.items[7].text())
            self.sheetPatientEmail.setText(self.items[8].text())
            self.sheetPatientAddress.setText(self.items[9].text())

    def change_email(self):
        """
        Sets a new email in the employee's information

        Args:
            self (undefined):
        Vars:
            email: The new user's email
            numero: The user's employee number
            profile*: clears all the information in the text boxes

        """
        try:

            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            email = self.profileNewEmail.text()
            numero = self.profileNumber.toPlainText()
            self.cur.execute('''
                UPDATE `id_funcionario` SET
                                                `email` = %s
                WHERE(`funcionario_numero` = %s)
            ''', (email,
                  numero))

            self.db.commit()
            self.show_info("Change email sucessfully whose nr: %s " %numero)

            self.db.close()

            self.profileEmail.setText(email)
            self.profileNewEmail.clear()

        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while change email: %s" % exception)    # prints the exception
            self.show_erro("An Error Occurred while change email whose nr, %s :\n %s" %(numero, exception))


    def change_table_atributes(self):
        """
        Sets up the table so all the information can be shown, depending on the combo box choice the user made

        Args:
            self (undefined):
        Vars:
            comboBox_2: Combo box that the user can choose from
            showPatientsTable: Sets the table so the data can be shown

        """
        if str(self.comboBox_2.currentText()) == "Utente":
            self.searchPatient.setEnabled(True)
            self.showPatientsTable.setColumnCount(10)
            self.showPatientsTable.setHorizontalHeaderLabels(("Utente",
                                                              "Nome",
                                                              "Cartão Cidadão",
                                                              "NIF",
                                                              "Segurança Social",
                                                              "Data Nascimento",
                                                              "Telefone",
                                                              "Telemóvel",
                                                              "Email",
                                                              "Morada"))
        if str(self.comboBox_2.currentText()) == "Funcionário":
            self.searchPatient.setEnabled(False)
            self.showPatientsTable.setColumnCount(11)
            self.showPatientsTable.setHorizontalHeaderLabels(("Funcionário",
                                                              "Nome",
                                                              "Cartão Cidadão",
                                                              "NIF",
                                                              "Segurança Social",
                                                              "Data Nascimento",
                                                              "Telefone",
                                                              "Telemóvel",
                                                              "Email",
                                                              "Profissão",
                                                              "Morada"
                                                              ))
        self.search_trigger()

    def patient_search_table(self):
        """
        Shows the information from the patients on the table

        Args:
            self (undefined):
        Vars:
            visitTable: gets the number of rows the table will have and sets them all as they should be
        """
        self.db = connect.connection(self)
        self.cur = self.db.cursor()

        self.visitTable.setRowCount(self.cur.execute(
            "select data, utente_numero, funcionario_numero from consulta "
            "where utente_numero in"
            "(select numero from utente where ativo = 1) "
            "order by data desc limit 10;"
            ))

        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            for self.valor in self.tuplo:
                self.visitTable.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                self.j = self.j + 1
                if self.j == 3:
                    self.cur.execute(
                        "select nome, telemovel, morada from utente where numero = %s;"
                        , self.tuplo[1]
                    )
                    self.dados = self.cur.fetchall()[0]
                    for self.dados1 in self.dados:
                        self.visitTable.setItem(self.i, self.j, QTableWidgetItem(str(self.dados1)))
                        self.j = self.j + 1
            self.i = self.i + 1



    def search_trigger(self):
        """
        Searches information based on the comboBoxes that were selected by the user

        Args:
            self (undefined):
        Vars:
            comboBox*: Combo Boxes with various choices for the user
            searchType: Name of the relationship
            searchItem: Name of the Attribute
            showPatientsTable: Sets the table with the right values to be shown

        """
        self.db = connect.connection(self)
        self.cur = self.db.cursor()

        if str(self.comboBox.currentText()) == "Nome":
            self.searchItem = "nome"
        else:
                self.searchItem = "numero"

        self.showPatientsTable.setRowCount(self.cur.execute(
            "SELECT * FROM utente WHERE {} LIKE '%{}%' and ativo = 1;".format(self.searchItem,
                                                                              self.nameSearchBar.text())))

        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            for self.valor in self.tuplo:
                self.showPatientsTable.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                self.j = self.j + 1
            self.i = self.i + 1
        self.db.close()

    def search_edit_patient(self):
        """
        Sets all the values to the window so the user can edit all it's information

        Args:
            self (undefined):
        Vars:
            tabWidget_2: Sets the widget visible and in the right index
            editPatient*: Values to be edited by the user 

        """
        self.tabWidget_2.setTabEnabled(3, True)
        self.tabWidget_2.setCurrentIndex(3)
        self.editPatientName.setText(self.sheetPatientName.toPlainText())
        self.editPatientNumber.setText(self.sheetPatientNumber.toPlainText())
        self.editPatientDate.setText(self.sheetPatientDate.toPlainText())
        self.editPatientAddress.setText(self.sheetPatientAddress.toPlainText())
        self.editPatientEmail.setText(self.sheetPatientEmail.toPlainText())
        self.editPatientIDNr.setText(self.sheetPatientIDNr.toPlainText())
        self.editPatientMobileNr.setText(self.sheetPatientMobileNr.toPlainText())
        self.editPatientNIF.setText(self.sheetPatientNIF.toPlainText())
        self.editPatientPhoneNr.setText(self.sheetPatientPhoneNr.toPlainText())
        self.editPatientSocialNr.setText(self.sheetPatientSocialNr.toPlainText())

    def check_user_exists(self):
        """
        Checks if the user with the number that was inserted exists in the database

        Args:
            self (undefined):
        Vars:
            number: Patient Number
            name: Patient Name

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            number = self.addPatientNr.text()
            self.cur.execute('''SELECT `nome` FROM `utente` where `numero` = %s''', number)
            name = self.cur.fetchone()
            if name == None:
                self.db.commit()
                self.show_info("The patient does not yet exist")
                self.db.close()
            else:
                self.show_erro("Patient already existis, is %s" %name)
        except AttributeError:                                                                     # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while adding a new patient: %s" % exception)                  # prints the exception
            self.show_erro("An Error Occurred while check number patiente")

    def add_patient(self):
        """
        Add a new patient to the database

        Args:
            self (undefined):
        Vars:
            patient_*: Patient information

        """
        self.change_table_atributes()
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            patient_nr = self.addPatientNr.text()
            patient_name = self.addPatientName.text()
            patient_id_nr = self.addPatientIDNr.text()
            patient_social_nr = self.addPatientSocialNr.text()
            patient_nif = self.addPatientNIF.text()
            patient_date = self.addPatientDate.text()
            patient_phone_nr = self.addPatientPhoneNr.text()
            patient_mobile_nr = self.addPatientMobileNr.text()
            patient_email = self.addPatientEmail.text()
            patient_street = self.addPatientStreet.text()
            patient_home_nr = self.addPatientHomeNr.text()
            patient_postal = self.addPatientPostalCode.text()
            patient_address = (patient_street + ", nº" + patient_home_nr + ", " + patient_postal)

            if patient_phone_nr == "":
                patient_phone_nr = None
            if patient_email == "":
                patient_email = "None"

            if patient_date > str(date.today()):
                self.show_erro("Date is invalid")
            else:
                # Date should be passed in this format : '2020-01-01'
                self.cur.execute('''
                        INSERT INTO `utente` (`numero`,
                                                        `nome`,
                                                        `nr_cartao_cidadao`,
                                                        `nr_seg_social`,
                                                        `nif`,
                                                        `data_nascimento`,
                                                        `telefone`,
                                                        `telemovel`,
                                                        `email`,
                                                        `morada`,
                                                        `ativo`)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    ''', (patient_nr,
                          patient_name,
                          patient_id_nr,
                          patient_social_nr,
                          patient_nif,
                          patient_date,
                          patient_phone_nr,
                          patient_mobile_nr,
                          patient_email,
                          patient_address,
                          True))
                self.db.commit()
                self.show_info("Add patient sucessfully whose nr: %s " % patient_nr)
                self.db.close()

                self.tabWidget_2.setCurrentIndex(4)

                self.addPatientNr.clear()
                self.addPatientName.clear()
                self.addPatientIDNr.clear()
                self.addPatientSocialNr.clear()
                self.addPatientNIF.clear()
                self.addPatientDate.clear()
                self.addPatientPhoneNr.clear()
                self.addPatientMobileNr.clear()
                self.addPatientEmail.clear()
                self.addPatientStreet.clear()
                self.addPatientHomeNr.clear()
                self.addPatientPostalCode.clear()
        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while adding a new patient: %s" % exception)  # prints the exception
            self.show_erro("An Error Occurred while adding a new patient")

    def edit_patient(self):
        """
        Edit the patient's information

        Args:
            self (undefined):
        Vars:
            editPatient*: Information that will override the information in the database
            tabWidget_2: Set the right window and tab for the user

        """
        try:
            print(self.editPatientNumber.text())
            print(self.sheetPatientNumber.toPlainText())
            if self.editPatientNumber.text() != self.sheetPatientNumber.toPlainText():
                self.change_table_atributes()
                self.db = connect.connection(self)
                self.cur = self.db.cursor()
                self.cur.execute('''
                UPDATE `utente` SET
                                        `ativo` = %s
                WHERE(`numero` = %s); ''', (False,self.sheetPatientNumber.toPlainText()))
                self.db.commit()
                self.show_info("Edit patient sucessfully whose nr: %s " % self.editPatientNumber.text())
                self.db.close()
                self.db = connect.connection(self)
                self.cur = self.db.cursor()
                self.cur.execute('''
                INSERT INTO `utente` (`numero`,
                                        `nome`,
                                        `nr_cartao_cidadao`,
                                        `nr_seg_social`,
                                        `nif`,
                                        `data_nascimento`,
                                        `telefone`,
                                        `telemovel`,
                                        `email`,
                                        `morada`,
                                        `ativo`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    ''',  (self.editPatientNumber.text(),
                          self.editPatientName.text(),
                          self.editPatientNumber.text(),
                          self.editPatientNIF.text(),
                          self.editPatientSocialNr.text(),
                          self.editPatientDate.text(),
                          self.editPatientPhoneNr.text(),
                          self.editPatientMobileNr.text(),
                          self.editPatientEmail.text(),
                          self.editPatientAddress.text(),
                          True))
                self.db.commit()
                self.show_info("Edit patient sucessfully whose nr: %s " % self.editPatientNumber.text())
                self.db.close()
            else:
                self.change_table_atributes()
                self.db = connect.connection(self)
                self.cur = self.db.cursor()
                self.cur.execute('''
                            UPDATE `utente` SET
                                                    `nome` = %s,
                                                    `nr_cartao_cidadao` = %s,
                                                    `nif` = %s,
                                                    `nr_seg_social` = %s,
                                                    `data_nascimento` = %s,
                                                    `telefone` = %s,
                                                    `telemovel` = %s,
                                                    `email` = %s,
                                                    `morada` = %s,
                                                    `ativo` = %s
                            WHERE (`numero` = %s);
                        ''', (self.editPatientName.text(),
                            self.editPatientIDNr.text(),
                            self.editPatientNIF.text(),
                            self.editPatientSocialNr.text(),
                            self.editPatientDate.text(),
                            self.editPatientPhoneNr.text(),
                            self.editPatientMobileNr.text(),
                            self.editPatientEmail.text(),
                            self.editPatientAddress.text(),
                            True,
                            self.editPatientNumber.text()))
                self.db.commit()
                self.show_info("Edit patient sucessfully whose nr: %s " % self.editPatientNumber.text())
                self.db.close()
            self.search_trigger()                                                                   # Prints the exception
            self.tabWidget_2.setCurrentIndex(1)
            self.tabWidget_7.setCurrentIndex(1)
            self.sheetPatientNumber.setText(self.editPatientNumber.text())
            self.sheetPatientName.setText(self.editPatientName.text())
            self.sheetPatientIDNr.setText(self.editPatientNIF.text())
            self.sheetPatientSocialNr.setText(self.editPatientSocialNr.text())
            self.sheetPatientNIF.setText(self.editPatientNIF.text())
            self.sheetPatientDate.setText(self.editPatientDate.text())
            self.sheetPatientPhoneNr.setText(self.editPatientPhoneNr.text())
            self.sheetPatientMobileNr.setText(self.editPatientMobileNr.text())
            self.sheetPatientEmail.setText(self.editPatientEmail.text())
            self.sheetPatientAddress.setText(self.editPatientAddress.text())
            self.tabWidget_2.setTabEnabled(3, False)
            self.editPatientName.clear()
            self.editPatientIDNr.clear()
            self.editPatientNIF.clear()
            self.editPatientSocialNr.clear()
            self.editPatientDate.clear()
            self.editPatientPhoneNr.clear()
            self.editPatientMobileNr.clear()
            self.editPatientEmail.clear()
            self.editPatientAddress.clear()
            self.editPatientNumber.clear()
        except AttributeError:                                                                     # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while edit patient: %s" % exception)                          # prints the exception
            self.show_erro("An Error Occurred while edit a patient whose nr, %s :\n %s" % (self.editPatientNumber.text(), exception))

    def delete_patient(self):
        """
        Delete the patient from the database. It is not really a delete, but a set as inactive

        Args:
            self (undefined):
        Vars:
            editPatient*: User's information. The user has been set to inactive
        """
        try:
            self.change_table_atributes()
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            self.cur.execute('''
                UPDATE `utente` SET
                                        `ativo` = %s
                WHERE(`numero` = %s)
            ''', (False,
                  self.editPatientNumber.text()))
            self.db.commit()
            self.show_info("Delete patient sucessfully whose nr: %s " % self.editPatientNumber.text())
            self.db.close()
            self.editPatientName.clear()
            self.editPatientIDNr.clear()
            self.editPatientNIF.clear()
            self.editPatientSocialNr.clear()
            self.editPatientDate.clear()
            self.editPatientPhoneNr.clear()
            self.editPatientMobileNr.clear()
            self.editPatientEmail.clear()
            self.editPatientAddress.clear()
            self.editPatientNumber.clear()
        except AttributeError:                                                                     # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while deleting a patient: %s" % exception)                    # prints the exception
            self.show_erro("An Error Occurred while deleting a patient whose nr, %s :\n %s" % (self.editPatientNumber.text(), exception))




    def change_pass(self):
        """
        Sets a new password in the employee's information

        Args:
            self (undefined):
        Vars:
            cipher: Instance of the class crypto
            numero: The user's employee number
            profile*: clears all the information in the text boxes
            pass_atual: The hashed previous password
            pass_nova: An array with the new hashed password and the secret key that hashed the new password, that will be saved in the database
            nova: The hashed password
            chave: The secret key
            profile*: Clears the text boxes

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            cipher = crypto.passwordHandling()

            numero = self.profileNumber.toPlainText()
            pass_atual = cipher.hashing(self.profileCurrentPass.text(), self.user_id)
            pass_nova = cipher.hashing(self.profileNewPass.text(), 0)

            self.cur.execute('''SELECT `palavra_passe` FROM `funcionario` where `numero` = %s''', numero)
            password = self.cur.fetchone()

            if password[0] == pass_atual[0].decode():
                if self.profileNewPass.text() == self.profileRepPass.text():
                    nova = pass_nova[0].decode().strip()
                    chave = pass_nova[1]
                    self.cur.execute('''
                        UPDATE funcionario SET
                            palavra_passe = %s,
                            secret_key = %s
                        WHERE(`numero` = %s)
                    ''', (nova,
                          chave,
                          numero))

                    self.db.commit()

                    self.show_info("Change password sucessfully whose nr: %s " % numero)

                    self.db.close()

                    self.profileNewPass.clear()
                    self.profileCurrentPass.clear()
                    self.profileRepPass.clear()

                else:
                    self.show_erro("Enter the password again")
            else:
                self.show_erro("Password Incorrect")

        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while changing password: %s" % exception)  # prints the exception
            self.show_erro("An Error Occurred while changing password whose nr, %s :\n %s" % (numero, exception))


    # Consultas

    def add_appointment(self):
        """
        Add an appointment to the patient

        Args:
            self (undefined):
            app_*: Information from the appointment
            sch_*: Gets the appointment information
            total_DayTime: Helper for the convertions
            busy_Slot: Check if there is already an appointment for that specific period of time

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            app_date = self.calendarScheduling.selectedDate().toPyDate()
            app_utente = self.app_nrUtente.text()
            sch_doctor = self.app_dtr.text()
            sch_description = self.app_description.toPlainText()
            app_time = self.timeScheduling.time().toString(Qt.DefaultLocaleShortDate).split(" ")
            total_DayTime = 0
            try:
                if app_time[1] == 'PM':
                    total_DayTime += 720  # 12H x 60M
            except:
                pass

            self.cur.execute('''SELECT profissao FROM id_funcionario
                                            WHERE funcionario_numero
                                             = %s;''', (sch_doctor))

            funcionario = self.cur.fetchone()

            if str(funcionario[0]) == "Médico":

                app_time = app_time[0].split(':')
                total_DayTime += int(app_time[0]) * 60 + int(app_time[1])  # H x 60 + M
                busy_Slot = self.cur.execute('''SELECT * FROM consulta
                                            WHERE funcionario_numero
                                            LIKE %s and data = %s and hora > %s and hora < %s;''', (
                sch_doctor,
                app_date,
                total_DayTime - 30,
                total_DayTime + 30))
                if busy_Slot == 0:
                    self.cur.execute('''INSERT INTO consulta (
                                `data`,
                                `utente_numero`,
                                `relatorio_consulta`,
                                `funcionario_numero`,
                                `aviso_consulta`,
                                `hora`)
                                VALUES (%s, %s, %s, %s, %s, %s);
                                ''', (app_date,
                                      app_utente,
                                      sch_description,
                                      sch_doctor,
                                      sch_description,
                                      total_DayTime))
                    self.db.commit()
                    print('done')
                    self.show_info(
                    "Add appointment sucessfully whose date, %s and utente number, %s " % (app_date, app_utente))
                    app_utente = self.app_nrUtente.clear()
                    self.app_dtr.clear()
                    self.app_description.clear()

                else:
                    print("It is not available at this time for the appointment!")
                    self.show_erro("It is not available at this time for the appointment!")
                    self.db.close()
            else:
                self.show_erro("Only Doctors can have appointments to their name: Change employee number")
        except Exception as exception:
            if exception.__class__.__name__ == "DataError":
                print("Missing doctor or patient number!")
                self.show_erro("Missing doctor or patient number!")
            elif exception.__class__.__name__ == "IntegrityError":
                print("The patient already has an appointment for this day!")
                self.show_erro("The patient already has an appointment for this day!")
            else:
                print("An Error Occurred while adding a appointment: %s" % exception)  # - The employee number is wrong
                self.show_erro("An Error Occurred while adding a appointment whose date, %s and utente number, %s :\n %s " % (
                    app_date,
                    app_utente, exception))
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_7.setCurrentIndex(0)

    def visit_table_update(self, procurar_por, funcionario):
        """
        Fetches all the information for the table to be shown and set up
        Args:
            self (undefined):
        Vars:
            visitTableUtente: Gets the table

        """
        procurar_por = "cliente"  # situacao a alterar assim que possivel com login
        funcionario = "administrativo"
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        if funcionario == "administrativo":
            self.visitTableUtente.setRowCount(self.cur.execute(
                "SELECT data,utente_numero,funcionario_numero FROM consulta WHERE utente_numero = {};"
                .format(self.sheetPatientNumber.toPlainText())))
            self.i = 0
            for self.tuplo in self.cur.fetchall():
                self.j = 0
                for self.valor in self.tuplo:
                    self.visitTableUtente.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                    self.j = self.j + 1
                self.i = self.i + 1
        else:
            if procurar_por == "cliente":
                self.visitTableUtente.setRowCount(self.cur.execute(
                    "SELECT data,utente_numero,medicacao_administrada, relatorio_consulta FROM consulta WHERE utente_numero = {};"
                    .format(self.sheetPatientNumber.toPlainText())))
            elif procurar_por == "funcionário":
                self.visitTableUtente.setRowCount(self.cur.execute(
                    "SELECT data,utente_numero,medicacao_administrada, relatorio_consulta FROM consulta WHERE funcionario_numero = {};"
                    .format("33")))
            self.i = 0
            for self.tuplo in self.cur.fetchall():
                self.j = 0
                for self.valor in self.tuplo:
                    self.visitTableUtente.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                    if self.j == 1:
                        self.numero_utente = str(self.valor)
                        self.j = self.j + 1
                        self.cur.execute(
                            """SELECT consulta_utente_numero FROM prescricao WHERE
                             consulta_utente_numero = {} AND
                             consulta_data = "{}";"""
                                .format(self.numero_utente, self.tuplo[0]))
                        self.visitTableUtente.setItem(self.i, self.j, QTableWidgetItem(str(len(self.cur.fetchall()))))
                    self.j = self.j + 1
                self.i = self.i + 1
            self.addReportDescription.setReadOnly(True)



    def appointment_history(self):
        """
        Shows the appointment history for a specific patient

        Args:
            self (undefined):
        Vars:
            tabWidget*: Sets the right tab for the user
            openReport: Sets the report to be shown to the user

        """
        self.visit_table_update("cliente","administrativo")
        self.tabWidget_7.setTabEnabled(0, True)
        self.tabWidget_7.setCurrentIndex(0)

    def appointment_cancelation(self):
        """
        Cancels the appointment.

        Args:
            self (undefined):
        Vars:
            msgs: Creates the message that will be printed as the justification
            choice: Creates a box with a double choice for the user
            delete: Fetches all the selected information from the appointment that is supposed to be deleted
            tabWidget*: Shows the right tab to the user

        """

        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        msgs = QMessageBox()
        msgs.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgs.setWindowTitle("ELiminação da Consulta")
        msgs.setText("Tem a certeza que pretende eliminar esta consulta?")
        msgs.setIcon(QMessageBox.Warning)
        choice = msgs.exec_()
        if choice == QMessageBox.Ok:
            try:
                delete = self.visitTableUtente.selectedItems()
                self.cur.execute('''DELETE FROM consulta WHERE data = %s ''', delete[0].text())
                self.db.commit()
                self.db.close()
            except IndexError:
                self.show_erro("Tem de selecionar uma consulta para eliminar!")
            except Exception as e:
                if e.__class__.__name__ == 'IntegrityError':
                    self.show_erro("Não pode desmarcar Consultas que já aconteceram!")
        elif choice == QMessageBox.Cancel:
            self.tabWidget_7.setCurrentIndex(0)

    def appointment_justification(self):
        """
        Creates a file that shows that the patient was in fact in an appointment

        Args:
            self (undefined):
        Vars:
            dados: Gets the data from the selected items from the self.visitTableUtente table
            hora: Calculates the hour
            minutos: Calculate the minutes
            minutos_final: Calculates the end of the appointment
            nomes: Fetches the name of the patient
            msg: Creates the message that will be printed as the justification

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()

            dados = self.visitTableUtente.selectedItems()
            self.cur.execute('''SELECT `hora` FROM `consulta` where `data` = %s ''', dados[0].text())
            hora = self.cur.fetchone()
            self.db.close()
            hora = hora[0] / 60
            minutos = hora - int(hora)
            minutos = minutos * 60
            minutos_final = minutos + 30
            hora_final = hora
            if minutos_final >= 60:
                minutos_final = minutos_final - 60
                hora_final = hora_final + 1
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT `nome` FROM utente inner join consulta on utente_numero = numero where data = %s and utente_numero = %s''', (dados[0].text(), dados[1].text()))
            nomes = self.cur.fetchone()
            self.db.close()
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT `utilizador_nome` FROM funcionario inner join consulta on funcionario_numero = numero where funcionario_numero = %s ''', (dados[2].text()))
            func = self.cur.fetchone()
            print(func)
            msg = QMessageBox()
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setWindowTitle("Justificação Para impressão")
            msg.setText('''Serve o Presente documento como comprovativo que o utente: %s esteve presente na clínica tendo dado entrada às: %s:%02d  e tendo recebido alta às: %s:%02d no dia: %s Por ser verdade segue assinada pelo Médico: %s''' % (nomes[0], int(hora), int(minutos), int(hora_final) , int(minutos_final), dados[0].text(), func[0]))
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except IndexError:
            self.show_erro("Selecione Consulta para passar justificação!")
