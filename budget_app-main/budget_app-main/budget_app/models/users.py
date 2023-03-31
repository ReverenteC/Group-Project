
from budget_app.config.mysqlconnection import connectToMySQL

import re


from flask import flash


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'budget_app'

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friends = []



    @classmethod 
    def save(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        result = connectToMySQL(cls.db).query_db(query, data)
        test = {"user_id": result}
        query2 = 'INSERT INTO budget (user_id) VALUES(%(user_id)s)'
        connectToMySQL(cls.db).query_db(query2, test)
        print(result)
        return result
    
    @classmethod
    def show_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def get_one_by_id(cls,data):
        query = 'SELECT * FROM users WHERE users.id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_onewith_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        if result:
            return cls(result[0])
        return False


    @classmethod
    def update(cls,data):
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM users WHERE id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        return result

    @staticmethod
    def validate(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result  = connectToMySQL(User.db).query_db(query,user)
        if len(user['first_name']) < 2 :
            flash('First name can not be less than 2 characters')
            is_valid = False
        if len(user['last_name']) < 2 :
            flash('Last name can not be less than 2 characters')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be atleast 8 characters')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords do not match')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please provide a Valid email")
            is_valid = False
        if len(result) >= 1:
            flash("email already in use")
            is_valid = False
        return is_valid
        
    @staticmethod
    def validate_update_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user['email']):
            flash('Invalid email address')
            is_valid = False
        return is_valid