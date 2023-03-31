from budget_app.config.mysqlconnection import connectToMySQL
from flask import  flash, request
mydb ="budget_app"


class Comment:

    def __init__( self , data ):
        self.comment= data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id =data['user_id']
        self.main_bill_id =data['main_bill_id']
        self.creator =None


    @staticmethod
    def validate_post(user):
        is_valid =True
        if len(user['comment']) <1 :
            flash('Post cant be blank silly gosse  what are you thinking why on gods green earth would you post a blank post?????????')
            is_valid =False
        return is_valid



    @classmethod
    def save(cls, data):
        query ='''
        INSERT into user_bill_has_comment (comment, user_id, main_bill_id) Values(%(comment)s, %(user_id)s,%(main_bill_id)s)
        '''
        return connectToMySQL(mydb).query_db( query, data )


    @classmethod
    def get_all(cls):
        query = '''
        SELECT user_bill_has_comment.* ,users.first_name FROM user_bill_has_comment JOIN users ON users.id= user_bill_has_comment.user_id ;
        '''
        results = connectToMySQL(mydb).query_db(query)

        comments = []
        for comment in results:
            this_comment =cls(comment)
            this_comment.creator =comment['first_name']
            comments.append( this_comment)
            print(this_comment)
        return comments


    @classmethod
    def delete_comment(cls,data):
        pass
    