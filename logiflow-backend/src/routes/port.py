from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.port import db, Port
from src.models.user import User

port_bp = Blueprint('port', __name__)

@port_bp.route('', methods=['GET'])
def get_ports():
    ports = Port.query.filter_by(is_active=True).all()
    return jsonify({
        'success': True,
        'data': [port.to_dict() for port in ports]
    })

@port_bp.route('/<int:port_id>', methods=['GET'])
def get_port(port_id):
    port = Port.query.get_or_404(port_id)
    return jsonify({
        'success': True,
        'data': port.to_dict()
    })

@port_bp.route('', methods=['POST'])
@jwt_required()
def create_port():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role not in ['admin', 'super_admin']:
        return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
    
    data = request.get_json()
    
    port = Port(
        code=data['code'],
        name=data['name'],
        city=data['city'],
        country=data.get('country', 'Turkey'),
        ardiye_free_days=data.get('ardiye_free_days', 7),
        detention_free_days=data.get('detention_free_days', 7)
    )
    
    db.session.add(port)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Liman oluşturuldu',
        'data': port.to_dict()
    }), 201
