import sys
import datetime
import calendar
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore  
        

class AccountsReceivable_MonthlyView(QtWidgets.QGridLayout):
    def __init__(self, frame,customer_info):
        super().__init__()
        self.customer_name = customer_info["name"]
        self.selectedMonth = customer_info["month"]
        self.selectedYear = customer_info["year"]
        
        if self.selectedMonth == 1:
            self.beforeMonth = 12
            self.beforeYear = self.selectedYear - 1
        else:
            self.beforeMonth = self.selectedMonth - 1
            self.beforeYear = self.selectedYear
        
        
        self.frame = frame
        self.init_ui()
        

    def input_beg_balance(self, balance):
        self.lBeginning_Balance.setText("Beginning Balance: " + str(balance["balance"]))
    def input_end_balance(self, balance):
        self.lEnding_Balance.setText("Ending Balance: " + str(balance["balance"]))
    
    def input_ar_table(self, ar_results):
        for ar_row in ar_results:
            self.ar_Table.insertRow(self.ar_Table.rowCount())
            date = QtWidgets.QTableWidgetItem(ar_row["Date"])
            date.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ar_Table.setItem(self.ar_Table.rowCount()-1,0,date)
            inv_id = QtWidgets.QTableWidgetItem(str(ar_row["inv_id"]))
            inv_id.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ar_Table.setItem(self.ar_Table.rowCount()-1,1,inv_id)
            amount = QtWidgets.QTableWidgetItem(str(ar_row["amount"]))
            amount.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ar_Table.setItem(self.ar_Table.rowCount()-1,2,amount)
            
            if ar_row["date_paid"] is None:
                ar_row["date_paid"] = ""
            date_paid = QtWidgets.QTableWidgetItem(str(ar_row["date_paid"]))
            date_paid.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ar_Table.setItem(self.ar_Table.rowCount()-1,3,date_paid)
            if ar_row["pr_id"] is None:
                ar_row["pr_id"] = ""
            pr_id = QtWidgets.QTableWidgetItem(str(ar_row["pr_id"]))  
            pr_id.setFlags(QtCore.Qt.ItemIsEnabled)  
            self.ar_Table.setItem(self.ar_Table.rowCount()-1,4,pr_id)
            if ar_row["payment"] is None:
                ar_row["payment"] = ""
            payment = QtWidgets.QTableWidgetItem(str(ar_row["payment"]))
            payment.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ar_Table.setItem(self.ar_Table.rowCount()-1,5,payment)
            
            status = QtWidgets.QTableWidgetItem(str(ar_row["status"]))
            status.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ar_Table.setItem(self.ar_Table.rowCount()-1,6,status)
            
    def label_balances(self):
        self.bCustomer_name = QtWidgets.QPushButton("< "+self.customer_name)
        self.bCustomer_name.setStyleSheet(self.buttonStyle)
        self.lMonth_Year = QtWidgets.QLabel(calendar.month_name[self.selectedMonth] + " " + str(self.selectedYear))
        self.lMonth_Year.setStyleSheet(self.labelStyle)
        self.lMonth_Year.setAlignment(QtCore.Qt.AlignCenter)
        self.lBeginning_Balance = QtWidgets.QLabel("Beginning Balance:")
        self.lBeginning_Balance.setStyleSheet(self.addressStyle)
        self.lEnding_Balance = QtWidgets.QLabel("Ending Balance:")
        self.lEnding_Balance.setStyleSheet(self.addressStyle)
        
    def init_ui(self):
        self.buttonStyle = """QPushButton {
                         background:none;
                         color:inherit;
                         border:none; 
                         padding:0;
                         font: inherit;
                         font-size: 14pt; color: gray; padding: 1px;
                         }
                         QPushButton:hover{color:black;}
                        """
    
        self.labelStyle = """QLabel { font-size: 16pt; color: black; padding: 4px;}"""
        self.addressStyle = """QLabel { font-size: 14pt; color: #666666; padding: 4px;}"""
        
        self.bAdd_Payment = QtWidgets.QPushButton("Add Payment")
        self.bAdd_Payment.setStyleSheet("""QPushButton { font-size: 14pt; padding: 10px; color: #fff; background-color: #5cb85c; border-color: #4cae4c;
                                                    border-radius: 5px;
                                                    margin-top: 10px;}
                                        QPushButton:hover {background-color: #4baa4b; border-color: #409140;}""")
        
        self.bDel_Payment = QtWidgets.QPushButton("Delete Payment")
        self.bDel_Payment.setStyleSheet("""QPushButton { font-size: 14pt; padding: 10px; color: #fff; 
        background-color: #d9534f;
        border-color: #d43f3a;
                                                    border-radius: 5px;
                                                    margin-top: 10px;}
                                        QPushButton:hover {background-color: #d5443f; border-color: #d8504b;}""")
        
        
#        self.account_receivable_Box()
        self.label_balances()
        
#        self.setColumnStretch(1,1)
#        self.setColumnStretch(2,1)
#        self.setColumnStretch(3,3)
#        self.setColumnStretch(4,1)
#        self.setColumnStretch(5,1)
#        self.setRowStretch(1,9)
#        self.setRowStretch(12,1)
        
        self.ar_Table = QtWidgets.QTableWidget()
        #self.ar_Table.setRowCount(10)
        self.ar_Table.setColumnCount(7)
        self.ar_Table.setHorizontalHeaderLabels(["Date","Invoice #","Amount", "Date Paid","PR no.", "Payment", "Status"])
        self.ar_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ar_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ar_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.ar_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.ar_Table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.ar_Table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        self.ar_Table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        self.ar_Table.setStyleSheet( """QTableWidget {font-size: 12pt;} QHeaderView::section{font-size: 12pt; padding: 5px;}""")

#        self.addWidget(self.customer_groupbox, 1, 1, 1, 1)
        self.addWidget(self.bCustomer_name, 1, 1, 1, 1)
        self.addWidget(self.lMonth_Year, 1, 3, 1, 1)
        self.addWidget(self.ar_Table, 2, 1, 1, 5)
        self.addWidget(self.lBeginning_Balance, 3, 1, 1, 1)
        self.addWidget(self.lEnding_Balance, 3, 2, 1, 1)
        self.addWidget(self.bAdd_Payment, 3, 4, 1, 1)
        self.addWidget(self.bDel_Payment, 3, 5, 1, 1)
#        #self.addWidget(self.lUsername, 3, 1, 1, 1)
#        self.addWidget(self.tUsername, 3, 1, 1, 2)
#        #self.addWidget(self.lPassword, 4, 1, 1, 1)
#        self.addWidget(self.tPassword, 4, 1, 1, 2)
#        self.addWidget(self.bLogin, 8, 1, 1, 2)
        