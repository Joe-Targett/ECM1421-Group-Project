from tkinter import DISABLED, Tk, ttk, messagebox, N, S, E, W, Frame, StringVar, Button
from utils import *
from functools import partial

class Screen(Tk):
    '''
    Application screen wrapper class
    '''

    def __init__(self):
        '''
      

        Set up window and initialise global variables
        '''
        Tk.__init__(self)
        
        #Initialise properties
        self.selectedStreet = StringVar()
        self.headerText = StringVar()
        self.selectedID = StringVar()
        self.selectedTown = StringVar()
        self.selectedFirstName = StringVar()
        self.selectedLastName = StringVar()
        self.selectedPostcode = StringVar()
        self.selectedCounty = StringVar()
        self.selectedLandline = StringVar()
        self.selectedMobile = StringVar()
        self.selectedEmail = StringVar()
        self.selectedAddInfo = StringVar()
        self.selectedDeliveryInfo = StringVar()
        self.errorMessageText = StringVar()
        self.phone3 = StringVar()
        self.email = StringVar()
        self.firstName = StringVar()
        self.lastName = StringVar()
        self.street = StringVar()
        self.town = StringVar()
        self.postcode = StringVar()
        self.county = StringVar()
        self.phoneLandline = StringVar()
        self.phoneMobile = StringVar()
        self.what3words = StringVar()
        self.additionalInfo = StringVar()
        self.deliveryInfo = StringVar()
        self.selectedOrderID = StringVar()
        self.selectedOrderDate = StringVar()
        self.selectedOrderPicked = StringVar()
        self.selectedOrderDelivered = StringVar()
        self.selectedOrderInvoiced = StringVar()
        self.selectedOrderPaid = StringVar()
        self.selectedOrderGoodsCost = StringVar()
        self.selectedOrderExtrasInfo = StringVar()
        self.selectedOrderExtrasCost = StringVar()
        self.selectedOrderDeliveryCost = StringVar()
        self.selectedOrderTotalCost = StringVar()

        #set up window
        self.minsize(500, 500)
        self.geometry('1366x768')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=7)
        self.grid_columnconfigure(1, minsize=300)
        self.content = ttk.Frame(self, name='contentFrame', padding=(5))
        self.content.grid(column=1, row=1, sticky=(N, S, E, W), pady=10)
        self.content.grid_columnconfigure(0, minsize=100)
        self.content.grid_columnconfigure(1, minsize=100)
        self.header = Frame(self, name='headerFrame', bg="light gray", height=40)
        self.header.grid(column=0, columnspan=2, row=0,sticky=(N, S, E, W))
        title = ttk.Label(self.header, name='titleLabel', textvariable=self.headerText, font=("Arial", 40), background="light gray")
        title.grid(column=0, row=0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)
        self.content.columnconfigure(1, weight=9)
        self.content.rowconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)
        self.content.rowconfigure(2, weight=1)
        self.content.rowconfigure(3, weight=1)
        self.content.rowconfigure(4, weight=1)
        self.content.rowconfigure(5, weight=1)
        self.content.rowconfigure(6, weight=1)
        self.content.rowconfigure(7, weight=1)
        self.content.rowconfigure(8, weight=1)
        self.content.rowconfigure(9, weight=1)
        self.content.rowconfigure(10, weight=1)
        self.content.rowconfigure(11, weight=1)
        self.content.rowconfigure(12, weight=1)

    def set_database(self, database):
        '''
        Allow manual override of the database.

        CAUTION - THIS SHOULD NOT BE USED AND CAN CAUSE ERRORS!
        '''
        self.database = database

    def validate_login(self, username : str, password : str) -> bool:
        '''
        
        Sends login information to the Database server and sends result of login.
        '''
        self.database = Database(UID=username.get(), PWD=password.get())
        if isinstance(self.database, Database):
            self.list_customer_screen()
            return True
        else:
            messagebox.showerror("Login Error", "Your username or password was incorrect, please try again.")
            return False

    def clear_contents(self):
        '''
        

        Clears all widgets - except self.content. frame - for new screen draw
        '''
        for i in self.winfo_children():
            if 'contentFrame' in i.winfo_name():
                for j in i.winfo_children():
                    j.destroy()
            else:
                None if 'headerFrame' in i.winfo_name() else i.destroy()

    def login_screen(self):
        '''
        

        Renders the login screen and handles the underlying logic.
        '''
        self.clear_contents()
        self.change_header('Login')
        ttk.Label(self.content, text="User Name").grid(row=0, column=0, sticky=(E))
        username = StringVar()
        usernameField = ttk.Entry(self.content, textvariable=username)
        usernameField.grid(row=0, column=1, sticky=(N, S, E, W), pady=10)  

        # Password label and entry field
        ttk.Label(self.content,text="Password").grid(row=1, column=0, sticky=(E))  
        password = StringVar()
        passwordField = ttk.Entry(self.content, textvariable=password, show='*')
        passwordField.grid(row=1, column=1, sticky=(N, S, E, W), pady=10)  

        validateLogin = partial(self.validate_login, username, password)
        loginButton = Button(self.content, text="Login", command=validateLogin)
        loginButton.grid(row=4, column=0, sticky=(E))
        cancelButton = Button(self.content, text="Cancel", command=exit)
        cancelButton.grid(row=4, column=1, sticky=(W))
        if len(self.header.winfo_children()) > 1:
            for i in self.header.winfo_children():
                None if 'titleLabel' in i.winfo_name() else i.destroy()

    def add_customers(self):
        '''Gets the customers from the database and creates tkinter table'''

        customers = self.database.execute("SELECT cont.id,cont.firstname,cont.lastname,cont.street,cont.town,cont.postcode,cont.county,cont.phonelandline,cont.phonemobile,cont.email,cust.addliinfo,cust.deliveryinfo FROM Customer as cust INNER JOIN Contact as cont ON cust.contactid = cont.id")
        for item in self.customerTable.get_children():
            self.customerTable.delete(item)
        for customer in customers:
            self.customerTable.insert('', 'end',values=(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6],
                                 customer[7], customer[8], customer[9], customer[10], customer[11]))

    def add_order_details(self):
        '''Gets the customers from the database and creates tkinter table'''
        orders = self.database.execute(f"SELECT ord.itemqty,ord.itemname,ord.itemunit,ord.itemprice,ord.itemcost FROM SalesOrderLine as ord WHERE ord.orderid = {self.selectedOrderID.get()}")
        for item in self.orderDetailsTable.get_children():
            self.orderDetailsTable.delete(item)
        for order in orders:
            self.orderDetailsTable.insert('', 'end',values=(order[0], order[1], order[2], order[3], order[4]))

    def add_orders(self):
        '''Gets the customers from the database and creates tkinter table'''
        orders = self.database.execute(f"SELECT ord.id,ord.customerid,ord.orderdate,ord.goodscost,ord.totalcost FROM SalesOrder as ord WHERE ord.customerid = {self.selectedID.get()} AND ord.complete = 'N'")
        for item in self.orderTable.get_children():
            self.orderTable.delete(item)
        for order in orders:
            self.orderTable.insert('', 'end',values=(order[0], order[1], order[2], order[3], order[4]))


    def get_customer_id(self, contactID):
        '''Gets the ID for a customer'''

        customers = self.database.execute(f"SELECT id FROM customer WHERE contactid = {str(contactID)}")
        customerID = str(customers[0][0])
        return customerID

    def customer_selected(self, event):
        '''Gets the selected customer values from tree view and assigns values to associated text boxes'''
        selectedCustomer = self.customerTable.selection()
        for line in selectedCustomer:
            values = self.customerTable.item(line)['values']
            self.selectedID.set(values[0])
            self.selectedFirstName.set(values[1])
            self.selectedLastName.set(values[2])
            self.selectedStreet.set(values[3])
            self.selectedTown.set(values[4])
            self.selectedPostcode.set(values[5])
            self.selectedCounty.set(values[6])
            self.selectedMobile.set(str(values[7]))
            self.selectedLandline.set(values[8])
            self.selectedEmail.set(values[9])
            self.selectedAddInfo.set(values[10])
            self.selectedDeliveryInfo.set(values[11])

    def _update_contact_table(self, contactID, firstName, lastName, street, town, postcode, county, mobile, landline, email):
        '''Updates contact table in NymptonFoodHub database'''
        self.database.sql_update_table(f"firstname = '{firstName}', lastname = '{lastName}', street = '{street}', town = '{town}', postcode = '{postcode}', county = '{county}', phonelandline = '{landline}', phonemobile = '{mobile}', email = '{email}' WHERE id = {contactID}", 'Contact')
        self.add_customers()

    def _update_customer_table(self, customerID, additionalInfo, deliveryInfo):
        '''Updates customer table in NymptonFoodHub database'''
        self.database.sql_update_table(f"addliinfo = '{additionalInfo}', deliveryinfo = '{deliveryInfo}' WHERE id = {customerID}", 'Customer')
        self.add_customers()

    def _update_database_customer(self, contactID, firstName, lastName, street, town, postcode, county, mobile, landline, email,
                               additionalInfo, deliveryInfo):
        '''Updates the database with new values'''
        customerID = self.get_customer_id(contactID)
        
        self._update_contact_table(contactID, firstName, lastName, street, town, postcode, county, mobile, landline, email)
        self._update_customer_table(customerID, additionalInfo, deliveryInfo)

    def update_customer(self):
        '''Updates the database with the user inputs'''
        self.errorMessageText.set("")
        firstName = self.selectedFirstName.get()
        if not firstName.strip():
            self.errorMessageText.set("First name cannot be empty")
            return
        contactID = self.selectedID.get()
        lastName = self.selectedLastName.get()
        street = self.selectedStreet.get()
        town = self.selectedTown.get()
        postcode = self.selectedPostcode.get()
        county = self.selectedCounty.get()
        mobile = self.selectedMobile.get()
        landline = self.selectedLandline.get()
        email = self.selectedEmail.get()
        additionalInfo = self.selectedAddInfo.get()
        deliveryInfo = self.selectedDeliveryInfo.get()
        self._update_database_customer(contactID, firstName, lastName,
                               street, town, 
                               postcode, county,
                               mobile, landline,
                               email, additionalInfo,
                               deliveryInfo)

    def order_selected(self, event):
        '''
        Add selected order ID to the application
        '''
        selectedOrder = self.orderTable.selection()
        for line in selectedOrder:
            values = self.orderTable.item(line)['values']
            self.selectedOrderID.set(values[0])

    def get_order_details(self):
        '''
        Get details of order that has been selected
        '''
        self.orderDetails = self.database.execute(f"SELECT ord.id,ord.orderdate,ord.picked,ord.delivered,ord.invoiced,ord.paid,ord.goodscost,ord.extrasinfo,ord.extrascost,ord.deliverycost,ord.totalcost FROM SalesOrder as ord WHERE ord.id = {self.selectedOrderID.get()}")[0]
        self.selectedOrderDate.set(self.orderDetails[1])
        self.selectedOrderPicked.set(self.orderDetails[2])
        self.selectedOrderDelivered.set(self.orderDetails[3])
        self.selectedOrderInvoiced.set(self.orderDetails[4])
        self.selectedOrderPaid.set(self.orderDetails[5])
        self.selectedOrderGoodsCost.set(self.orderDetails[6])
        self.selectedOrderExtrasInfo.set(self.orderDetails[7])
        self.selectedOrderExtrasCost.set(self.orderDetails[8])
        self.selectedOrderDeliveryCost.set(self.orderDetails[9])
        self.selectedOrderTotalCost.set(self.orderDetails[10])

        
    
    def build_order_table(self):
        '''
        Builds the table into the window
        '''
        self.tableFrame = Frame(self, borderwidth=5, relief="ridge", width = 200, height=200)
        self.tableFrame.grid(column=0, row=1, sticky=(N, S), pady=10)
        self.orderTable = ttk.Treeview(self.tableFrame, columns=("id", "customerid", "orderdate", "goodscost", "totalcost"),
                                 show="headings", selectmode="browse")
        self.orderTable.heading('id', text='ID')
        self.orderTable.column('id', minwidth=100, width=100)
        self.orderTable.heading('totalcost', text='Total £')
        self.orderTable.column('totalcost', minwidth=200, width=200)
        self.orderTable.heading('customerid', text='Customer ID')
        self.orderTable.column('customerid', minwidth=200, width=200)
        self.orderTable.heading('orderdate', text='Order Date')
        self.orderTable.column('orderdate', minwidth=200, width=200)
        self.orderTable.heading('goodscost', text='Goods £')
        self.orderTable.column('goodscost', minwidth=200, width=200)

        self.orderTable.grid(column = 0, row=0, sticky=(N, S))

        ytreescroll = ttk.Scrollbar(self.tableFrame, orient = "vertical", command = self.orderTable.yview)
        self.tableFrame.grid_columnconfigure(1, minsize=15)
        ytreescroll.grid(column=1, row=0, sticky=(N,S,E,W))
        
        xtreescroll = ttk.Scrollbar(self.tableFrame, orient = "horizontal", command = self.orderTable.xview)
        xtreescroll.grid(row = 1, column = 0, sticky = "ew")

        self.orderTable.configure(yscrollcommand = ytreescroll.set, xscrollcommand = xtreescroll.set)

        self.add_orders()

        self.orderTable.bind('<<TreeviewSelect>>', self.order_selected)

        self.tableFrame.rowconfigure(0, weight=9)
        self.tableFrame.rowconfigure(1, weight=1)
        self.tableFrame.columnconfigure(0, weight=9)
        self.tableFrame.columnconfigure(1, weight=1)

    def build_order_details_table(self):
        '''
        Builds the table into the window
        '''
        self.tableFrame = Frame(self, borderwidth=5, relief="ridge", width = 200, height=200)
        self.tableFrame.grid(column=0, row=1, sticky=(N, S), pady=10)
        self.orderDetailsTable = ttk.Treeview(self.tableFrame, columns=("qty", "item", "unit", "price", "cost"),
                                 show="headings", selectmode="browse")
        self.orderDetailsTable.heading('qty', text='Quantity')
        self.orderDetailsTable.column('qty', minwidth=100, width=100)
        self.orderDetailsTable.heading('item', text='Item')
        self.orderDetailsTable.column('item', minwidth=200, width=200)
        self.orderDetailsTable.heading('unit', text='Unit')
        self.orderDetailsTable.column('unit', minwidth=200, width=200)
        self.orderDetailsTable.heading('price', text='Price')
        self.orderDetailsTable.column('price', minwidth=200, width=200)
        self.orderDetailsTable.heading('cost', text='Cost')
        self.orderDetailsTable.column('cost', minwidth=200, width=200)

        self.orderDetailsTable.grid(column = 0, row=0, sticky=(N, S))

        ytreescroll = ttk.Scrollbar(self.tableFrame, orient = "vertical", command = self.orderDetailsTable.yview)
        self.tableFrame.grid_columnconfigure(1, minsize=15)
        ytreescroll.grid(column=1, row=0, sticky=(N,S,E,W))
        
        xtreescroll = ttk.Scrollbar(self.tableFrame, orient = "horizontal", command = self.orderDetailsTable.xview)
        xtreescroll.grid(row = 1, column = 0, sticky = "ew")

        self.orderDetailsTable.configure(yscrollcommand = ytreescroll.set, xscrollcommand = xtreescroll.set)

        self.add_order_details()

        self.tableFrame.rowconfigure(0, weight=9)
        self.tableFrame.rowconfigure(1, weight=1)
        self.tableFrame.columnconfigure(0, weight=9)
        self.tableFrame.columnconfigure(1, weight=1)
        

    def build_customer_table(self):
        '''
        Builds the table into the window
        '''
        self.tableFrame = Frame(self, borderwidth=5, relief="ridge", width = 200, height=200)
        self.tableFrame.grid(column=0, row=1, sticky=(N, S), pady=10)
        self.customerTable = ttk.Treeview(self.tableFrame, 
                                 columns=("id", "firstname", "lastname", "street", "town", "postcode", "county", "landline", "mobile", "email", "addInfo", "deliveryInfo"),
                                 show="headings", selectmode="browse")
    
        self.customerTable.heading('id', text="Id")
        self.customerTable.column('id', minwidth=20, width=50)
        
        self.customerTable.heading('firstname', text="First Name")
        self.customerTable.column('firstname', minwidth=100, width=100)
        
        self.customerTable.heading('lastname', text="Last Name")
        self.customerTable.column('lastname', minwidth=100, width=100)
        
        self.customerTable.heading('street', text="Street")
        self.customerTable.column('street', minwidth=100, width=150)
        
        self.customerTable.heading('town', text="Town")
        self.customerTable.column('town', minwidth=100, width=150)
        
        self.customerTable.heading('postcode', text="Postcode")
        self.customerTable.column('postcode', minwidth=100, width=100)
        
        self.customerTable.heading('county', text="County")
        self.customerTable.column('county', minwidth=100, width=100)
        
        self.customerTable.heading('landline', text="Landline")
        self.customerTable.column('landline', minwidth=100, width=100)
        
        self.customerTable.heading('mobile', text="Mobile")
        self.customerTable.column('mobile', minwidth=100, width=100)
        
        self.customerTable.heading('email', text="Email")
        self.customerTable.column('email', minwidth=100)
        
        self.customerTable.heading('addInfo', text="Additional Info")
        self.customerTable.column('addInfo', minwidth=100)
        
        self.customerTable.heading('deliveryInfo', text="Delivery Info")
        self.customerTable.column('deliveryInfo', minwidth=100)
        
        self.customerTable.grid(column = 0, row=0, sticky=(N, S))

        ytreescroll = ttk.Scrollbar(self.tableFrame, orient = "vertical", command = self.customerTable.yview)
        self.tableFrame.grid_columnconfigure(1, minsize=15)
        ytreescroll.grid(column=1, row=0, sticky=(N,S,E,W))
        
        xtreescroll = ttk.Scrollbar(self.tableFrame, orient = "horizontal", command = self.customerTable.xview)
        xtreescroll.grid(row = 1, column = 0, sticky = "ew")

        self.customerTable.configure(yscrollcommand = ytreescroll.set, xscrollcommand = xtreescroll.set)

        self.add_customers()

        self.customerTable.bind('<<TreeviewSelect>>', self.customer_selected)

        self.tableFrame.rowconfigure(0, weight=9)
        self.tableFrame.rowconfigure(1, weight=1)
        self.tableFrame.columnconfigure(0, weight=9)
        self.tableFrame.columnconfigure(1, weight=1)

    def addPermission(self):
        """ Checks if the current user has permission to add a new user """
        username = "'PAUser'"
        query = ("SELECT DP1.Name\
        FROM sys.database_role_members AS DRM\
        RIGHT OUTER JOIN sys.database_principals AS DP1\
        ON DRM.role_principal_id = DP1.principal_id\
        LEFT OUTER JOIN sys.database_principals AS DP2\
        ON DRM.member_principal_id = DP2.principal_id\
        WHERE DP2.Name = " + username + "")
        results = self.database.execute(query)
        count = 0
        for row in results:
            if (row[count] == 'Manager' or row[count] == 'TeamLeader'):
                return True
            count += 1
        return False

    def add_customer(self, *args):
        """ Adds a customer to the database using the data inputted """
        if self.addPermission() :
            if not len(args) < 13:
                for i in args:
                    if not isinstance(i, StringVar):
                        messagebox.showerror("Add Customer Error", "Sorry, something went wrong when trying to add a new customer.")
                        return None
                self.database.sql_insert(f"INSERT INTO Contact (firstName, lastName, street, town, postcode, county, phoneLandline, phoneMobile, phone3, email, what3words) VALUES ('{self.database.stringToSQLString(self.firstName.get())}', '{self.database.stringToSQLString(self.lastName.get())}', '{self.database.stringToSQLString(self.street.get())}', '{self.database.stringToSQLString(self.town.get())}', '{self.database.stringToSQLString(self.postcode.get())}', '{self.database.stringToSQLString(self.county.get())}', '{self.database.stringToSQLString(self.phoneLandline.get())}', '{self.database.stringToSQLString(self.phoneMobile.get())}', '{self.database.stringToSQLString(self.phone3.get())}', '{self.database.stringToSQLString(self.email.get())}', '{self.database.stringToSQLString(self.what3words.get())}')", 'Contact')
        else:
            messagebox.showerror("Permission Error", "Sorry, you don't have permission to add a new customer.")

    def order_details_screen(self):
        '''
      

        Renders Order Details Screen
        '''
        self.clear_contents()
        self.change_header(f'Order Details - {self.selectedOrderID.get()}')

        self.get_order_details()

        ttk.Label(self.content, text="ID", borderwidth=2, relief="groove").grid(row=0, column=0)
        ttk.Label(self.content, text="Date", borderwidth=2, relief="groove").grid(row=1, column=0)
        ttk.Label(self.content, text="Picked", borderwidth=2, relief="groove").grid(row=2, column=0)
        ttk.Label(self.content, text="Delivered", borderwidth=2, relief="groove").grid(row=3, column=0)
        ttk.Label(self.content, text="Invoiced", borderwidth=2, relief="groove").grid(row=4, column=0)
        ttk.Label(self.content, text="Paid", borderwidth=2, relief="groove").grid(row=5, column=0)
        ttk.Label(self.content, text="Goods £", borderwidth=2, relief="groove").grid(row=6, column=0)
        ttk.Label(self.content, text="Extras Info", borderwidth=2, relief="groove").grid(row=7, column=0)
        ttk.Label(self.content, text="Extras Cost", borderwidth=2, relief="groove").grid(row=8, column=0)
        ttk.Label(self.content, text="Delivery £", borderwidth=2, relief="groove").grid(row=9, column=0)
        ttk.Label(self.content, text="Total £", borderwidth=2, relief="groove").grid(row=10, column=0)
        idEntry = ttk.Entry(self.content, text=self.selectedOrderID, state=DISABLED)
        idEntry.grid(row=0, column=1)
        dateEntry = ttk.Entry(self.content, text=str(self.selectedOrderDate), state=DISABLED)
        dateEntry.grid(row=1, column=1)
        ttk.Entry(self.content, text=self.selectedOrderPicked, state=DISABLED).grid(row=2, column=1)
        ttk.Entry(self.content, text=self.selectedOrderDelivered, state=DISABLED).grid(row=3, column=1)
        ttk.Entry(self.content, text=self.selectedOrderInvoiced, state=DISABLED).grid(row=4, column=1)
        ttk.Entry(self.content, text=self.selectedOrderPaid, state=DISABLED).grid(row=5, column=1)
        ttk.Entry(self.content, text=self.selectedOrderGoodsCost, state=DISABLED).grid(row=6, column=1)
        ttk.Entry(self.content, text=self.selectedOrderExtrasInfo, state=DISABLED).grid(row=7, column=1)
        ttk.Entry(self.content, text=self.selectedOrderExtrasCost, state=DISABLED).grid(row=8, column=1)
        ttk.Entry(self.content, text=self.selectedOrderDeliveryCost, state=DISABLED).grid(row=9, column=1)
        ttk.Entry(self.content, text=self.selectedOrderTotalCost, state=DISABLED).grid(row=10, column=1)

        backButton = ttk.Button(self.content, text="Back", command=self.list_order_screen)
        backButton.grid(column="2", row="12", sticky=(W))
        self.build_order_details_table()

    def add_customer_screen(self):
        '''
        Renders Screen to add a customer
        '''
        self.clear_contents()
        self.change_header('Add Customer')
        firstNameLabel = ttk.Label(self.content, text="First Name").grid(row=0, column=0)
        firstNameField = ttk.Entry(self.content, textvariable=self.firstName).grid(row=0, column=1)  

        # Last Name label and entry field
        lastNameLabel = ttk.Label(self.content,text="Last Name").grid(row=1, column=0)  
        lastNameField = ttk.Entry(self.content, textvariable=self.lastName).grid(row=1, column=1)  

        # Street label and entry field
        streetLabel = ttk.Label(self.content,text="Street").grid(row=2, column=0)  
        streetField = ttk.Entry(self.content, textvariable=self.street).grid(row=2, column=1)  

        # Town label and entry field
        townLabel = ttk.Label(self.content,text="Town").grid(row=3, column=0)  
        townField = ttk.Entry(self.content, textvariable=self.town).grid(row=3, column=1)  

        # Postcode label and entry field
        postcodeLabel = ttk.Label(self.content,text="Postcode").grid(row=4, column=0)  
        postcodeField = ttk.Entry(self.content, textvariable=self.postcode).grid(row=4, column=1)  

        # County label and entry field
        countyLabel = ttk.Label(self.content,text="County").grid(row=5, column=0)  
        countyField = ttk.Entry(self.content, textvariable=self.county).grid(row=5, column=1)  

        # Phone - Landline label and entry field
        phoneLandlineLabel = ttk.Label(self.content,text="Phone - Landline").grid(row=6, column=0)  
        phoneLandlineField = ttk.Entry(self.content, textvariable=self.phoneLandline).grid(row=6, column=1)  

        # Phone - Mobile label and entry field
        phoneMobileLabel = ttk.Label(self.content,text="Phone - Mobile").grid(row=7, column=0)  
        phoneMobileField = ttk.Entry(self.content, textvariable=self.phoneMobile).grid(row=7, column=1)

        # Phone3 label and entry field
        phone3Label = ttk.Label(self.content,text="Phone Three").grid(row=8, column=0)  
        phone3Field = ttk.Entry(self.content, textvariable=self.phone3).grid(row=8, column=1)  

        # Email label and entry field
        emailLabel = ttk.Label(self.content,text="Email").grid(row=9, column=0)  
        emailField = ttk.Entry(self.content, textvariable=self.email).grid(row=9, column=1)  

        # what3words label and entry field
        what3wordsLabel = ttk.Label(self.content,text="what3words").grid(row=10, column=0)  
        what3wordsField = ttk.Entry(self.content, textvariable=self.what3words).grid(row=10, column=1)  

        # Additional Info label and entry field
        additionalInfoLabel = ttk.Label(self.content,text="Additional Info").grid(row=11, column=0)  
        additionalInfoField = ttk.Entry(self.content, textvariable=self.additionalInfo).grid(row=11, column=1)  

        # Delivery Info label and entry field
        deliveryInfoLabel = ttk.Label(self.content,text="Delivery Info").grid(row=12, column=0)  
        deliveryInfoField = ttk.Entry(self.content, textvariable=self.deliveryInfo).grid(row=12, column=1)  

        # Add button
        add = partial(self.add_customer,
        self.firstName, 
        self.lastName,
        self.street,
        self.town,
        self.postcode,
        self.county,
        self.phoneLandline,
        self.phoneMobile,
        self.phone3,
        self.email,
        self.what3words,
        self.additionalInfo,
        self.deliveryInfo)
        addButton = Button(self.content, text="Add", command=add).grid(row=13, column=0)  

        # Cancel button
        cancelButton = Button(self.content, text="Back", command=self.login_screen).grid(row=13, column=1)  

    def list_order_screen(self):
        '''
        @author Joe Targett

        Renders Order Screen
        '''
        self.clear_contents()
        self.change_header(f'Orders - {self.selectedFirstName.get() + " " + self.selectedLastName.get()}')
        
        detailsButton = ttk.Button(self.content, text="Details", command=self.order_details_screen)
        detailsButton.grid(column="1", row="12", sticky=(W))

        backButton = ttk.Button(self.content, text="Back", command=self.list_customer_screen)
        backButton.grid(column="2", row="12", sticky=(W))

        self.build_order_table()

    def list_customer_screen(self):
        '''
      

        Renders customer list screen
        '''
        self.clear_contents()
        self.change_header('Customer list')

        self.addCustomerButton = Button(self.header, text="Add Customer(s)", command=self.add_customer_screen)
        self.addCustomerButton.grid(row = 1, column=0)
        self.listCustomerButton = Button(self.header, text="List Customer(s)", command=self.list_customer_screen)
        self.listCustomerButton.grid(row = 1, column=1)

        firstNameLabel = ttk.Label(self.content, text="First Name")
        firstNameLabel.grid(column="0", row="0", sticky=(E))
        firstNameEntry = ttk.Entry(self.content, textvariable=self.selectedFirstName)
        firstNameEntry.grid(column="1", row="0", sticky=(N, S, E, W), pady=10)

        lastNameLabel = ttk.Label(self.content, text="Last Name")
        lastNameLabel.grid(column="0", row="1", sticky=(E))
        lastNameEntry = ttk.Entry(self.content, textvariable=self.selectedLastName)
        lastNameEntry.grid(column="1", row="1", sticky=(N, S, E, W), pady=10)

        streetLabel = ttk.Label(self.content, text="Street")
        streetLabel.grid(column="0", row="2", sticky=(E))
        streetEntry = ttk.Entry(self.content, textvariable=self.selectedStreet)
        streetEntry.grid(column="1", row="2", sticky=(N, S, E, W), pady=10)

        townLabel = ttk.Label(self.content, text="Town")
        townLabel.grid(column="0", row="3", sticky=(E))
        townEntry = ttk.Entry(self.content, textvariable=self.selectedTown)
        townEntry.grid(column="1", row="3", sticky=(N, S, E, W), pady=10)

        postCodeLabel = ttk.Label(self.content, text="Postcode")
        postCodeLabel.grid(column="0", row="4", sticky=(E))
        postCodeEntry = ttk.Entry(self.content, textvariable=self.selectedPostcode)
        postCodeEntry.grid(column="1", row="4", sticky=(N, S, E, W), pady=10)

        countyLabel = ttk.Label(self.content, text="County")
        countyLabel.grid(column="0", row="5", sticky=(E))
        countyEntry = ttk.Entry(self.content, textvariable=self.selectedCounty)
        countyEntry.grid(column="1", row="5", sticky=(N, S, E, W), pady=10)

        landlineLabel = ttk.Label(self.content, text="Phone - Landline")
        landlineLabel.grid(column="0", row="6", sticky=(E))
        landlineEntry = ttk.Entry(self.content, textvariable=self.selectedLandline)
        landlineEntry.grid(column="1", row="6", sticky=(N, S, E, W), pady=10)
        
        moblieLabel = ttk.Label(self.content, text="Phone - Mobile")
        moblieLabel.grid(column="0", row="7", sticky=(E))
        mobileEntry = ttk.Entry(self.content, textvariable=self.selectedMobile)
        mobileEntry.grid(column="1", row="7", sticky=(N, S, E, W), pady=10)
        
        emailLabel = ttk.Label(self.content, text="Email")
        emailLabel.grid(column="0", row="8", sticky=(E))
        emailEntry = ttk.Entry(self.content, textvariable=self.selectedEmail)
        emailEntry.grid(column="1", row="8", sticky=(N, S, E, W), pady=10)
        
        addInfoLabel = ttk.Label(self.content, text="Additional Info")
        addInfoLabel.grid(column="0", row="9", sticky=(E))
        addInfoEntry = ttk.Entry(self.content, textvariable=self.selectedAddInfo)
        addInfoEntry.grid(column="1", row="9", sticky=(N, S, E, W), pady=10)
        
        deliveryInfoLabel = ttk.Label(self.content, text="Delivery Info")
        deliveryInfoLabel.grid(column="0", row="10", sticky=(E))
        deliveryInfoEntry = ttk.Entry(self.content, textvariable=self.selectedDeliveryInfo)
        deliveryInfoEntry.grid(column="1", row="10", sticky=(N, S, E, W), pady=0)
        
        errorMessageLabel = ttk.Label(self.content, textvariable=self.errorMessageText)
        errorMessageLabel.grid(column="0", row="11", columnspan="2")

        okButton = ttk.Button(self.content, text="Ok", command=self.update_customer)
        okButton.grid(column="0", row="12", sticky=(E))
        
        ordersButton = ttk.Button(self.content, text="Orders", command=self.list_order_screen)
        ordersButton.grid(column="1", row="12", sticky=(W))

        backButton = ttk.Button(self.content, text="Exit", command=self.login_screen)
        backButton.grid(column="2", row="12", sticky=(W))

        self.build_customer_table()


    def change_header(self, text : str):
        '''Change header text at top of program'''
        self.headerText.set(text)
        self.title(text)