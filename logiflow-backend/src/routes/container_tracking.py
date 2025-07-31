from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import random
from src.models.container_tracking import db, ContainerTracking, TrackingHistory
from src.models.user import User

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/search', methods=['POST'])
def search_container():
    data = request.get_json()
    container_no = data.get('container_no')
    
    if not container_no:
        return jsonify({'success': False, 'message': 'Konteyner numarası gerekli'}), 400
    
    # Mock tracking data
    mock_data = {
        'container_no': container_no.upper(),
        'bl_no': f'BL{random.randint(100000, 999999)}',
        'booking_no': f'BK{random.randint(100000, 999999)}',
        'vessel_name': random.choice(['MSC ISTANBUL', 'MAERSK ANKARA', 'CMA CGM IZMIR']),
        'voyage_no': f'{random.randint(100, 999)}W',
        'loading_port': random.choice(['Shanghai', 'Hamburg', 'Rotterdam']),
        'discharge_port': random.choice(['Istanbul', 'Izmir', 'Mersin']),
        'current_location': random.choice(['At Sea', 'Istanbul Port', 'Customs']),
        'status': random.choice(['loaded', 'in_transit', 'discharged', 'delivered']),
        'shipping_line': random.choice(['MSC', 'MAERSK', 'CMA CGM']),
        'eta': (datetime.now() + timedelta(days=random.randint(1, 10))).isoformat(),
        'last_update': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'data': mock_data
    })

@tracking_bp.route('', methods=['GET'])
@jwt_required()
def get_user_trackings():
    user_id = get_jwt_identity()
    trackings = ContainerTracking.query.filter_by(user_id=user_id, is_active=True).all()
    
    return jsonify({
        'success': True,
        'data': [tracking.to_dict() for tracking in trackings]
    })

@tracking_bp.route('', methods=['POST'])
@jwt_required()
def add_tracking():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('container_no'):
        return jsonify({'success': False, 'message': 'Konteyner numarası gerekli'}), 400
    
    tracking = ContainerTracking(
        user_id=user_id,
        container_no=data['container_no'].upper(),
        bl_no=data.get('bl_no'),
        booking_no=data.get('booking_no'),
        vessel_name=data.get('vessel_name'),
        shipping_line=data.get('shipping_line')
    )
    
    db.session.add(tracking)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Konteyner takip listesine eklendi',
        'data': tracking.to_dict()
    }), 201
