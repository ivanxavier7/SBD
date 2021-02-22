import sys
import pymysql
import logging
from datetime import date
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QDate, QDateTime
import classes.connection as connect
import classes.crypto as crypto
from PyQt5.QtGui import *
from PyQt5.QtCore import *

ui, _ = loadUiType('clinica.ui')

class Logger():
    log = logging.getLogger('name')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    #Save to a file
    file_handler = logging.FileHandler('loggers.log')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)


class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui_changes()
        self.box_messages.hide()
        self.changeEmail.hide()
        self.changePass.hide()


    def handle_ui_changes(self):
        self.handle_buttons()
        self.tabWidget.setCurrentIndex(0)
        self.user_profile()

    def handle_buttons(self):
        self.openSearchTab.clicked.connect(self.open_search_tab)
        self.openPatientsTab.clicked.connect(self.open_patients_tab)
        self.openEmployeesTab.clicked.connect(self.open_employees_tab)
        self.openAppointmentsTab.clicked.connect(self.open_appointments_tab)
        self.addEmployee.clicked.connect(self.add_employee)
        self.editEmployee.clicked.connect(self.edit_employee)
        self.addAppointmentReport.clicked.connect(self.add_appointment_report)
        self.addExamFile.clicked.connect(self.add_exam_file)
        self.addAppointmentExam.clicked.connect(self.add_appointment_exam)
        self.openReport.clicked.connect(self.open_report)
        self.addPatient.clicked.connect(self.add_patient)
        self.editPatient.clicked.connect(self.edit_patient)
        self.deletePatient.clicked.connect(self.delete_patient)
        self.searchPatientTrigger.clicked.connect(self.search_trigger)
        #self.searchEmployee.clicked.connect(self.search_employee)
        self.nameSearchBar.textEdited.connect(self.search_trigger)
        self.searchPatient.clicked.connect(self.search_patient)
        self.deleteEmployee.clicked.connect(self.delete_employee)
        self.confirmScheduling.clicked.connect(self.add_appointment)
        self.sheetPatientAppointment.clicked.connect(self.patient_make_appointment)
        self.comboBox_2.currentIndexChanged.connect(self.change_table_atributes)
        self.tabWidget_2.setTabEnabled(0, False)
        self.tabWidget_2.setTabEnabled(2, False)
        self.searchPatient.setEnabled(False)
        self.openReport.setEnabled(False)
        self.showPatientsTable.itemSelectionChanged.connect(self.show_table_changed)
        self.visitTable.itemSelectionChanged.connect(self.visit_table_changed)
        self.sheetPatientEdit.clicked.connect(self.search_edit_patient)
        self.sheetPatientAppointmentList.clicked.connect(self.appointment_history)
        self.openReport.clicked.connect(self.open_report)
        self.sheetEmployeeEdit.clicked.connect(self.sheet_edit_employee)
        self.sheetEmployeeAppointmentList.clicked.connect(self.appointment_history)
        self.tabWidget_4.setTabEnabled(0, False)
        self.tabWidget_4.setTabEnabled(2, False)
        self.closeBoxMessages.clicked.connect(self.close_box_messages)
        self.profileShowBoxPass.clicked.connect(self.show_box_pass)
        self.profileShowBoxEmail.clicked.connect(self.show_box_email)
        self.profileChangeEmail.clicked.connect(self.change_email)
        self.profileChangePass.clicked.connect(self.change_pass)

    # Opening tabs
    def open_search_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_patients_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_employees_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_appointments_tab(self):
        self.tabWidget.setCurrentIndex(3)

    #Pop up
    def show_info(self, message):
        Logger.log.info(message)
        self.box_messages.show()
        self.messages.setText(message)

    def show_erro(self, message):
        Logger.log.error(message)
        self.box_messages.show()
        self.messages.setText(message)

    def close_box_messages(self):
        self.box_messages.hide()

    # Patients

    #Search triggers
    def show_table_changed(self):
        self.searchPatient.setEnabled(True)

    def patient_make_appointment(self):
        self.items = self.showPatientsTable.selectedItems()
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_3.setCurrentIndex(2)
        self.app_nrUtente.setText(self.items[0].text())

    def search_patient(self):
        if self.searchPatient.text() == "Selecionar Utente":
            self.tabWidget_2.setTabEnabled(0, True)
            self.items = self.showPatientsTable.selectedItems()
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget_2.setCurrentIndex(0)
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
            self.tabWidget_4.setTabEnabled(0, True)
            self.items = self.showPatientsTable.selectedItems()
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget_4.setCurrentIndex(0)
            self.sheetEmployeeNumber.setText(self.items[0].text())
            self.sheetEmployeeName.setText(self.items[1].text())
            self.sheetEmployeeIDNr.setText(self.items[2].text())
            self.sheetEmployeeSocialNr.setText(self.items[3].text())
            self.sheetEmployeeNIF.setText(self.items[4].text())
            self.sheetEmployeeDate.setText(self.items[5].text())
            self.sheetEmployeePhoneNr.setText(self.items[6].text())
            self.sheetEmployeeMobileNr.setText(self.items[7].text())
            self.sheetEmployeeEmail.setText(self.items[8].text())
            self.sheetEmployeeAddress.setText(self.items[9].text())
            self.sheetEmployeeJob.setText(self.items[10].text())

    def change_table_atributes(self):
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
            self.searchPatient.setText("Selecionar Utente")
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
                                                              "Morada",
                                                              "Profissão"))
            self.searchPatient.setText("Selecionar Funcionário")
        self.search_trigger()


    def search_trigger(self):
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
            "SELECT * FROM {} WHERE {} LIKE '%{}%' and ativo = 1;".format(self.searchType,self.searchItem,self.nameSearchBar.text())))

        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            for self.valor in self.tuplo:
                self.showPatientsTable.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                self.j = self.j+1
            self.i = self.i+1


    def search_edit_patient(self):
        self.tabWidget_2.setTabEnabled(2, True)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(2)
        self.editPatientName.setText(self.sheetPatientName.text())
        self.editPatientNumber.setText(self.sheetPatientNumber.text())
        self.editPatientDate.setText(self.sheetPatientDate.text())
        self.editPatientAddress.setText(self.sheetPatientAddress.text())
        self.editPatientEmail.setText(self.sheetPatientEmail.text())
        self.editPatientIDNr.setText(self.sheetPatientIDNr.text())
        self.editPatientMobileNr.setText(self.sheetPatientMobileNr.text())
        self.editPatientNIF.setText(self.sheetPatientNIF.text())
        self.editPatientPhoneNr.setText(self.sheetPatientPhoneNr.text())
        self.editPatientSocialNr.setText(self.sheetPatientSocialNr.text())

    def add_patient(self):
        # Change the password
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
            print('done')
            self.show_info("Add patient sucessfully whose nr: %s " %patient_nr)
            self.db.close()

            self.tabWidget.setCurrentIndex(0)

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
        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while adding a new patient: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while adding a new patient")

    def edit_patient(self):
        # Change the password
        try:
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
            print('done')
            self.show_info("Edit patient sucessfully whose nr: %s " %self.editPatientNumber.text())
            self.db.close()
            self.search_trigger()  # prints the exception
            self.tabWidget_2.setCurrentIndex(0)
            self.tabWidget_2.setTabEnabled(2, False)
        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while edit patient: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while edit a patient whose nr, %s :\n %s" %(self.editPatientNumber.text(), e))

    def delete_patient(self):
        # Change the password
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()

            self.cur.execute('''
                UPDATE `utente` SET
                                        `ativo` = %s
                WHERE(`numero` = %s)
            ''', (False,
                  self.editPatientNumber.text()))

            self.db.commit()
            print('done')
            self.show_info("Delete patient sucessfully whose nr: %s " %self.editPatientNumber.text())
            self.db.close()
        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while deleting a patient: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while deleting a patient whose nr, %s :\n %s" %(self.editPatientNumber.text(), e))

    # Employee
    def add_employee(self):
        """
        Description of add_employee

        Args:
            self (undefined):

        """
        # Change the password
        """
        Description of add_employee

        Args:
            self (undefined):

        """
        # Change the password
        try:
            self.change_table_atributes()
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            search = self.db.cursor()
            cipher = crypto.passwordHandling()  # Hash creator for passwords
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

            print("first query")
            print(employee_pass_key[0])
            hashedPassword = employee_pass_key[0].decode()
            print(hashedPassword)
            # Date entry in the funcionario relation
            self.cur.execute('''
                INSERT INTO `funcionario` (`utilizador_nome`,
                                                      `palavra_passe`)
                VALUES (%s, %s);
            ''', (employee_utilizador,
                  hashedPassword))
            self.db.commit()
            # get the employee number
            print("second query")
            self.cur.execute('''SELECT `numero` FROM `funcionario` where `utilizador_nome` = %s''', employee_utilizador)
            number = self.cur.fetchone()

            employee_number = number[0]
            print("third query")
            # Date entry in the id_funcionario relation
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
            print("fourth query")
            self.cur.execute('''
                    UPDATE funcionario SET
                            secret_key = %s
                    WHERE(numero = %s)''', (employee_pass_key[1], employee_number))
            self.db.commit()
            print('done')
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

            print("end")
            #except AttributeError:  # Error is thrown in the connection.py file
                #pass
            #except:
            #    e = sys.exc_info()[0]  # saves the exception on the variable e
            #    print("An Error Occurred while adding a new employee: %s" % e)  # prints the exception
            #    self.show_erro("An Error Occurred while adding a new employee: %s" % e)
        except AttributeError:  # Error is thrown in the connection.py file
            pass
        except Exception:
            print("An Error Occurred while adding a new employee: %s" % Exception)  # prints the exception
            self.show_erro("An Error Occurred while adding a new employee: %s" % Exception)


    def sheet_edit_employee(self):
        self.tabWidget_4.setTabEnabled(2, True)
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_4.setCurrentIndex(2)

        self.editEmployeeNumber.setText(self.sheetEmployeeNumber.text())
        self.editEmployeeName.setText(self.sheetEmployeeName.text())
        self.editEmployeeIDNr.setText(self.sheetEmployeeIDNr.text())
        self.editEmployeeSocialNr.setText(self.sheetEmployeeSocialNr.text())
        self.editEmployeeNIF.setText(self.sheetEmployeeNIF.text())
        self.editEmployeeDate.setText(self.sheetEmployeeDate.text())
        self.editEmployeePhoneNr.setText(self.sheetEmployeePhoneNr.text())
        self.editEmployeeMobileNr.setText(self.sheetEmployeeMobileNr.text())
        self.editEmployeeEmail.setText(self.sheetEmployeeEmail.text())
        self.editEmployeeMorada.setText(self.sheetEmployeeAddress.text())
        self.editEmployeeJob.setText(self.sheetEmployeeJob.text())

    def edit_employee(self):
        try:
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

            print('done!')
            self.show_info("Edit employee sucessfully whose nr: %s " %employee_num)

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
            self.tabWidget_4.setTabEnabled(2, False)
            self.tabWidget_4.setTabEnabled(0, False)

        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while editing a new employee: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while editing a employee whose nr, %s : \n  %s" %(employee_num, e))

    def delete_employee(self):
        try:
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
            print('done')
            self.show_info("Delete employee sucessfully whose nr: %s " %employee_num)

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
            self.tabWidget_4.setTabEnabled(2, False)
        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while delete a new employee: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while delete a new employee whose nr, %s :\n %s" %(employee_num, e))

    def user_profile(self):
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            numero_funcionario = 54

            self.cur.execute('''SELECT * FROM `id_funcionario` where `funcionario_numero` = %s''', numero_funcionario)
            number = self.cur.fetchone()

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

        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while search profile: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while search profile: %s " %e)

    def show_box_email(self):
        self.changeEmail.show()

    def show_box_pass(self):
        self.changePass.show()

    def change_email(self):
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()

            email = self.profileNewEmail.text()
            numero = self.profileNumber.text()

            self.cur.execute('''
                UPDATE `id_funcionario` SET
                                                `email` = %s
                WHERE(`funcionario_numero` = %s)
            ''', (email,
                  numero))

            self.db.commit()
            print('done')
            self.show_info("Change email sucessfully whose nr: %s " %numero)

            self.db.close()

            self.profileEmail.setText(email)
            self.profileNewEmail.clear()
            self.changeEmail.hide()

        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while change email: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while change email whose nr, %s :\n %s" %(numero, e))

    def change_pass(self):
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            cipher = crypto.passwordHandling()

            numero = self.profileNumber.text()
            pass_atual = cipher.hashing(self.profileCurrentPass.text())
            pass_nova = cipher.hashing(self.profileNewPass.text())
            pass_repetida = cipher.hashing(self.profileRepPass.text())

            self.cur.execute('''SELECT `palavra_passe` FROM `funcionario` where `numero` = %s''', numero)
            password = self.cur.fetchone()
            print("%s +   :   + %s" %(pass_atual, password))

            if password == pass_atual:
                print("aqui!")
                if pass_nova == pass_repetida:
                    print("aqui!!")
                    self.cur.execute('''
                        UPDATE `funcionario` SET
                                                        `palavra_passe` = %s
                        WHERE(`funcionario_numero` = %s)
                    ''', (pass_nova,
                          numero))

                    self.db.commit()
                    print('done')
                    self.show_info("Change password sucessfully whose nr: %s " %numero)

                else:
                    self.show_erro("Enter the password again")
            else:
                self.show_erro("Password Incorrect")

            self.db.close()

            self.profileNewPass.clear()
            self.changePass.hide()

        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while change email: %s" %e)    # prints the exception
            self.show_erro("An Error Occurred while change email whose nr, %s :\n %s" %(numero, e))

    # Consultas
    def visit_table_changed(self):
        self.openReport.setEnabled(True)

    def add_appointment(self):
        #try:
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        app_date = self.calendarScheduling.selectedDate().toPyDate()
        app_hour = self.timeScheduling.time()
        app_utente = self.app_nrUtente.text()
        sch_doctor = self.app_dtr.text()
        sch_description = self.app_description.text()
        app_time = self.timeScheduling.time()
        app_time = app_time.toString(Qt.DefaultLocaleShortDate).split(" ")
        total_DayTime = 0
        try:
            if app_time[1] == 'PM':
                total_DayTime += 720    # 12H x 60M
        except:
            pass
        app_time = app_time[0].split(':')
        total_DayTime += int(app_time[0])*60 + int(app_time[1]) # H x 60 + M
        busy_Slot = self.cur.execute('''  SELECT * FROM consulta
                                    WHERE funcionario_numero
                                    LIKE %s and data = %s and hora > %s and hora < %s;''',(
                                        sch_doctor,
                                        app_date,
                                        total_DayTime - 30,
                                        total_DayTime + 30))
        if busy_Slot == 0:
            self.cur.execute('''INSERT INTO `consulta` (
                            `data`,
                            `utente_numero`,
                            `estado_paciente`,
                            `funcionario_numero`,
                            `aviso_consulta`,
                            `hora`)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            ''',(app_date,
                                app_utente,
                                sch_description,
                                sch_doctor,
                                sch_description,
                                total_DayTime))
            self.db.commit()
            print('done')
            self.show_info("Add appointment sucessfully whose date, %s and utente number, %s " %(app_date, app_utente))

        else:
            print("It is not available at this time for the appointment!")
            self.show_erro("It is not available at this time for the appointment!")
        self.db.close()
        #print(" Utente nr: %s \n Tem consulta com o médico %s \n No dia: %s \n às: %s \n Descrição: %s" % (app_utente,sch_doctor,app_date,app_hour, sch_description))
        #print("Data e hora: %s , %s "% (app_date,app_hour))
        #except:
        #    e = sys.exc_info()[0]                                              # Possible errors: - The user already has an appointment that day
        #    print("An Error Occurred while adding a appointment: %s" %e)       #                  - The employee number is wrong
        #    self.show_erro("An Error Occurred while adding a appointment whose date, %s and utente number, %s :\n %s " %(app_date, app_utente, e))

    def add_appointment_report(self):
        self.db = connect.connection(self)
        self.cur = self.db.cursor()

        self.cur.execute("""UPDATE `consulta` SET
                            `relatorio_consulta` = %s,
                            `medicacao_administrada` = %s WHERE
                            (`data` = %s) and
                            (`utente_numero` = %s);"""
            ,(
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


    def visit_table_update(self, procurar_por):
        procurar_por = "cliente"                                #situacao a alterar assim que possivel com login
        self.db = connect.connection(self)
        self.cur = self.db.cursor()
        if procurar_por == "cliente":
            self.tipo = "utente_numero"
            self.numero = self.sheetPatientNumber.text()
        elif procurar_por == "funcionario":
            self.tipo = "funcionario_numero"
            self.numero = "33"
        self.visitTable.setRowCount(self.cur.execute(
            "SELECT data,utente_numero,relatorio_consulta,medicacao_administrada FROM consulta WHERE {} LIKE '%{}%';".format(
                self.tipo, self.numero)))
        self.i = 0
        for self.tuplo in self.cur.fetchall():
            self.j = 0
            for self.valor in self.tuplo:
                self.visitTable.setItem(self.i, self.j, QTableWidgetItem(str(self.valor)))
                if self.j == 1:
                    self.numero_utente = str(self.valor)
                self.j = self.j + 1
            self.cur.execute(
                """SELECT consulta_utente_numero FROM prescricao WHERE
                 consulta_utente_numero = {} AND
                 consulta_data = "{}";"""
                    .format(self.numero_utente, self.tuplo[0]))
            self.visitTable.setItem(self.i, self.j, QTableWidgetItem(str(len(self.cur.fetchall()))))

            self.i = self.i + 1
        self.addReportDescription.setReadOnly(True)

    def open_report(self, utilizador):
        self.warning_text.clear()
        self.addReportDescription.setReadOnly(True)
        self.medication_text.setReadOnly(True)
        self.db = connect.connection(self)
        self.cur = self.db.cursor()

        self.items = self.visitTable.selectedItems()
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_3.setCurrentIndex(1)
        self.addReportDate.setText(self.items[0].text())
        self.addReportPatientNumber.setText(self.items[1].text())
        self.addReportDescription.setText(self.items[2].text())
        self.medication_text.setText(self.items[3].text())
        self.cur.execute("""SELECT aviso_consulta
                            FROM consulta
                            where data in(select max(data) from consulta
                            where data < %s
                            and utente_numero = %s);"""
                         , (
                             self.items[0].text(),
                             self.items[1].text()
                            )
                         )
        if str(date.today()) == str(self.items[0].text()):
            if utilizador == "medico":
                self.addReportDescription.setReadOnly(False)
                self.medication_text.setReadOnly(False)
                self.addReportPrescription.setReadOnly(False)
            elif utilizador == "enfermeiro":
                self.medication_text.setReadOnly(False)
        self.aviso = self.cur.fetchone()
        if self.aviso:
            self.warning_text.setText(self.aviso[0])

        self.db.close()
        self.fill_prescription(self.items[1].text(), self.items[0].text())

    def fill_prescription(self, numero_utente, data_consulta):
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
        try:
            self.db = connect.connection(self)
            self.cur = self.db.cursor()
            patient_number = self.addReportPatientNumber.text()
            consul_date = self.addReportDate.text()
            exame_date = self.addExameDate.text()
            filename = self.imageName.text()

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
            print('done')
            self.show_info("Add appointment sucessfully whose date, %s and utente number, %s " %(consul_date, patient_number))
            self.db.close()

        except AttributeError:                                              # Error is thrown in the connection.py file
            pass
        except:
            e = sys.exc_info()[0]                                           # saves the exception on the variable e
            print("An Error Occurred while adding a new exam: %s" %e)       # prints the exception
            self.show_info("An Error Occurred while adding a new exam whose date, %s and utente number, %s :\n %s" %(consul_date, patient_number, e))

    def add_exam_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\Users', 'Image files (*.pdf *.jpg *.jpeg *.png)')
        print(fname[0])
        if fname[0] != '':
            image = QImage("img.png")
            img = image.scaled(QSize(70,60))

            self.labelImage.setPixmap(QPixmap(img))
            self.imageName.setText(fname[0])

    def appointment_warnings(self):
        pass

    def appointment_history(self):
        self.visit_table_update("cliente")
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_3.setCurrentIndex(0)



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
