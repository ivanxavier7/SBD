import io
import logging
import os
import sys
from datetime import date, datetime

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import classes.connection as connect
import classes.crypto as crypto
import classes.multiTool as MT

#import classes.logger as Logger

ui, _ = loadUiType('UI/nurseWindow.ui')


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
    Description of MainApp

    Attributes:
        user_id (type):
        user_name (type):

    Inheritance:
        QMainWindow:
        ui:

    Args:
        user_id (undefined):
        user_name (undefined):

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
        # self.box_messages.hide()
        # self.changeEmail.hide()
        # self.changePass.hide()
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
        self.addAppointmentReport.clicked.connect(self.add_appointment_report)
        self.patient_search_table()
        self.profileChangeEmail.clicked.connect(self.change_email)
        self.profileChangePass.clicked.connect(self.change_pass)
        self.nurseButtExamHist.clicked.connect(self.exam_history)
        self.openExame.clicked.connect(self.show_image)
        self.addAppointmentExam.clicked.connect(self.add_appointment_exam)
        self.openReport.clicked.connect(self.open_report_helper_2)
        self.searchPatientTrigger.clicked.connect(self.search_trigger)
        self.searchPatient.clicked.connect(self.search_patient)
        self.comboBox_2.currentIndexChanged.connect(self.change_table_atributes)
        self.openReport.setEnabled(False)
        self.showPatientsTable.itemSelectionChanged.connect(self.show_table_changed)
        self.visitTable.itemSelectionChanged.connect(self.visit_table_changed)
        self.sheetPatientAppointmentList.clicked.connect(self.appointment_history)
        self.openReport_2.clicked.connect(self.open_report_helper_1)
        self.tabWidget_8.setTabEnabled(0, False)
        self.tabWidget_8.setTabEnabled(1, False)
        self.tabWidget_8.setTabEnabled(2, False)
        self.tabWidget_2.setTabEnabled(2, False)
        self.tabWidget_2.setTabEnabled(1, False)
        self.searchPatient.setEnabled(False)
        self.openReport.setEnabled(False)
        self.addExamFile.clicked.connect(self.add_exam_file)
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
        logger = Logger(self.user_name, message, "erro")
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    # Patients

    # Search triggers
    def show_table_changed(self):
        """
            Makes the button clickable

            Args:
                self (undefined):
            Vars:
                searchPatient.setEnabled(True): Making the button clickable

        """
        self.searchPatient.setEnabled(True)



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
        try:
            scen = QtWidgets.QGraphicsScene(self)
            scen.clear()
            self.graphicsExamView.setScene(scen)

            self.tabWidget_2.setTabEnabled(1, True)
            self.tabWidget_8.setTabEnabled(1, True)
            self.tabWidget_8.setTabEnabled(0, False)
            self.tabWidget_8.setTabEnabled(2, False)
            self.items = self.showPatientsTable.selectedItems()
            self.tabWidget_2.setCurrentIndex(1)
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
            self.items = self.showPatientsTable.selectedItems()
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
            # self.searchPatient.setText("Selecionar Utente")
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
            # self.searchPatient.setText("Selecionar Funcionário")
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

        if str(self.comboBox_2.currentText()) == "Nome":
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
        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]  # saves the exception on the variable e
            print("An Error Occurred while adding a new patient: %s" % e)  # prints the exception
            self.show_erro("An Error Occurred while check number patiente")


    def sheet_edit_employee(self):
        """
            Sets the text boxes with the information from the employee that will be edited

            Args:
                self (undefined):
            Vars:
                tabWidget*: Changes the tabs that are shown to the user
                editEmployee*: Sets the text boxes with the right information

        """
        self.tabWidget_5.setTabEnabled(2, True)
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_5.setCurrentIndex(2)
        # Caso em que se usa toPlainText é porque são usados QTextBrowsers
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

        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while search profile: %s" % exception)  # prints the exception
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
    def visit_table_changed(self):
        """
        Shows the right window to the user

        Args:
            self (undefined):
        Vars:
            openReport*: Sets the button to enabled, so it can be pressed

        """
        self.openReport.setEnabled(True)



    def add_appointment_report(self):
        """
        Description of add_appointment_report

        Args:
            self (undefined):

        """
        self.db = connect.connection(self)
        self.cur = self.db.cursor()

        self.cur.execute("""UPDATE `consulta` SET
                            `relatorio_consulta` = %s,
                            `medicacao_administrada` = %s WHERE
                            (`data` = %s) and
                            (`utente_numero` = %s);"""
                         , (
                             self.addReportDescription.toPlainText(),
                             self.medication_text.toPlainText(),
                             self.addReportDate.text(),
                             self.addReportPatientNumber.text()
                         )
                         )

        self.db.commit()
        self.db.close()
        self.tabWidget_3.setCurrentIndex(0)
        self.visit_table_update("cliente")

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
            elif procurar_por == "funcionario":
                self.visitTableUtente.setRowCount(self.cur.execute(
                    "SELECT data,utente_numero,medicacao_administrada, relatorio_consulta FROM consulta WHERE funcionario_numero = {};"
                    .format("33")))
            # self.visitTable.setRowCount(self.cur.execute(
            #     "SELECT data,utente_numero,medicacao_administrada, relatorio_consulta FROM consulta WHERE {} = {};".format(
            #         self.tipo, self.numero)))
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
        self.warning_text.clear()
        self.tabWidget_2.setTabEnabled(2, True)
        self.addReportDescription.setReadOnly(True)
        self.medication_text.setReadOnly(True)
        self.tabWidget_2.setCurrentIndex(2)
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

        self.cur.execute("""SELECT aviso_consulta
                            FROM consulta
                            where data in(select max(data) from consulta
                            where data < %s
                            and utente_numero = %s);"""
                         , (
                             str(self.items[0]),
                             str(self.items[1])
                         )
                         )
        if str(date.today()) == str(str(self.items[0])):
            self.addReportDescription.setReadOnly(False)
            self.addReportPrescription.setReadOnly(False)
            self.addAppointmentReport.setEnabled(True)
            self.addReportWarning.setReadOnly(False)
            self.addExamFile.setEnabled(True)
            self.addAppointmentExam.setEnabled(True)
            self.addExameDate.setEnabled(True)
        else:
            self.addReportDescription.setReadOnly(True)
            self.addReportPrescription.setReadOnly(True)
            self.addAppointmentReport.setEnabled(False)
            self.addReportWarning.setReadOnly(True)
            self.addExamFile.setEnabled(False)
            self.addAppointmentExam.setEnabled(False)
            self.addExameDate.setEnabled(False)

        self.aviso = self.cur.fetchone()

        if self.aviso:
            self.warning_text.setText(self.aviso[0])

        self.db.close()
        # self.fill_prescription(n_utente, data_consulta)

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

            # Date should be passed in this format : '2020-01-01'

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

        except AttributeError:  # Error is thrown in the connection.py file
           pass
        except Exception as exception:
            print("An Error Occurred while adding a new exam: %s" % exception)  # prints the exception
            self.show_erro("An Error Occurred while adding a new exam whose date, %s and utente number, %s :\n %s" % (
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
            self.show_info("Add exam file sucessfully")
        else:
            self.show_info("Add exam file insucessfully")

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
            self.tabWidget_8.setTabEnabled(2,True)
            self.tabWidget_8.setCurrentIndex(2)

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

        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while search a exam: %s" % exception)  # prints the exception
            self.show_erro("An Error Occurred while search a exam whose date, %s and utente number, %s :\n %s" % (
            consul_date, patient_number, exception))

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

            try:
                # covert byte to RGB image
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
        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except Exception as exception:
            print("An Error Occurred while search a exam: %s" % exception)  # prints the exception
            self.show_erro("An Error Occurred while search a exam %s \n " % exception)

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
        self.tabWidget_8.setTabEnabled(0, True)
        self.tabWidget_8.setCurrentIndex(0)
