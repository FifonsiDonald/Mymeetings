from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task, User
from app.extensions import db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    tasks = Task.query.filter_by(user_id=user.id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    data = request.get_json()
    task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=data.get('due_date'),
        priority=data.get('priority'),
        user_id=user.id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    task = Task.query.filter_by(id=task_id, user_id=user.id).first_or_404()
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    task = Task.query.filter_by(id=task_id, user_id=user.id).first_or_404()
    data = request.get_json()
    task.title = data['title']
    task.description = data.get('description')
    task.due_date = data.get('due_date')
    task.priority = data.get('priority')
    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    task = Task.query.filter_by(id=task_id, user_id=user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Task deleted"}), 200
