from src.database.db_dao import Database

DB = 'api_gestion'

def get_customers_db(db : Database):
    db.__connect__(DB)
    customers = db.select(table = "customers")
    db.__disconnect__()
    return customers

def get_items_by_customer_id_db(db : Database, customer_id):
    db.__connect__(DB)
    items = db.select(table="items", fields="id_item, name_item, quantity", condition="id_customer = " + str(customer_id))
    db.__disconnect__()
    return items

def call_function_db(db : Database, function_name, data):
    db.__connect__(DB)
    resp = db.call_func(function_name, data)
    db.__disconnect__()
    return resp

def exec_script(db: Database, script_path):
    db.__connect__(DB)
    resp = db.call_script(script_path)
    db.__disconnect__()
    return resp