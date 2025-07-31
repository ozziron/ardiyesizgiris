from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.port import Port
from src.models.container_type import ContainerType
from src.models.shipping_line import ShippingLine
from src.models.calculation import Calculation
from src.models.blog_post import BlogPost

admin_bp = Blueprint('admin', __name__)

def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role in ['admin', 'super_admin']

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    if not admin_required():
        return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
    
    stats = {
        'total_users': User.query.count(),
        'total_calculations': Calculation.query.count(),
        'total_ports': Port.query.count(),
        'total_blog_posts': BlogPost.query.count(),
        'recent_calculations': [calc.to_dict() for calc in Calculation.query.order_by(Calculation.created_at.desc()).limit(5).all()],
        'recent_users': [user.to_dict() for user in User.query.order_by(User.created_at.desc()).limit(5).all()]
    }
    
    return jsonify({
        'success': True,
        'data': stats
    })

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    if not admin_required():
        return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
    
    users = User.query.all()
    return jsonify({
        'success': True,
        'data': [user.to_dict() for user in users]
    })
