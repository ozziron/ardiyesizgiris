from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.shipping_line import db, ShippingLine
from src.models.user import User

shipping_line_bp = Blueprint('shipping_line', __name__)

@shipping_line_bp.route('', methods=['GET'])
def get_shipping_lines():
    lines = ShippingLine.query.filter_by(is_active=True).all()
    return jsonify({
        'success': True,
        'data': [line.to_dict() for line in lines]
    })

@shipping_line_bp.route('/<int:line_id>', methods=['GET'])
def get_shipping_line(line_id):
    line = ShippingLine.query.get_or_404(line_id)
    return jsonify({
        'success': True,
        'data': line.to_dict()
    })
