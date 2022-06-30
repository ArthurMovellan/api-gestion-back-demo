"""
This module the implementation of the database
"""
import os
# import shutil
import psycopg2

# DB = str(os.getenv('db_name'))
# ADRESS_BDD = str(os.getenv('ADRESSBDD'))
# PASSWORD = str(os.getenv('PASSWORD'))
DB = 'api_gestion'
ADRESS_BDD = "database"
PASSWORD = "root"
REWRITE_DB = True

class Database:
    """This class represents a database.
    """
    def __init__(self):
        self.connection = None
        self.customers = 'customers'
        self.items = 'items'
        self.debug = True
        self.null = "NULL"
        # Try connection to BBD
        try:
            self.connection = psycopg2.connect(host=ADRESS_BDD, user='postgres', password=PASSWORD, port='5432')
            print('Database connected.')
        except (Exception, psycopg2.DatabaseError) as error:
            print("!!!===========!!!")
            print('Database not connected.')
            print(error)


        # If connection not empty, we test if the database have been created
        if self.connection is not None:

            self.connection.autocommit = True
            self.cur = self.connection.cursor()
            self.cur.execute("SELECT datname FROM pg_database;")
            self.list_database = self.cur.fetchall()
            self.database_name = DB

            if (self.database_name,) in self.list_database:
                print("%s Database already exist", self.database_name)
                self.__connect__(DB)
            else:
                self.cur.execute("CREATE DATABASE " + DB +";")
                print("Database created")

            # Get all the table of the database, if it's null then we execute the sql script
            # self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
            # tables = self.cur.fetchall()

            if(REWRITE_DB): # If the user wants to rewrite it
                script = open('./scripts/script.sql','r')
                self.cur.execute(script.read())
                self.connection.commit()
                print("tables created")
            else:
                print("tables already created")
            self.connection.close()


    def __connect__(self, database):
        self.connection = psycopg2.connect(host=ADRESS_BDD, database=database, user='postgres', password=PASSWORD, port='5432')
        self.cur = self.connection.cursor()

    def __disconnect__(self):
        self.cur.close()
        self.connection.close()

    def select(self, table, fields=None, inner_join=False, condition=None, fetchone=False):
        """Return a list of records that match the condition."""
        if fields:
            req = f"SELECT {fields} FROM {table}"
        else :
            req = f"SELECT * FROM {table}"
        if inner_join :
            req += f", {inner_join}"
        if condition:
            req += f" WHERE {condition}"
        self.log(req)
        self.cur.execute(req)
        return self.cur.fetchone() if fetchone else self.cur.fetchall()

    def insert(self, table, **data):
        """Insert a new record in the table."""
        keys = ", ".join(data.keys())
        values = ", ".join([f"'{x}'" if x else self.null for x in data.values()])
        req = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        self.log(req)
        self.cur.execute(req)
        self.connection.commit()

    def update(self, table, condition, **data):
        """Update existing records that match the condition."""
        values = ", ".join(
            [f"{k}='{v}'" if v else f"{k}={self.null}" for k, v in data.items()])
        req = f"UPDATE {table} SET {values} WHERE {condition}"
        self.log(req)
        self.cur.execute(req)
        self.connection.commit()

    def delete(self, table, condition):
        """Delete records that match the condition."""
        req = f"DELETE FROM {table} WHERE {condition}"
        self.log(req)
        self.cur.execute(req)
        self.connection.commit()

    def log(self, msg):
        """Debug logging."""
        if self.debug:
            print(msg)
            
    def call_func(self, function_name, data):
        if data != '{}':
            self.cur.callproc(function_name, (data,))
        else : 
            self.cur.callproc(function_name)
        return self.cur.fetchall()
    
    def call_script(self, script_path):
        script = open(script_path,'r')
        self.cur.execute(script.read())
        return self.cur.fetchall()
