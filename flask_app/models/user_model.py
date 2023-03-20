# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the user table from our database
from flask_app import DATABASE
from flask import flash, request
import re #to use regex

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #? =============REGISTER A USER===========================
    @classmethod
    def save(cls, data ):
        query = """
            INSERT INTO users ( first_name , last_name , email , password ) 
            VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s)
        """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(DATABASE).query_db( query, data )

    #?===============GET USER INFO============================
    @classmethod
    def get_user_id(cls, id):

        data = {
            'id' : id
        }

        query = f"""
            SELECT * FROM users 
            WHERE id = '{data['id']}'
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False
    
    #?=============CHECK IF EMAIL EXISTS IN DATABASE==========
    @classmethod
    def get_by_email(cls, data):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s
        """

        #!vulnerable to sql injection 
        # query =f"""
        #     SELECT * FROM users
        #     WHERE email = '{data['email']}'
        # """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        #if there is an email result, create found_user instance
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False



    # #===================VALIDATE LOGIN=======================
    @classmethod
    def validate_login(cls, data):
        
        found_user = cls.get_by_email(data)

        if not found_user:
            flash("Invalid login attempt","login")
            return False
        
        else:
            hash = found_user.password
            if hash == data['password']:
                return found_user
            else:
                flash("Invalid login attempt","login")
                return False

    #==============VAIDATE REGISTRATION FORM INPUT===========
    @staticmethod
    def validate_new_user(data):
        is_valid = True

        # if len(data['username'] < 3):
        #     flash("Username must be at least 3 characters long!")
        #     is_valid = False
        
        if len(data['first_name']) < 1:
            flash("Please provide your first name","register")
            is_valid = False
        
        if len(data['last_name']) < 2:
            flash("Please provide your last name","register")
            is_valid = False

        #check if email is in right format i.e. name@domain.com
        if not EMAIL_REGEX.match(data['email']):
            flash("Not a valid email address", "register")
            is_valid = False
        #checks if email already exists in database
        elif User.get_by_email(data):
            flash("Email already registered!", "register")
        
        if len(data['password']) < 3:
            flash("Password needs to be longer than 3 chars", "register")
            is_valid = False
        
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match!", "register")
            is_valid = False
        
        return is_valid