from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Gin, gin_schema, gins_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/gins', methods = ['POST'])
@token_required
def create_gin(current_user_token):
    country_of_origin = request.json['country_of_origin']
    gin_name = request.json['gin_name']
    tasting_notes = request.json['tasting_notes']
    pairs_with = request.json['pairs_with']
    user_token = current_user_token.token

    print(f'NOW TESTING: {current_user_token.token}')

    gin = Gin(country_of_origin, gin_name, tasting_notes, pairs_with, user_token = user_token )

    db.session.add(gin)
    db.session.commit()

    response = gin_schema.dump(gin)
    return jsonify(response)

@api.route('/gins', methods = ['GET'])
@token_required
def get_gin(current_user_token):
    a_user = current_user_token.token
    gins = Gin.query.filter_by(user_token = a_user).all()
    response = gins_schema.dump(gins)
    return jsonify(response)

@api.route('/gins/<id>', methods = ['GET'])
@token_required
def get_gin_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        gin = Gin.query.get(id)
        response = gin_schema.dump(gin)
        return jsonify(response)
    else:
        return jsonify({"message":"You must have a valid token."}), 401

@api.route('/gins/<id>', methods = ['POST','PUT'])
@token_required
def update_gin(current_user_token,id):
    gin = Gin.query.get(id) 
    gin.country_of_origin = request.json['country_of_origin']
    gin.gin_name = request.json['gin_name']
    gin.tasting_notes = request.json['tasting_notes']
    gin.pairs_with = request.json['pairs_with']
    gin.user_token = current_user_token.token

    db.session.commit()
    response = gin_schema.dump(gin)
    return jsonify(response)

@api.route('/gins/<id>', methods = ['DELETE'])
@token_required
def delete_gin(current_user_token, id):
    gin = Gin.query.get(id)
    db.session.delete(gin)
    db.session.commit()
    response = gin_schema.dump(gin)
    return jsonify(response)