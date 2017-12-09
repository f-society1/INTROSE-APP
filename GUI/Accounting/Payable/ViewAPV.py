import sys
import datetime
import calendar
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

class AccountsPayable_MonthlyView(QtWidgets.QGridLayout):
    def __init__(self, frame,accountspayable_info):
        super().__init__()
        #self.customer_name = customer_info["name"]
        self.selectedMonth = accountspayable_info["month"]
        self.selectedYear = accountspayable_info["year"]
        
        if self.selectedMonth == 1:
            self.beforeMonth = 12
            self.beforeYear = self.selectedYear - 1
        else:
            self.beforeMonth = self.selectedMonth - 1
            self.beforeYear = self.selectedYear
        
        
        self.frame = frame
        self.init_ui()
        

    def input_monthly_total(self, total):
        self.lTotal.setText("Total: " + str(total["total"]))
    
    def input_ap_table(self, ap_results):
        for ap_row in ap_results:
            self.ap_Table.insertRow(self.ap_Table.rowCount())
            self.ap_Table.setItem(self.ap_Table.rowCount()-1,0,QtWidgets.QTableWidgetItem(ap_row["Date"]))
            self.ap_Table.setItem(self.ap_Table.rowCount()-1,1,QtWidgets.QTableWidgetItem(ap_row["name"]))
            self.ap_Table.setItem(self.ap_Table.rowCount()-1,2,QtWidgets.QTableWidgetItem(str(ap_row["id_apv"])))
            self.ap_Table.setItem(self.ap_Table.rowCount()-1,3,QtWidgets.QTableWidgetItem(str(ap_row["amount"])))
        
    def init_ui(self):
    
        self.labelStyle = """QLabel { font-size: 16pt; color: black; padding: 4px;}"""
        self.addressStyle = """QLabel { font-size: 14pt; color: #666666; padding: 4px;}"""
        
        self.bDetails = QtWidgets.QPushButton("Details")
        self.bDetails.setStyleSheet("""QPushButton { font-size: 14pt; padding: 10px; color: #fff; background-color: #5cb85c; border-color: #4cae4c;
                                                    border-radius: 5px;
                                                    margin-top: 10px;}
                                        QPushButton:hover {background-color: #4baa4b; border-color: #409140;}""")
        
        self.lMonth_Year = QtWidgets.QLabel(calendar.month_name[self.selectedMonth] + " " + str(self.selectedYear))
        self.lMonth_Year.setStyleSheet(self.labelStyle)
        self.lMonth_Year.setAlignment(QtCore.Qt.AlignCenter)
        
        self.lTotal = QtWidgets.QLabel("Total:")
        self.lTotal.setStyleSheet(self.addressStyle)
        
#        self.account_receivable_Box()
        #self.label_balances()
        
#        self.setRowStretch(1,9)
#        self.setRowStretch(12,1)
        
        self.ap_Table = QtWidgets.QTableWidget()
        #self.ar_Table.setRowCount(10)
        self.ap_Table.setColumnCount(4)
        self.ap_Table.setHorizontalHeaderLabels(["Date","Particulars","APV #", "Vouchers Payable"])
        self.ap_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ap_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ap_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.ap_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.ap_Table.setStyleSheet( """QTableWidget {font-size: 12pt;} QHeaderView::section{font-size: 12pt; padding: 5px;}""")

#        self.addWidget(self.customer_groupbox, 1, 1, 1, 1)
        #self.addWidget(self.lCustomer_name, 1, 1, 1, 1)
        self.addWidget(self.lMonth_Year, 1, 2, 1, 1)
        self.addWidget(self.ap_Table, 2, 1, 1, 3)
        self.addWidget(self.lTotal, 3, 3, 1, 1)
        #self.addWidget(self.lEnding_Balance, 3, 2, 1, 1)
        self.addWidget(self.bDetails, 3, 1, 1, 1)
#        #self.addWidget(self.lUsername, 3, 1, 1, 1)
#        self.addWidget(self.tUsername, 3, 1, 1, 2)
#        #self.addWidget(self.lPassword, 4, 1, 1, 1)
#        self.addWidget(self.tPassword, 4, 1, 1, 2)
#        self.addWidget(self.bLogin, 8, 1, 1, 2)