from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.container_type import db, ContainerType
from src.models.user import User

container_type_bp = Blueprint('container_type', __name__)

@container_type_bp.route('', methods=['GET'])
def get_container_types():
    container_types = ContainerType.query.filter_by(is_active=True).all()
    return jsonify({
        'success': True,
        'data': [ct.to_dict() for ct in container_types]
    })

@container_type_bp.route('/<int:type_id>', methods=['GET'])
def get_container_type(type_id):
    container_type = ContainerType.query.get_or_404(type_id)
    return jsonify({
        'success': True,
        'data': container_type.to_dict()
    })
