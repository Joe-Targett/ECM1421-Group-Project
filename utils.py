import pyodbc as odbc
import os

class Database():

    def __init__(self, server = 'localhost', port = '1433', database = 'NymptonFoodHub', UID = '', PWD = ''):
        '''
        Sets up database object by initialising a connection to the database
        '''
        try:
            self.connection = odbc.connect(f"Driver={'{SQL Server}' if os.name == 'nt' else '{ODBC Driver 17 for SQL Server}'};"
                                            f"Server={server + (',' + port) if len(port) > 0 else None};"
                                            f"Database={database};"
                                            f"{('UID='+UID) if len(UID) > 0 and len(PWD) > 0 else ''};"
                                            f"{('PWD='+PWD) if len(PWD) > 0 and len(PWD) > 0 else ''};"
                                            f"{('Trusted_Connection=yes') if len(PWD) <= 0 and len(PWD) <= 0 else ''};")
        except odbc.Error as ex:
            if ex.args[0] == '01000':
                print(f'Could not find driver for SQL Server, have you got it `installed?\n\tError:\n\t{ex.args[1]}\nIf your os is unix-like you will need the ODBC driver for SQL Server')
            else:
                print(f'Could not connect to SQL Server, have you got it running?\n\tError:\n\t{ex.args[1]}')

    def execute(self, query) -> list:
        """Runs the query passed in as a parameter. Returns the results as an array. """
        cursor = self.connection.cursor()
        return cursor.execute(query).fetchall()

    def sql_insert(self, query, table) -> str:
        """ Connects to the local running database and runs the query passed in as a parameter. Returns the ID of the new record created """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor.execute('SELECT id FROM '+ table + ' WHERE id=(SELECT max(id) FROM '+ table + ');').fetchone()[0]

    def sql_update_table(self, args, table):
        """Connects to the running database and runs the update query
            Makes query
            UPDATE table SET args"""
        cursor = self.connection.cursor()
        cursor.execute('UPDATE ' + table + ' SET ' + args)
        self.connection.commit()

    def sqlStoredProcedure(self, storedProcedure, parameters):
        """ Connects to the local running database and runs the stored procedure passed in, uses the parameters given ( use () if no parameters needed ). Returns the results as an array. """
        cursor = self.connection.cursor()
        cursor.execute( storedProcedure, parameters )
        results = cursor.fetchall()
        return results

    def stringToSQLString(myString):
        """ Takes ' and turns it into '' to allow SQL to understand it, accounts for names like O'Connor """
        newString = ''
        if (type(myString) is str):
            newString = myString.replace("'", "''")
        return newString
    
    def __del__(self):
        '''Clean-up
        __del__ is not a true destructor, it will run even if the constructor (__init__) has not finished running or encountered an exception.
        '''
        try:
            #Try to create a cursor to check the connection to the database
            cursor = self.connection.cursor()
            self.connection.close()
        except odbc.ProgrammingError as e:
            pass
        except AttributeError as e:
            pass
