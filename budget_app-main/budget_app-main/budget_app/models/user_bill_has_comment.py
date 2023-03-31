
from budget_app.config.mysqlconnection import connectToMySQL

from budget_app.models import users, main_bills

from flask import flash

class Bill_comment:
    db = 'budget_app'

    def __init__(self,data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creater = None

    @classmethod 
    def save(cls,data):
        query = 'INSERT INTO user_bill_has_comment (comment, main_bill_id, user_id) VALUES(%(bill_type)s,%(amount)s,, %(main_bill_id)s, %(user_id)s)'
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result

    @classmethod
    def get_comment_for_bill(cls,data):
        query = """SELECT * FROM user_bill_has_comment
                LEFT JOIN users ON user_bill_has_comment.user_id = users.id
                LEFT JOIN main_bills ON user_bill_has_comment.main_bill_id = main_bill.id
                WHERE main_bills.id = %(id)s"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
        

    @staticmethod
    def validate_comment(bill_comment):
        is_valid = True
        if bill_comment['bill_type'] == '':
            flash("Comment can not be empty")
            is_valid = False
        return is_valid 