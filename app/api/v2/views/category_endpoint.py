from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
from ..models.category_model import Categories
from ..models import db_connection
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_claims)

#passing incoming data into post requests
parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)

class Category(Resource):
    @jwt_required
    def post(self):
        """Post new category"""
        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']
        
        if name.isalpha() == False:
            return{
                'message' : 'Invalid category name'
            }
        else:
            try:
                new_category = Categories()
                sql = new_category.create_category()
                cursor.execute(sql,(name,))
                connection.commit()
                
                return {
                        'message': 'Category created successfully',
                    },201
            except:
                return {'message' : 'Category already exist'}
    @jwt_required
    def get(self):
        """Get all Categories"""

        connection = db_connection()
        cursor = connection.cursor()

        categories = Categories()
        sql = categories.get_all_category()
        cursor.execute(sql)
        data = cursor.fetchall()

        if len(data) == 0:
            return {'message' : 'No categories'}

        return {
                'message' : 'success',
                'Categories' : data
            },200

class SingleCategory(Resource):
    @jwt_required
    def get(self, category_id):
        """Get one Category"""

        connection = db_connection()
        cursor = connection.cursor()

        category = Categories()
        sql = category.get_one_category()
        cursor.execute(sql,(category_id,))
        data = cursor.fetchone()

        if data is None:
            return {'message' : 'Category not Found'}

        return {
            'message' : 'success',
            'Category' : data
        },200

    @jwt_required
    def put(self, category_id):
        """Modify one Category"""

        connection = db_connection()
        cursor = connection.cursor()

        data = parser.parse_args()
        name = data['name']

        try:
            category = Categories()
            sql = category.modify_category()
            cursor.execute(sql,(name,category_id))
            connection.commit()

            return {
                    'message': 'successfuly modified'
                },200
                
        except:
            return {'message': 'Category already exist'}

    @jwt_required
    def delete(self, category_id):
        """delete one category"""

        connection = db_connection()
        cursor = connection.cursor()

        try:
            category = Categories()
            sql = category.delete_category()
            cursor.execute(sql,(category_id,))
            connection.commit()

            return {
                  'message': 'successfuly deleted'
              },200

        except:
            return {'message' : 'Category not found'}

