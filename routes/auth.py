from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.models import User
from app.extensions import db

auth_bp =  Blueprint('auth', __name__)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email already exists'}), 400
    
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

#Supervisor/Teacher & Supervisee/student reg & login division 