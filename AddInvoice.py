import sys
from PyQt5 import QtWidgets,QtCore
from AddInvoiceConfirm import *

from InvoiceView import *


class AddInvoiceView(QtWidgets.QGridLayout):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.frame.setWindowTitle("Invoice")
        self.added_products = []
        self.current_row = 0
        self.components = []

        self.init_ui()
    

    def add_products(self):
        self.add_product_to_table(self.tProduct.currentText(), self.tQuantity.value(), self.tUnit.currentText(), self.tUnitPrice.text(), self.tQuantity.value())

    def change_address_tag(self):
        self.tAdd.setText(str(self.client_list[self.tBuyer.currentIndex()][1]))
        
        
    #SETTERS
    def set_term_list(self, term_list):
        """This method sets the term list for invoice
            term_list(['str']): contains an array of strings for term
        """ 
        self.tTerms.clear()
        for i,term in enumerate(term_list):
            self.tTerms.insertItem(i,term)
    
    def set_unit_list(self, unit_list):
        """This method sets the unit list for invoice
            unit_list(['str']): contains an array of strings for units
        """ 
        self.tUnit.clear()
        for i,unit in enumerate(unit_list):
            self.tUnit.insertItem(i,unit)
            
    def confirm_submit(self):
        self.confirm_window = ConfirmWindow()
        self.confirm_window.show()
        self.confirm_window.layout.layout.bAddInvoice.clicked.connect(self.submit_invoice)
        # self.confirm_window.layout.layout.bAddInvoice.clicked.connect(self.home_invoice_tab)
        for x in range(self.tProduct_Table.rowCount()):
            self.confirm_window.layout.layout.add_to_table(x,0,self.tProduct_Table.item(x,0).text())
            self.confirm_window.layout.layout.add_to_table(x,1,self.tProduct_Table.item(x,1).text())
            self.confirm_window.layout.layout.add_to_table(x,2,self.tProduct_Table.item(x,2).text())
            self.confirm_window.layout.layout.add_to_table(x,3,self.tProduct_Table.item(x,3).text())
            self.confirm_window.layout.layout.add_to_table(x,4,self.tProduct_Table.item(x,4).text())

        self.check_info = self.get_items()

        self.confirm_window.layout.layout.checkout_info(self.total_amount,self.total_vat,self.total_taxable,self.total_profit,self.check_info)

    def set_product_list(self, product_list):
        """This method sets the product list for invoice
            product_list(['str']): contains an array of strings for products
        """ 
        self.tProduct.clear()
        for i,product in enumerate(product_list):
            self.tProduct.insertItem(i,unit)
            
    def set_buyer_list(self, buyer_list):
        """This method sets the buyer list for invoice
            buyer_list(['str']): contains an array of strings for buyers
        """ 
        self.tBuyer.clear()
        for i,buyer in enumerate(buyer_list):
            self.tBuyer.insertItem(i,buyer)
    
    def add_product_to_table(self, product_name, quantity, unit, unit_price, amount):
        """This method adds a product to the products table"""

        self.tProduct_Table.insertRow(self.tProduct_Table.rowCount())
        self.tProduct_Table.setItem(self.tProduct_Table.rowCount()-1,0,QtWidgets.QTableWidgetItem(str(quantity)))
        self.tProduct_Table.setItem(self.tProduct_Table.rowCount()-1,1,QtWidgets.QTableWidgetItem(unit))
        self.tProduct_Table.setItem(self.tProduct_Table.rowCount()-1,2,QtWidgets.QTableWidgetItem(product_name))
        self.tProduct_Table.setItem(self.tProduct_Table.rowCount()-1,3,QtWidgets.QTableWidgetItem(str(unit_price)))
        self.tProduct_Table.setItem(self.tProduct_Table.rowCount()-1,4,QtWidgets.QTableWidgetItem(str(int(unit_price) * quantity)))
        print(type(product_name))
        print(type(self.origPriceList[0]))
        print(unit_price)
        print(type(quantity))
        print(type(unit))
        
        comp = Component(product_name, self.origPriceList[0], int(unit_price), quantity, unit)
        self.components.append(comp)

        total_temp = comp.get_total()
        self.total_amount += total_temp[0]
        self.total_nonvat += total_temp[1]
        self.total_vat += total_temp[3]
        self.total_taxable += total_temp[2]
        self.total_profit += total_temp[4]

        self.lamountTotal.setText("Total amount: " + str(self.total_amount))
        self.ltaxedTotal.setText("Total taxable: "  + str(self.total_taxable))
        self.ltaxTotal.setText("Total tax: "  + str(self.total_vat))
        self.lprofitTotal.setText("Total profit: "  + str(self.total_profit))

    
    #GETTERS
    def get_items(self):
        items = {}
        #Invoice Details
        items["invoice_id"] = self.invnum
        items["date"] = self.tDate.text()
        
        #Client Details
        items["buyer"] = self.tBuyer.currentText()
        items["Address"] = self.tAdd.text()
        
        #Company Details
        items["seller"] = self.tSeller.currentText()
        items["term"] = self.tTerms.currentText()
        
        # components = []
        
        # for i in range(self.tProduct_Table.rowCount()):
        #     component = {}
        #     component["quantity"] = self.tProduct_Table.item(i,0).text()
        #     component["unit"] = self.tProduct_Table.item(i,1).text()
        #     component["product_name"] = self.tProduct_Table.item(i,2).text()
        #     component["unit_price"] = self.tProduct_Table.item(i,3).text()
        #     component["amount"] = self.tProduct_Table.item(i,4).text()
        #     components.append(component)
        
        # items["components"] = components
        
        return items
                
    def delete_entry(self):
        print(self.components)
        print(self.total)

    def submit_invoice(self):
        invo_db = InvoiceDB()
        invo_entry = Invoice(self.tBuyer.currentText(),self.tDate.text(), self.tTerms.currentText(), self.tSeller.currentText())
        print(self.check_info["buyer"])
        invo_db.add_invoice(self.check_info["buyer"], self.check_info["date"], self.check_info["term"],self.check_info["date"],self.check_info["seller"], self.components)
        # cust, issue_date, terms, ddate, seller, components
        print(invo_entry)
        self.confirm_window.close()
        invo_db.close_connection()

        
    def init_ui(self):
        #Create Widgets

        self.total_amount = 0
        self.total_nonvat = 0
        self.total_vat = 0
        self.total_taxable = 0
        self.total_profit = 0
        
        invo_db = InvoiceDB()
        components = []
        client_list = []
        seller_list = []
        self.components = []
        self.client_list = invo_db.get_client_name()
        self.seller_list = invo_db.get_seller_name()
        last_id = invo_db.get_last_id()
        invo_db.close_connection()
        self.invnum = last_id + 1
        self.termsList = ("30 days", "60 days", "90 days", "1 year")
        self.unitList = ("Tetrapack", "Sachet", "Pack", "Buy 1 Take 1")
        self.productsList = ("Yakult", "Milo", "Hotdog")
        self.origPriceList = [900, 1000, 1100]
        self.unitPriceList = [1000, 1100, 1200]
        #Quantity, Unit, Articles, Unit Price, Amount
        
        self.lInvoice_Details = QtWidgets.QLabel("INVOICE DETAILS")
        self.lInvoice_Details.setStyleSheet('QLabel {font: bold 50px; font-size: 12pt; padding: 10px;}')
        
        self.lClient_Details = QtWidgets.QLabel("CLIENT DETAILS")
        self.lClient_Details.setStyleSheet('QLabel {font: bold 50px; font-size: 12pt; padding: 10px;}')
        
        self.lCompany_Details = QtWidgets.QLabel("COMPANY DETAILS")
        self.lCompany_Details.setStyleSheet('QLabel {font: bold 50px; font-size: 12pt; padding: 10px;}')
        
        self.linvoiceNum = QtWidgets.QLabel("Invoice Number: ")
        self.linvoiceNum.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        self.tinvoiceNum = QtWidgets.QLabel(str(self.invnum))
        self.tinvoiceNum.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')			

        #Label#
        self.lBuyer = QtWidgets.QLabel("Buyer:")
        self.lBuyer.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        #TEXT INPUT#
        self.tBuyer = QtWidgets.QComboBox(self.frame)
        for x in range(len(self.client_list)):
            self.tBuyer.insertItem(x, str(self.client_list[x][0]))
        self.tBuyer.activated.connect(self.change_address_tag)
        #self.tProduct_code.
        #self.tProduct_code.resize(280, 40)

        #Label#
        self.lDate = QtWidgets.QLabel("Date: ")
        self.lDate.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        self.tDate = QtWidgets.QDateEdit(self.frame)
        self.tDate.setCalendarPopup(True)
        self.tDate.setDisplayFormat("yyyy-MM-dd")
        self.tDate.setDate(datetime.datetime.now())

		
		
        #Label#
        self.lSeller = QtWidgets.QLabel("Seller:")
        self.lSeller.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        #TEXT INPUT#
        self.tSeller = QtWidgets.QComboBox(self.frame)
        for x in range(len(self.seller_list)):
            self.tSeller.insertItem(x, self.seller_list[x])
        
		#Label#
        self.lAdd = QtWidgets.QLabel("Address:")
        self.lAdd.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')


        #TEXT INPUT#
        self.tAdd = QtWidgets.QLabel(str(self.client_list[0][1]))
		
        #Label#
        self.lTerms = QtWidgets.QLabel("Terms:")
        self.lTerms.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        #TEXT INPUT#
        self.tTerms = QtWidgets.QComboBox(self.frame)
        self.tTerms.insertItem(0, self.termsList[0])
        self.tTerms.insertItem(1, self.termsList[1])
        self.tTerms.insertItem(2, self.termsList[2])
        self.tTerms.insertItem(3, self.termsList[3])
		
		#Label#
        self.lProduct_Table = QtWidgets.QLabel("PRODUCTS")
        self.lProduct_Table.setStyleSheet('QLabel {font: bold 50px; font-size: 12pt; padding: 10px;}')		
		
		#Product Table#
        self.tProduct_Table = QtWidgets.QTableWidget()
        #self.tProduct_Table.setRowCount(5)
        self.tProduct_Table.setColumnCount(5)
        self.tProduct_Table.setHorizontalHeaderLabels(["Quantity", "Unit", "Articles", "Unit Price", "Amount"])
        self.tProduct_Table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        tablewidth = self.tProduct_Table.width() + 5
        self.tProduct_Table.setColumnWidth(0, tablewidth / 8)
        self.tProduct_Table.setColumnWidth(1, tablewidth / 8)
        self.tProduct_Table.setColumnWidth(2, tablewidth / 2)
        self.tProduct_Table.setColumnWidth(3, tablewidth / 8)		
        self.tProduct_Table.setColumnWidth(4, tablewidth / 8)
        self.tProduct_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)			

        self.Add_Product_Table = QtWidgets.QPushButton("Add Product")
        self.Add_Product_Table.setStyleSheet('QPushButton { font-size: 12pt; padding: 10px;}')
		
        #self.lnumProducts = QtWidgets.QLabel("Number of Products:")
        #self.lnumProducts.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        #TEXT INPUT#
        #self.tnumProducts = QtWidgets.QSpinBox(self.frame)
        #self.tnumProducts.setFixedWidth(100)
		
        #self.lProduct = QtWidgets.QLabel("Product:")
        #self.lProduct.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')
        
        #TEXT INPUT#
        #self.tProduct = QtWidgets.QComboBox(self.frame)

        #Label#
        #self.lQuantity = QtWidgets.QLabel("Quantity:")
        #self.lQuantity.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')
        
        #TEXT INPUT#
        #self.tQuantity = QtWidgets.QSpinBox(self.frame)
        #self.tQuantity.setFixedWidth(100)
		
        self.ltaxedTotal = QtWidgets.QLabel("Total taxable: (system generated)")
        self.ltaxedTotal.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)	
        
        self.ltaxTotal = QtWidgets.QLabel("Total tax: (system generated)")
        self.ltaxTotal.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.lamountTotal = QtWidgets.QLabel("Total amount: (system generated)")
        self.lamountTotal.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.lprofitTotal = QtWidgets.QLabel("Total profit: (system generated)")
        self.lprofitTotal.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.lAddProduct = QtWidgets.QLabel("PRODUCT DETAILS")
        self.lAddProduct.setStyleSheet('QLabel {font: bold 50px; font-size: 12pt; padding: 10px;}')
        
		#Label#
        self.lQuantity = QtWidgets.QLabel("Quantity: ")
        self.lQuantity.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        self.tQuantity = QtWidgets.QSpinBox(self.frame)
        self.tQuantity.setFixedWidth(50)		

		#Label#
        self.lUnit = QtWidgets.QLabel("Unit: ")
        self.lUnit.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        self.tUnit = QtWidgets.QComboBox(self.frame)
        self.tUnit.setFixedWidth(70)	
        self.tUnit.insertItem(0,self.unitList[0])
        self.tUnit.insertItem(1,self.unitList[1])
        self.tUnit.insertItem(2,self.unitList[2])
        self.tUnit.insertItem(3,self.unitList[3])
		
        #Label#
        self.lProduct = QtWidgets.QLabel("Product:")
        self.lProduct.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        #TEXT INPUT#
        self.tProduct = QtWidgets.QComboBox(self.frame)
        self.tProduct.setFixedWidth(200)		
        self.tProduct.insertItem(0,self.productsList[0])
        self.tProduct.insertItem(1,self.productsList[1])
        self.tProduct.insertItem(2,self.productsList[2])

        #Label#
        self.lUnitPrice = QtWidgets.QLabel("Unit Price: ")
        self.lUnitPrice.setStyleSheet('QLabel { font-size: 12pt; padding: 10px;}')

        self.tUnitPrice = QtWidgets.QLineEdit(self.frame)
        self.tUnitPrice.setFixedWidth(70)	
		

        self.tQuantity.setValue(0)
        self.bAdd = QtWidgets.QPushButton("Add")
        self.bAdd.setStyleSheet('QPushButton {color: white;background-color: #1db6d1;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 12px;min-width: 10em;padding: 4px;}')
        self.bAdd.setFixedWidth(200)
        self.bAdd.clicked.connect(self.add_products)

        
        self.bDelete = QtWidgets.QPushButton("Delete")
        self.bDelete.setStyleSheet('QPushButton {color: white;background-color: #6017a5;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 12px;min-width: 10em;padding: 4px;}')        
        self.bDelete.setFixedWidth(200)
        self.bDelete.clicked.connect(self.delete_entry)

        self.bBack = QtWidgets.QPushButton("Back")
        self.bBack.setStyleSheet('QPushButton {color: white;background-color: #d62f2f;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;}')
        self.bBack.setFixedWidth(80)
        
        self.bSubmit = QtWidgets.QPushButton("Submit")
        self.bSubmit.setStyleSheet('QPushButton {color: white;background-color: #47c468;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;}')
        self.bSubmit.setFixedWidth(200)
        self.bSubmit.clicked.connect(self.confirm_submit)


        self.setColumnStretch(7,1)
        self.setColumnStretch(1,1)
        self.setRowStretch(21,1)

        #Add Widgets
        
        self.addWidget(self.lInvoice_Details, 0, 3, 1, 1)

        self.addWidget(self.linvoiceNum, 1, 3, 1, 1)
        self.addWidget(self.tinvoiceNum, 1, 4, 1, 1)
		
        self.addWidget(self.lDate, 2, 3, 1, 1)
        self.addWidget(self.tDate, 2, 4, 1, 1)
        
        self.addWidget(self.lClient_Details, 3, 3, 1, 1)        

        self.addWidget(self.lBuyer, 4, 3, 1, 1)
        self.addWidget(self.tBuyer, 4, 4, 1, 1)
		
        self.addWidget(self.lAdd, 5, 3, 1, 1)
        self.addWidget(self.tAdd, 5, 4, 1, 1)
        
        self.addWidget(self.lCompany_Details, 3, 5, 1, 1) 
        
        self.addWidget(self.lSeller, 4, 5, 1, 1)
        self.addWidget(self.tSeller, 4, 6, 1, 1)	

        self.addWidget(self.lTerms, 5, 5, 1, 1)
        self.addWidget(self.tTerms, 5, 6, 1, 1)			
	
        self.addWidget(self.lProduct_Table, 8, 5, 1, 1)	
        self.addWidget(self.tProduct_Table, 9, 5, 5, 2)			
        
        self.addWidget(self.ltaxedTotal, 14, 6, 1, 1)

        self.addWidget(self.ltaxTotal, 15,6, 1, 1)

        self.addWidget(self.lamountTotal, 16, 6, 1, 1)

        self.addWidget(self.lprofitTotal, 17, 6, 1, 1)
        
        self.addWidget(self.lAddProduct, 8, 3, 1, 1)

        self.addWidget(self.lProduct, 9, 3, 1, 1)
        self.addWidget(self.tProduct, 9, 4, 1, 1)
		
        self.addWidget(self.lQuantity, 10, 3, 1, 1)
        self.addWidget(self.tQuantity, 10, 4, 1, 1)

        self.addWidget(self.lUnit, 11, 3, 1, 1)
        self.addWidget(self.tUnit, 11, 4, 1, 1)

        self.addWidget(self.lUnitPrice, 12, 3, 1, 1)
        self.addWidget(self.tUnitPrice, 12, 4, 1, 1)
        
        #self.addWidget(self.lProduct_Code, 1, 1, 1, 1)
        self.addWidget(self.bDelete, 13, 3, 1, 1)
        self.addWidget(self.bAdd, 13, 4, 1, 1)

        
        #self.addWidget(self.lProduct_Code, 1, 1, 1, 1)
        self.addWidget(self.bBack, 20, 3, 1, 1)
        self.addWidget(self.bSubmit, 21, 3, 1, 1)
        