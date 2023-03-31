
from budget_app.config.mysqlconnection import connectToMySQL

from budget_app.models import users, user_bill_has_comment,sub_bills

from flask import flash

class Main_bill:
    db = 'budget_app'

    def __init__(self,data):
        self.id = data['id']
        self.bill_type = data['bill_type']
        self.budget_main_bills_id = data['budget_main_bills_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creater = None
        self.sub_bills = []


    @classmethod 
    def save(cls,data):
        query = '''INSERT INTO main_bills (bill_type, budget_main_bills_id) 
                    VALUES(%(bill_type)s, %(budget_main_bills_id)s)'''
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result
    @classmethod 
    def get_bill_by_id(cls,data):
        query = 'SELECT * FROM main_bills WHERE main_bills.id = %(id)s'
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result
    @classmethod
    def get_all_from_id(cls,data):
        query = """SELECT *
                    FROM budget
                    LEFT JOIN users
                    ON budget.user_id = users.id
                    LEFT JOIN main_bills
                    ON main_bills.budget_main_bills_id = budget.id
                    LEFT JOIN sub_bills
                    ON sub_bills.main_bill_id = main_bills.id
                    WHERE users.id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        bill_id=[]
        for d in result:
            bill_id.append(d['main_bills.id'])##this parses through results and gets all the main_bills.id and appends to the bill_id list which is called in flask for the conditoinal
        print(f'==== {bill_id}')
        return result


    @classmethod
    def update_budget(cls,data):
        query="UPDATE main_bills SET bill_type = %(bill_type)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @staticmethod
    def validate_bill_name(bill):
        is_valid = True
        if len(bill['bill_type']) < 2:
            flash("Name must be at least 2 characters long.")
            is_valid = False
        return is_valid 
    
    @classmethod
    def get_Sub_bills(cls,data):
        query = "SELECT sub_bills.*, main_bills.* FROM sub_bills LEFT JOIN main_bills ON sub_bills.main_bill_id = main_bills.id WHERE main_bills.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return []
        print(results)
        this_main_bill = cls(results[0])
        for i in results:
            data ={
                "id" : i ['id'],
                "sub_bill_name" : i["sub_bill_name"],
                "amount" : i["amount"],
                "created_at" : i['created_at'],
                'updated_at' :i['updated_at'],
                "main_bill_id" :['main_bill_id']
            }
            sub_bill = sub_bills.Sub_bills(data)
            
            this_main_bill.sub_bills.append(sub_bill)
        return this_main_bill.sub_bills

    @classmethod
    def delete_main_bill(cls,data):
        print('about to run delete query')
        sub_bill_query = 'DELETE FROM sub_bills WHERE main_bill_id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(sub_bill_query,data)
        comment_bill = 'DELETE FROM user_bill_has_comment WHERE main_bill_id = %(id)s'
        comment_result  = connectToMySQL(cls.db).query_db(comment_bill,data)
        main_bill_query = 'DELETE FROM main_bills WHERE id = %(id)s'
        main_result  = connectToMySQL(cls.db).query_db(main_bill_query,data)
        print('ran delete')
        print(result)
        return main_result