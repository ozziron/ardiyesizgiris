from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Kullanıcı adı ve şifre gerekli'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        if not user.is_active:
            return jsonify({'success': False, 'message': 'Hesap deaktif'}), 401
        
        user.update_last_login()
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'message': 'Giriş başarılı',
            'access_token': access_token,
            'user': user.to_dict()
        })
    
    return jsonify({'success': False, 'message': 'Geçersiz kullanıcı adı veya şifre'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} gerekli'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Bu kullanıcı adı zaten kullanılıyor'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Bu e-posta adresi zaten kullanılıyor'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        company=data.get('company'),
        phone=data.get('phone')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'message': 'Kayıt başarılı',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    })
