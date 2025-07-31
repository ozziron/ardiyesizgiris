from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profil bilgileri
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # Rol ve durum
    role = db.Column(db.String(20), default='user')  # user, admin, super_admin
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Tercihler
    language = db.Column(db.String(5), default='tr')
    timezone = db.Column(db.String(50), default='Europe/Istanbul')
    email_notifications = db.Column(db.Boolean, default=True)
    
    # Tarih bilgileri
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    calculations = db.relationship('Calculation', backref='user', lazy=True)
    container_trackings = db.relationship('ContainerTracking', backref='user', lazy=True)
    blog_posts = db.relationship('BlogPost', backref='author_user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'language': self.language,
            'timezone': self.timezone,
            'email_notifications': self.email_notifications,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def set_password(self, password):
        """Şifreyi hash'leyerek kaydet"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Şifreyi kontrol et"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Tam adı getir"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def update_last_login(self):
        """Son giriş tarihini güncelle"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def create_default_users():
        """Varsayılan kullanıcıları oluştur"""
        # Admin kullanıcısı
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@logiflow.com',
                first_name='Admin',
                last_name='User',
                role='super_admin',
                is_active=True,
                is_verified=True
            )
            admin_user.set_password('LogiFlow2025!')
            db.session.add(admin_user)
        
        # Test kullanıcısı
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@logiflow.com',
                first_name='Test',
                last_name='Kullanıcı',
                company='Test Lojistik A.Ş.',
                role='user',
                is_active=True,
                is_verified=True
            )
            test_user.set_password('test123')
            db.session.add(test_user)
        
        db.session.commit()
