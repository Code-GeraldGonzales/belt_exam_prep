from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Review:
    db = "movie_critic_belt_prep"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.rating = data['rating']
        self.date_watched = data['date_watched']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        query="SELECT * FROM reviews JOIN users ON reviews.user_id=users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        reviews = []
        for row in results:
            #create the review object
            review = cls(row)
            #create associated user object
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user = User(user_data)
            review.user = user
            reviews.append(review)
        return reviews

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM reviews JOIN users ON reviews.user_id=users.id WHERE reviews.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        review = cls(row)
        user_data = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        user = User(user_data)
        review.user = user
        return review

    @classmethod
    def create(cls, data):
        query = "INSERT INTO reviews(title, rating, date_watched, content, user_id) VALUES(%(title)s, %(rating)s, %(date_watched)s, %(content)s, %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE reviews SET title=%(title)s, rating=%(rating)s, date_watched=%(date_watched)s, content=%(content)s, WHERE ID=%(id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
        
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM reviews WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data) 


    @staticmethod
    def validate_create(review):
        is_valid = True
        if len(review['title']) < 1:
            flash('Title needs to be at least 1 character', 'error')
            is_valid = False
        if len(review['rating']) < 1:
            flash('Rating must be entered', 'error')
            is_valid = False
        else:
            if int(review['rating']) < 0 or int(review['rating']) > 5:
                flash('Rating need to be between 0-5', 'error')
                is_valid = False

        return is_valid





    # @classmethod
    # def get_user_by_email(cls, data):
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     results = connectToMySQL(cls.db).query_db(query, data)
    #     #check to see if there are any results, if not, the email does exist in the database
    #     if len(results) < 1:
    #         return False
    #     row = results[0]
    #     user = cls(row)
    #     return user

    # @classmethod
    # def get_user_by_id(cls, data):
    #     query = "SELECT * FROM users WHERE id = %(id)s;"
    #     results = connectToMySQL(cls.db).query_db(query, data)
    #     #check to see if there are any results, if not, the email does exist in the database
    #     if len(results) < 1:
    #         return False
    #     row = results[0]
    #     user = cls(row)
    #     return user

    # @staticmethod
    # def validate_register(user):
    #     is_valid = True
    #     user_in_db = User.get_user_by_email(user)
    #     if user_in_db:
    #         flash('Email is already associated with another account')
    #         is_valid = False
    #     if len(user['first_name']) < 2:
    #         flash('First name must be at least 3 characters', 'error')
    #         is_valid = False
    #     if len(user['last_name']) < 2:
    #         flash('Last name must be at least 3 characters', 'error')
    #         is_valid = False
    #     if len(user['password']) < 8:
    #         flash('Password must be at least 8 characters', 'error')
    #         is_valid = False
    #     if user['password'] !=user['confirm_password']:
    #         flash('Passowrds must match')
    #         is_valid = False
    #     if not EMAIL_REGEX.match(user['email']):
    #         flash('Invalid email address!')
    #         is_valid = False
    #     #check to see if the data is ok to process, is_valid is True if data is good, False if data failed validation

    #     return is_valid

    # @staticmethod
    # def validate_login(user):
    #     is_valid = True
    #     user_in_db = User.get_user_by_email(user)
    #     if not user_in_db:
    #         flash('Email is not associated with an account')
    #         is_valid = False
    #     if not EMAIL_REGEX.match(user['email']):
    #             flash('Invalid email address!')
    #             is_valid = False
    #     if len(user['password']) < 8:
    #         flash('Password must be at least 8 characters', 'error')
    #         is_valid = False
    #     return is_valid
        