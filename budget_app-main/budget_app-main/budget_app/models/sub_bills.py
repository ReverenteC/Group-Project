
from budget_app.config.mysqlconnection import connectToMySQL

from budget_app.models import users, main_bills

from flask import flash

class Sub_bills:
    db = 'budget_app'

    def __init__(self,data):
        self.id = data['id']
        self.sub_bill_name = data['sub_bill_name']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.main_bill_id = data['main_bill_id']



    @classmethod 
    def save(cls,data):
        query = 'INSERT INTO sub_bills (sub_bill_name, amount , main_bill_id) VALUES(%(sub_bill_name)s,%(amount)s, %(main_bill_id)s)'
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result
    
    @classmethod
    def update_sub_bill (cls, data):
        print('=========')
        query = "UPDATE sub_bills SET sub_bill_name = %(sub_bill_name)s, amount = %(amount)s WHERE id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(f'============{result}')
        return result

    @classmethod
    def getById(cls, data):
        query = 'SELECT * FROM sub_bills WHERE id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def delete_sub_bill(cls, data):
        query = 'DELETE FROM sub_bills WHERE sub_bills.id = %(id)s'
        results = connectToMySQL(cls.db).query_db( query, data )
        return results
    
    @staticmethod
    def validate_sub_bill_name(bill):
        is_valid = True
        if len(bill['sub_bill_name']) < 2:
            flash("Name must be at least 2 characters long.")
            is_valid = False
        if bill['amount'] < 1:
            flash("Amount must be greater than one.")
            is_valid = False
        return is_valid 
    
    @classmethod
    def allSubBills(cls):
        query = 'SELECT * FROM sub_bills'
        results = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users
    
    @classmethod
    def getById(cls, data):
        query = 'SELECT * FROM sub_bills WHERE id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        if result:
            return cls(result[0])
        return False
        


