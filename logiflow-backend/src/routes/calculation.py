from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.models.calculation import db, Calculation
from src.models.port import Port
from src.models.container_type import ContainerType
from src.models.shipping_line import ShippingLine
from src.models.user import User

calculation_bp = Blueprint('calculation', __name__)

@calculation_bp.route('', methods=['GET'])
@jwt_required()
def get_calculations():
    user_id = get_jwt_identity()
    calculations = Calculation.query.filter_by(user_id=user_id).order_by(Calculation.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [calc.to_dict() for calc in calculations]
    })

@calculation_bp.route('', methods=['POST'])
@jwt_required()
def create_calculation():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['port_id', 'container_type_id', 'shipping_line_id', 'calculation_type', 'vessel_departure']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} gerekli'}), 400
    
    # Parse dates
    try:
        vessel_departure = datetime.strptime(data['vessel_departure'], '%Y-%m-%d').date()
        gate_in_date = datetime.strptime(data['gate_in_date'], '%Y-%m-%d').date() if data.get('gate_in_date') else None
        gate_out_date = datetime.strptime(data['gate_out_date'], '%Y-%m-%d').date() if data.get('gate_out_date') else None
    except ValueError:
        return jsonify({'success': False, 'message': 'Geçersiz tarih formatı'}), 400
    
    # Get related objects
    port = Port.query.get(data['port_id'])
    container_type = ContainerType.query.get(data['container_type_id'])
    shipping_line = ShippingLine.query.get(data['shipping_line_id'])
    
    if not all([port, container_type, shipping_line]):
        return jsonify({'success': False, 'message': 'Geçersiz referans veriler'}), 400
    
    # Create calculation
    calculation = Calculation(
        user_id=user_id,
        port_id=data['port_id'],
        container_type_id=data['container_type_id'],
        shipping_line_id=data['shipping_line_id'],
        calculation_type=data['calculation_type'],
        vessel_departure=vessel_departure,
        gate_in_date=gate_in_date,
        gate_out_date=gate_out_date,
        is_imo=data.get('is_imo', False),
        is_oog=data.get('is_oog', False)
    )
    
    # Calculate result
    calculation.calculate_result()
    
    db.session.add(calculation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Hesaplama tamamlandı',
        'data': calculation.to_dict()
    }), 201

@calculation_bp.route('/<int:calc_id>', methods=['GET'])
@jwt_required()
def get_calculation(calc_id):
    user_id = get_jwt_identity()
    calculation = Calculation.query.filter_by(id=calc_id, user_id=user_id).first_or_404()
    
    return jsonify({
        'success': True,
        'data': calculation.to_dict()
    })
