import os
from datetime import date, datetime
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QDate
import classes.connection as connect
import classes.crypto as crypto
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PIL import Image
import io
import logging
import classes.multiTool as MT

ui, _ = loadUiType('UI/adminWindow.ui')


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
        self.setWindowTitle("Pyclinic")
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
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(4)
        date_today = date.today()
        date_today = date_today.strftime("%Y, %m, %d")
        date_today = tuple(map(int, date_today.split(', ')))
        self.calendarScheduling.setDateRange(QDate(date_today[0], date_today[1], date_today[2]),
                                            QDate(date_today[0]+1, date_today[1], date_today[2]),)  # setDateRange(QDate(Begin), QDate(End))
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
        self.addEmployee.clicked.connect(self.add_employee)
        self.editEmployee.clicked.connect(self.edit_employee)
        self.addExamFile.clicked.connect(self.add_exam_file)
        self.addAppointmentExam.clicked.connect(self.add_appointment_exam)
        self.addPatient.clicked.connect(self.add_patient)
        self.editPatient.clicked.connect(self.edit_patient)
        self.deletePatient.clicked.connect(self.delete_patient)
        self.searchPatientTrigger.clicked.connect(self.search_restore_trigger)
        self.nameSearchBar.textEdited.connect(self.search_restore_trigger)
        self.searchPatient.clicked.connect(self.search_patient)
        self.deleteEmployee.clicked.connect(self.delete_employee)
        self.confirmScheduling.clicked.connect(self.add_appointment)
        self.sheetPatientAppointment.clicked.connect(self.patient_make_appointment)
        self.comboBox_2.currentIndexChanged.connect(self.change_table_atributes)
        self.tabWidget_7.setTabEnabled(0, False)
        self.tabWidget_7.setTabEnabled(1, False)
        self.tabWidget_7.setTabEnabled(2, False)
        self.tabWidget_2.setTabEnabled(3, False)
        self.tabWidget_1.setTabEnabled(2, False)
        self.searchPatient.setEnabled(False)
        self.openReport.setEnabled(False)
        self.showPatientsTable.itemSelectionChanged.connect(self.show_table_changed)
        self.visitTable.itemSelectionChanged.connect(self.visit_table_changed)
        self.sheetPatientEdit.clicked.connect(self.search_edit_patient)
        self.sheetPatientAppointmentList.clicked.connect(self.appointment_history)
        self.sheetPatientAppointment.clicked.connect(self.patient_make_appointment)
        self.openReport.clicked.connect(self.open_report_helper_1)
        self.sheetEmployeeEdit.clicked.connect(self.sheet_edit_employee)
        self.tabWidget_5.setTabEnabled(0, False)
        self.tabWidget_5.setTabEnabled(2, False)
        self.giveJust.clicked.connect(self.appointment_justification)
        self.patient_search_table()
        self.profileChangeEmail.clicked.connect(self.change_email)
        self.profileChangePass.clicked.connect(self.change_pass)
        self.nurseButtExamHist.clicked.connect(self.exam_history)
        self.openExame.clicked.connect(self.show_image)
        self.searchPatients_3.clicked.connect(self.check_user_exists)
        self.openReport_3.setEnabled(False)
        self.openReport_3.clicked.connect(self.open_report_helper_2)
        self.app_cancel.clicked.connect(self.appointment_cancelation)
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap("standardImage.png")
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.graphicsView.setScene(scene)

        self.showExamButton.clicked.connect(self.show_button_Exam)
        self.showAppointmentButton.clicked.connect(self.show_button_Appointment)

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
        logger = Logger(self.user_name, message, "erro")
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

# Search triggers

    def open_report_helper_1(self):
        """
        Gets everything ready for the report to be shown

        Args:
            self (undefined):
        Vars:
            items: selected items on the visitTableUtente
            n_utente: Patient's number
            data_consulta: Appointment's Date

        """
        self.items = self.visitTableUtente.selectedItems()
        self.n_utente = self.items[1].text()
        self.data_consulta = str(self.items[0].text())
        self.open_report(self.n_utente, self.data_consulta)

    def open_report_helper_2(self):
        """
        Gets everything ready for the report to be shown

        Args:
            self (undefined):
        Vars:
            items: selected items on the visitTableUtente
            n_utente: Patient's number
            data_consulta: Appointment's Date
        """
        self.items = self.visitTable.selectedItems()
        self.n_utente = self.items[1].text()
        self.data_consulta = str(self.items[0].text())
        self.open_report(self.n_utente, self.data_consulta)


    def show_table_changed(self):
        """
        Makes the button clickable

        Args:
            self (undefined):
        Vars:
            searchPatient.setEnabled(True): Making the button clickable

        """
        self.searchPatient.setEnabled(True)

# Patients

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
        self.tabWidget_1.setCurrentIndex(1)
        self.app_nrUtente.setText(self.sheetPatientNumber.toPlainText())

    def search_patient(self):
        """
        Shows all the information of the selected patient

        Args:
            self (undefined):
        Vars:
            scen: Initializing the QT widget GraphicsScene
            tabWidget*: Changing or setting the visibility of the tab
            items: selected items on the showPatientsTable
            sheet*: Setting the text of those boxes to the values that came from the Patient Table
        """
        try:
            if self.comboBox_2.currentText() == "Utente":
                scen = QtWidgets.QGraphicsScene(self)
                scen.clear()
                self.graphicsExamView.setScene(scen)
                self.tabWidget_7.setTabEnabled(1, True)
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
            else:
                self.tabWidget_5.setTabEnabled(0, True)
                self.items = self.showPatientsTable.selectedItems()
                self.tabWidget.setCurrentIndex(1)
                self.tabWidget_5.setCurrentIndex(0)
                self.sheetEmployeeNumber.setText(self.items[0].text())
                self.sheetEmployeeName.setText(self.items[1].text())
                self.sheetEmployeeIDNr.setText(self.items[2].text())
                self.sheetEmployeeSocialNr.setText(self.items[4].text())
                self.sheetEmployeeNIF.setText(self.items[3].text())
                self.sheetEmployeeDate.setText(self.items[5].text())
                self.sheetEmployeePhoneNr.setText(self.items[6].text())
                self.sheetEmployeeMobileNr.setText(self.items[7].text())
                self.sheetEmployeeEmail.setText(self.items[8].text())
                self.sheetEmployeeJob.setText(self.items[9].text())
                self.sheetEmployeeAddress.setText(self.items[10].text())
        except Exception as exception:
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget_2.setCurrentIndex(4)
            print("Please select a row in the table: %s" % exception)                               # prints the exception
            self.show_erro("Please select a row in the table!")

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

    def search_restore_trigger(self):
        """
        Calls the functions so the table is updated

        Args:
            self (undefined):

        """
        self.change_table_atributes()
        self.search_trigger()

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
        if str(self.comboBox_2.currentText()) == "Utente":
            self.searchType = "utente"
        else:
            self.searchType = "id_funcionario"
        if str(self.comboBox.currentText()) == "Nome":
            self.searchItem = "nome"
        else:
            if self.searchType == "utente":
                self.searchItem = "numero"
            else:
                self.searchItem = "funcionario_numero"
        self.showPatientsTable.setRowCount(self.cur.execute(
            "SELECT * FROM {} WHERE {} LIKE '%{}%' and ativo = 1;".format(self.searchType, self.searchItem,
                                                                                  self.nameSearchBar.text())))
        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            for self.valor in self.tuplo:
                self.showPatientsTable.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                self.j = self.j + 1
            self.i = self.i + 1
        self.db.close()

    def show_button_Exam(self):
        """
        Executes the search for all the information for the Exam's tab

        Args:
            self (undefined):
        Vars:
            showPatientsTable: Sets the table and it's information to be shown to the user
        """
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        self.showPatientsTable.setColumnCount(5)
        self.showPatientsTable.setHorizontalHeaderLabels(("Exame",
                                                          "Data da Consulta",
                                                          "Utente",
                                                          "Data do Exame",
                                                          "Anexo"))
        self.showPatientsTable.setRowCount(self.cur.execute("SELECT * FROM exame;"))
        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            markExam = 0
            for self.valor in self.tuplo:
                markExam += 1
                if markExam == 5:
                    if self.valor != None:
                        self.showPatientsTable.setItem(self.i, self.j, QTableWidgetItem("X"))
                    else:
                        self.showPatientsTable.setItem(self.i, self.j, QTableWidgetItem(" "))
                else:
                    self.showPatientsTable.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                    self.j = self.j + 1
            self.i = self.i + 1
        self.db.close()



    def show_button_Appointment(self):
        """
        Gets the table and it's values ready to show the Appointments

        Args:
            self (undefined):
        Vars:
            showPatientsTable: Table that is being set up

        """
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        self.showPatientsTable.setColumnCount(8)
        self.showPatientsTable.setHorizontalHeaderLabels("Data",
                                                          "Utente",
                                                          "Relatório",
                                                          "Médico",
                                                          "Aviso",
                                                          "Hora",
                                                          "Administração",
                                                          "Prescrição")

        self.showPatientsTable.setRowCount(self.cur.execute("SELECT * FROM consulta;"))
        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            convertHours = 0
            for self.valor in self.tuplo:
                convertHours += 1
                if convertHours == 6:
                    hours = (int(self.valor)/60)
                    hours = int(hours)
                    minutes = (int(self.valor) % 60)
                    self.showPatientsTable.setItem(self.i, self.j, QTableWidgetItem("%02d:%02d" % (hours, minutes)))
                else:
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
        self.change_table_atributes()
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
            self.change_table_atributes()
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
        except AttributeError:                                                                      # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while adding a new patient: %s" % exception)                   # prints the exception
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

    # Employee

    def add_employee(self):
        """
        Creates a employee from a specific type. The type is chosen by a combo box

        Args:
            self (undefined):
        Vars:
            cipher: Instance of the class crypto
            employee_*: Information from the employee that will be created
            addEmployee*: Text boxes to be written by the user


        """
        try:
            self.change_table_atributes()
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            cipher = crypto.passwordHandling()                                                     # Hash creator for passwords
            employee_profession = self.addEmployeeTipo.currentText()
            employee_utilizador = self.addEmployeeNameUtilizador.text()
            employee_pass_key = cipher.hashing(self.addEmployeePass.text(), 0)
            if (self.addEmployeePass.text() != self.addEmployeeRepPass.text()):
                raise Exception("Passwords do not match!")
            employee_name = self.addEmployeeName.text()
            employee_id_nr = self.addEmployeeIDNr.text()
            employee_social_nr = self.addEmployeeSocialNr.text()
            employee_nif = self.addEmployeeNIF.text()
            employee_date = self.addEmployeeDate.text()
            employee_phone_nr = self.addEmployeePhoneNr.text()
            employee_mobile_nr = self.addEmployeeMobileNr.text()
            employee_email = self.addEmployeeEmail.text()
            employee_street = self.addEmployeeStreet.text()
            employee_home_nr = self.addEmployeeHomeNr.text()
            employee_postal = self.addEmployeePostalCode.text()
            employee_address = (employee_street + ", nº" + employee_home_nr + ", " + employee_postal)
            hashedPassword = employee_pass_key[0].decode()
            self.cur.execute('''
                INSERT INTO `funcionario` (`utilizador_nome`,
                                                      `palavra_passe`)
                VALUES (%s, %s);
            ''', (employee_utilizador,
                  hashedPassword))
            self.db.commit()
            self.cur.execute('''SELECT `numero` FROM `funcionario` where `utilizador_nome` = %s''', employee_utilizador)
            number = self.cur.fetchone()
            employee_number = number[0]
            self.cur.execute('''
                INSERT INTO `id_funcionario` (`funcionario_numero`,
                                                        `nome`,
                                                        `nr_cartao_cidadao`,
                                                        `nif`,
                                                        `nr_seguranca_social`,
                                                        `data_nascimento`,
                                                        `telefone`,
                                                        `telemovel`,
                                                        `email`,
                                                        `profissao`,
                                                        `morada`,
                                                        `ativo`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (employee_number,
                  employee_name,
                  employee_id_nr,
                  employee_nif,
                  employee_social_nr,
                  employee_date,
                  employee_phone_nr,
                  employee_mobile_nr,
                  employee_email,
                  employee_profession,
                  employee_address,
                  True))
            self.cur.execute('''
                    UPDATE funcionario SET
                            secret_key = %s
                    WHERE(numero = %s)''', (employee_pass_key[1], employee_number))
            self.db.commit()
            self.show_info("Add employee sucessfully whose nr: %s " % employee_number)
            self.db.close()
            self.addEmployeeNameUtilizador.clear()
            self.addEmployeePass.clear()
            self.addEmployeeRepPass.clear()
            self.addEmployeeName.clear()
            self.addEmployeeIDNr.clear()
            self.addEmployeeSocialNr.clear()
            self.addEmployeeNIF.clear()
            self.addEmployeeDate.clear()
            self.addEmployeePhoneNr.clear()
            self.addEmployeeMobileNr.clear()
            self.addEmployeeEmail.clear()
            self.addEmployeeStreet.clear()
            self.addEmployeeHomeNr.clear()
            self.addEmployeePostalCode.clear()
        except AttributeError:                                                                     # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while adding a new employee: %s" % exception)                 # prints the exception
            self.show_erro("An Error Occurred while adding a new employee: %s" % exception)

    def sheet_edit_employee(self):
        """
        Sets the text boxes with the information from the employee that will be edited

        Args:
            self (undefined):
        Vars:
            tabWidget*: Changes the tabs that are shown to the user
            editEmployee*: Sets the text boxes with the right information

        """
        self.change_table_atributes()
        self.tabWidget_5.setTabEnabled(2, True)
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_5.setCurrentIndex(2)
        self.editEmployeeNumber.setText(self.sheetEmployeeNumber.toPlainText())
        self.editEmployeeName.setText(self.sheetEmployeeName.toPlainText())
        self.editEmployeeIDNr.setText(self.sheetEmployeeIDNr.toPlainText())
        self.editEmployeeSocialNr.setText(self.sheetEmployeeSocialNr.toPlainText())
        self.editEmployeeNIF.setText(self.sheetEmployeeNIF.toPlainText())
        self.editEmployeeDate.setText(self.sheetEmployeeDate.toPlainText())
        self.editEmployeePhoneNr.setText(self.sheetEmployeePhoneNr.toPlainText())
        self.editEmployeeMobileNr.setText(self.sheetEmployeeMobileNr.toPlainText())
        self.editEmployeeEmail.setText(self.sheetEmployeeEmail.toPlainText())
        self.editEmployeeMorada.setText(self.sheetEmployeeAddress.toPlainText())
        self.editEmployeeJob.setText(self.sheetEmployeeJob.toPlainText())

    def edit_employee(self):
        """
        Edits the information from the Employee in the database

        Args:
            self (undefined):
        Vars:
            employee_*: New information from the employee
            editEmployee*: Sets all the text boxes to blanc
            tabWidget*: Shows the right tab to the user

        """
        try:
            self.change_table_atributes()
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            employee_name = self.editEmployeeName.text()
            employee_id_nr = self.editEmployeeIDNr.text()
            employee_social_nr = self.editEmployeeSocialNr.text()
            employee_nif = self.editEmployeeNIF.text()
            employee_date = self.editEmployeeDate.text()
            employee_phone_nr = self.editEmployeePhoneNr.text()
            employee_mobile_nr = self.editEmployeeMobileNr.text()
            employee_email = self.editEmployeeEmail.text()
            employee_address = self.editEmployeeMorada.text()
            employee_num = self.editEmployeeNumber.text()
            self.cur.execute('''
                UPDATE `id_funcionario` SET
                                                `nome` = %s,
                                                `nr_cartao_cidadao` = %s,
                                                `nif` = %s,
                                                `nr_seguranca_social` = %s,
                                                `data_nascimento` = %s,
                                                `telefone` = %s,
                                                `telemovel` = %s,
                                                `email` = %s,
                                                `morada` = %s
                WHERE(`funcionario_numero` = %s)
            ''', (employee_name,
                  employee_id_nr,
                  employee_nif,
                  employee_social_nr,
                  employee_date,
                  employee_phone_nr,
                  employee_mobile_nr,
                  employee_email,
                  employee_address,
                  employee_num))
            self.db.commit()
            self.show_info("Edit employee sucessfully whose nr: %s " % employee_num)
            self.db.close()
            self.editEmployeeName.clear()
            self.editEmployeeIDNr.clear()
            self.editEmployeeSocialNr.clear()
            self.editEmployeeNIF.clear()
            self.editEmployeeDate.clear()
            self.editEmployeePhoneNr.clear()
            self.editEmployeeMobileNr.clear()
            self.editEmployeeEmail.clear()
            self.editEmployeeMorada.clear()
            self.editEmployeeNumber.clear()
            self.editEmployeeJob.clear()
            self.tabWidget_5.setTabEnabled(2, False)
            self.tabWidget_5.setTabEnabled(0, False)
        except AttributeError:                                                                     # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while editing a new employee: %s" % exception)                # prints the exception
            self.show_erro("An Error Occurred while editing a employee whose nr, %s : \n  %s" % (employee_num, exception))

    def delete_employee(self):
        """
        Deletes the employee. It only really sets the employee as inactive in the database

        Args:
            self (undefined):
        Vars:
            editEmployee*: Clears the text boxes
            tabWidget*: Sets the right tab for the user 
        """
        try:
            self.change_table_atributes()
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            employee_num = self.editEmployeeNumber.text()
            self.cur.execute('''
                UPDATE `id_funcionario` SET
                                                `ativo` = %s
                WHERE(`funcionario_numero` = %s)
            ''', (False,
                  employee_num))
            self.db.commit()
            self.show_info("Delete employee sucessfully whose nr: %s " % employee_num)
            self.db.close()
            self.editEmployeeNumber.clear()
            self.editEmployeeName.clear()
            self.editEmployeeIDNr.clear()
            self.editEmployeeNIF.clear()
            self.editEmployeeSocialNr.clear()
            self.editEmployeeDate.clear()
            self.editEmployeePhoneNr.clear()
            self.editEmployeeMobileNr.clear()
            self.editEmployeeEmail.clear()
            self.editEmployeeMorada.clear()
            self.editEmployeeJob.clear()
            self.tabWidget_5.setTabEnabled(2, False)
            self.tabWidget_5.setTabEnabled(0, False)
        except AttributeError:                                                                     # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while delete a new employee: %s" % exception)                 # prints the exception
            self.show_erro("An Error Occurred while delete a new employee whose nr, %s :\n %s" % (employee_num, exception))

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
            self.change_table_atributes()
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
                                utilizador_nome
                            from id_funcionario inner join funcionario on funcionario_numero = numero where funcionario_numero = %s''', numero_funcionario)
            number = self.cur.fetchone()
            self.userIdentificationBox.setText(str(number[1]) + " | Nr: " + str(numero_funcionario))
            self.profileUserName.setText(number[11])
            self.profileNumber.setText(str(numero_funcionario))
            self.profileName.setText(number[1])
            self.profileIDNr.setText(str(number[2]))
            self.profileNIF.setText(str(number[3]))
            self.profileSocialNr.setText(str(number[4]))
            self.profileDate.setText(str(number[5]))
            self.profileaPhoneNr.setText(str(number[7]))
            self.profileMobileNr.setText(str(number[6]))
            self.profileEmail.setText(number[8])
            self.profileAdress.setText(number[9])
            self.profileJob.setText(number[10])
        except AttributeError:                                                                     # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while search profile: %s" % exception)                        # prints the exception
            self.show_erro("An Error Occurred while search profile: %s " % exception)

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
            self.change_table_atributes()
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
        except AttributeError:                                                                    # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while change email: %s" % exception)                         # prints the exception
            self.show_erro("An Error Occurred while change email whose nr, %s :\n %s" %(numero, exception))

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
        except AttributeError:                                                                  # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while changing password: %s" % exception)                  # prints the exception
            self.show_erro("An Error Occurred while changing password whose nr, %s :\n %s" % (numero, exception))



    # Consultas
    def visit_table_changed(self):
        """
        Shows the right window to the user

        Args:
            self (undefined):
        Vars:
            openReport*: Sets the button to enabled, so it can be pressed

        """
        self.openReport.setEnabled(True)
        self.openReport_3.setEnabled(True)

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
                    total_DayTime += 720                                                          # 12H x 60M
            except:
                pass
            self.cur.execute('''SELECT profissao FROM id_funcionario
                                            WHERE funcionario_numero
                                             = %s;''', (sch_doctor))
            funcionario = self.cur.fetchone()
            if str(funcionario[0]) == "Médico":

                app_time = app_time[0].split(':')
                total_DayTime += int(app_time[0]) * 60 + int(app_time[1])                         # H x 60 + M
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
                                `hora`)
                                VALUES (%s, %s, %s, %s, %s);
                                ''', (app_date,
                                      app_utente,
                                      sch_description,
                                      sch_doctor,
                                      total_DayTime))
                    self.db.commit()
                    self.show_info(
                    "Add appointment sucessfully whose date, %s and utente number, %s " % (app_date, app_utente))
                    app_utente = self.app_nrUtente.clear()
                    sch_doctor = self.app_dtr.clear()
                    sch_description = self.app_description.clear()

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
                print("An Error Occurred while adding a appointment: %s" % exception)             # - The employee number is wrong
                self.show_erro("An Error Occurred while adding a appointment whose date, %s and utente number, %s :\n %s " % (
                    app_date,
                    app_utente,
                    exception))

    def visit_table_update(self):
        """
        Fetches all the information for the table to be shown and set up
        Args:
            self (undefined):
        Vars:
            visitTableUtente: Gets the table

        """
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        self.visitTableUtente.setRowCount(self.cur.execute(
            "SELECT data, utente_numero, nome, medicacao_administrada, relatorio_consulta "
            "FROM consulta inner join id_funcionario on consulta.funcionario_numero = id_funcionario.funcionario_numero "
            "WHERE consulta.utente_numero = {};"
                .format(self.sheetPatientNumber.toPlainText())))
        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            for self.valor in self.tuplo:
                self.visitTableUtente.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                self.j = self.j + 1
            self.i = self.i + 1
        self.db.close()

    def open_report(self, n_utente, data_consulta):
        """
        Fetches and shows the report to the user

        Args:
            self (undefined):
            n_utente (integer): Patient's number
            data_consulta (date): Appointment's date
        Vars:
            addReport*: Clears all the information on the text boxes and then sets all the information that was fetched into the same text boxes
            medication_text: Clears all the medication text from the text box and then sets it to the information that was fetched into the same text box
            tabWidget*: Shows the correct tab to the user

        """
        self.addReportDate.clear()
        self.addReportPatientNumber.clear()
        self.medication_text.clear()
        self.addReportDescription.clear()
        self.addReportPrescription.clear()
        self.addReportWarning.clear()
        self.warning_text.clear()
        self.tabWidget_1.setTabEnabled(2, True)
        self.addReportDescription.setReadOnly(True)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_1.setCurrentIndex(2)
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        self.cur.execute(
            """SELECT data, utente_numero, medicacao_administrada, relatorio_consulta, prescricao_consulta, aviso_consulta
            FROM consulta
            WHERE utente_numero = %s and data = %s;""",
            (n_utente, data_consulta))
        self.items = self.cur.fetchone()
        self.addReportDate.setText(str(self.items[0]))
        self.addReportPatientNumber.setText(str(self.items[1]))
        self.medication_text.setText(str(self.items[2]))
        self.addReportDescription.setText(str(self.items[3]))
        self.addReportPrescription.setText(str(self.items[4]))
        self.addReportWarning.setText(str(self.items[5]))
        self.addReportDescription.setReadOnly(True)
        self.addReportPrescription.setReadOnly(True)
        self.addAppointmentReport.setEnabled(False)
        self.addReportWarning.setReadOnly(True)
        self.addExamFile.setEnabled(False)
        self.addAppointmentExam.setEnabled(False)
        self.addExameDate.setEnabled(False)
        self.cur.execute("""SELECT aviso_consulta
                                    FROM consulta
                                    where data in(select max(data) from consulta
                                    where data < %s
                                    and utente_numero = %s);"""
                         , (
                             data_consulta,
                             n_utente
                         )
                         )
        self.aviso = self.cur.fetchone()
        if self.aviso:
            self.warning_text.setText(self.aviso[0])
        self.db.close()

    def fill_prescription(self, numero_utente, data_consulta):
        """
        Shows all prescriptions to the user in a table

        Args:
            self (undefined):
            numero_utente (integer): Patient's number
            data_consulta (date): Appointment's date
        Vars:
            prescricoes: Prescriptions' information
            addReportPrescription: Set the text box equal to the var prescricoes

        """
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        self.cur.execute("""SELECT descricao
                                    FROM prescricao
                                    where consulta_utente_numero = %s
                                    and consulta_data = %s;"""
                         , (
                             numero_utente,
                             data_consulta
                         )
                         )
        self.prescricoes = ""
        for self.tuplo in self.cur.fetchall():
            self.prescricoes = self.prescricoes + "\u2022" + self.tuplo[0] + "\n"
        self.addReportPrescription.setText(self.prescricoes)
        self.db.close()

    def add_appointment_exam(self):
        """
        Adds an exam into the appointment

        Args:
            self (undefined):
        Vars:
            patient_number: Patient's Number
            consul_date: Appointment's Date
            exame_date: Exam's Date
            filename: Name for the Exam's File

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            patient_number = self.addReportPatientNumber.toPlainText()
            consul_date = self.addReportDate.toPlainText()
            exame_date = self.addExameDate.text()
            filename = self.exam_image
            with open(filename, 'rb') as file:
                binaryData = file.read()
            self.cur.execute('''
                INSERT INTO `exame` (`consulta_data`,
                                                `consulta_utente_numero`,
                                                `data_exame`,
                                                `imagem_exame`)
                VALUES (%s, %s, %s, %s);
                ''', (consul_date,
                      patient_number,
                      exame_date,
                      binaryData))
            self.db.commit()
            self.show_info(
                "Add appointment sucessfully whose date, %s and utente number, %s " % (consul_date, patient_number))
            self.db.close()
            self.addExameDate.clear()
            self.imageName.clear()

        except AttributeError:                                                                    # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            if exception.__class__.__name__ == "OperationalError":
                self.show_erro("Por favor, introduza a data do exame!")
            else:
                print("An Error Occurred while adding a new exam: %s" % exception)                    # prints the exception
                self.show_info("An Error Occurred while adding a new exam whose date, %s and utente number, %s :\n %s" % (
                consul_date, patient_number, exception))

    def add_exam_file(self):
        """
        Shows a window so a file can be selected

        Args:
            self (undefined):
        Vars:
            fname: File name

        """
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\Users', 'Image files (*.pdf *.jpg *.jpeg *.png)')
        if fname[0] != '':
            self.exam_image = fname[0]
            self.show_info("Added the exam file sucessfully")
        else:
            self.show_erro("Added the exam file unsucessfully")

    def exam_history(self):
        """
        Shows the exam history to the user

        Args:
            self (undefined):
        Vars:
            tabWidget*: Sets the right tabs for the user
            exameHistory: Fetches all information from all the Patient's exams and sets it into a table

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            self.tabWidget_7.setTabEnabled(2, True)
            self.tabWidget_7.setCurrentIndex(2)
            self.exameHistory.setRowCount(self.cur.execute(
                "SELECT consulta_data,consulta_utente_numero,data_exame FROM exame WHERE consulta_utente_numero = {};"
                .format(self.sheetPatientNumber.toPlainText())))
            exame = self.cur.fetchall()
            self.i = 0
            for self.tuplo in exame:
                self.j = 0
                for self.valor in self.tuplo:
                    self.exameHistory.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                    self.j = self.j + 1
                self.i = self.i + 1
        except AttributeError:                                                                  # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while search a exam: %s" % exception)                      # prints the exception
            self.show_erro("An Error Occurred while search a exam :\n %s" %(exception))

    def show_image(self):
        """
        Shows the image (if it is a image) or saves the file into the user's Desktop (if it is a PDF)

        Args:
            self (undefined):
        Vars:
            itens: Gets the selected items from self.exameHistory
            img: Opened image
            scene: Sets the scene that will show the image
            code: Bytes from the file
            date_today: Current Date Time
            f: File to be written

        """
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            itens = self.exameHistory.selectedItems()
            self.cur.execute('''SELECT `imagem_exame` FROM `exame`
                                where `consulta_utente_numero` = %s and `consulta_data` = %s and `data_exame` = %s
                             ''', (itens[1].text(), itens[0].text(), itens[2].text()))
            image = self.cur.fetchone()
            try:                                                                               # Covert byte to RGB image
                img = Image.open(io.BytesIO(image[0]))
                img.save('exame' + '.png', 'PNG')
                scene = QtWidgets.QGraphicsScene(self)
                pixmap = QPixmap("exame.png")
                item = QtWidgets.QGraphicsPixmapItem(pixmap)
                scene.addItem(item)
                self.graphicsExamView.setScene(scene)
            except Exception as exception:
                if exception.__class__.__name__ == 'UnidentifiedImageError':
                    code = image[0]
                    date_today = datetime.now()
                    f = open(os.path.expanduser("~/Desktop/exam_%s.pdf" % date_today.strftime("%Y-%m-%d, %H_%S")), 'wb')
                    f.write(code)
                    f.close()
                    self.show_info("Exam save in %s" %os.path.expanduser("~/Desktop/exam_%s.pdf" % date_today.strftime("%Y-%m-%d, %H_%S")))
            self.db.close()
        except AttributeError:                                                                # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while search a exam: %s" % exception)                    # prints the exception
            self.show_erro("An Error Occurred while search a exam : %s" % exception)

    def appointment_history(self):
        """
        Shows the appointment history for a specific patient

        Args:
            self (undefined):
        Vars:
            tabWidget*: Sets the right tab for the user
            openReport: Sets the report to be shown to the user

        """
        self.visit_table_update()
        self.tabWidget_7.setTabEnabled(0, True)
        self.tabWidget_7.setCurrentIndex(0)
        self.openReport.setEnabled(True)

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
          msg = QMessageBox()
          msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
          msg.setWindowTitle("Justificação Para impressão")
          msg.setText('''Serve o Presente documento como comprovativo que o utente: %s esteve presente na clínica tendo dado entrada às: %s:%02d  e tendo recebido alta às: %s:%02d no dia: %s Por ser verdade segue assinada pelo Médico: %s''' % (nomes[0], int(hora), int(minutos), int(hora_final) , int(minutos_final), dados[0].text(), dados[2].text()))
          msg.setIcon(QMessageBox.Information)
          msg.exec_()
        except IndexError:
           self.show_erro("Selecione Consulta para passar justificação!")


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
