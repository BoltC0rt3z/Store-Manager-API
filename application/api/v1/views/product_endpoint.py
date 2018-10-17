from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from ..models.product_model import Product
import json

class Products(Resource):
    """This class contain methods for product endpoints"""
    def post(self):
        """This method handles post requsts to add new products"""
        data = request.get_json()
        name = data.get('name').strip()
        price = data.get('price').strip()
        quantity = data.get('quantity').strip()
        min_quantity = data.get('min_quantity').strip()
        category = data.get('category').strip()
        
        product_obj= Product()

        response = jsonify(product_obj.create_product(name, price, quantity, min_quantity, category))
        response.status_code = 201

        return response

    def get(self):
        """This method handles get requests to fetch all products"""
        pass
