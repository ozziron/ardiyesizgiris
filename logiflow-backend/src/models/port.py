from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Port(db.Model):
    __tablename__ = 'ports'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), default='Turkey')
    city = db.Column(db.String(50), nullable=False)
    ardiye_free_days = db.Column(db.Integer, default=7)
    detention_free_days = db.Column(db.Integer, default=7)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    calculations = db.relationship('Calculation', backref='port', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'ardiye_free_days': self.ardiye_free_days,
            'detention_free_days': self.detention_free_days,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def create_default_ports():
        """Varsayılan Türkiye limanlarını oluştur"""
        default_ports = [
            {
                'code': 'TRIST',
                'name': 'İstanbul Limanı',
                'city': 'İstanbul',
                'ardiye_free_days': 7,
                'detention_free_days': 10
            },
            {
                'code': 'TRIZM',
                'name': 'İzmir Limanı',
                'city': 'İzmir',
                'ardiye_free_days': 7,
                'detention_free_days': 10
            },
            {
                'code': 'TRMER',
                'name': 'Mersin Limanı',
                'city': 'Mersin',
                'ardiye_free_days': 10,
                'detention_free_days': 12
            },
            {
                'code': 'TRISK',
                'name': 'İskenderun Limanı',
                'city': 'İskenderun',
                'ardiye_free_days': 8,
                'detention_free_days': 10
            },
            {
                'code': 'TRSAM',
                'name': 'Samsun Limanı',
                'city': 'Samsun',
                'ardiye_free_days': 7,
                'detention_free_days': 9
            },
            {
                'code': 'TRTEK',
                'name': 'Tekirdağ Limanı',
                'city': 'Tekirdağ',
                'ardiye_free_days': 7,
                'detention_free_days': 10
            },
            {
                'code': 'TRANT',
                'name': 'Antalya Limanı',
                'city': 'Antalya',
                'ardiye_free_days': 6,
                'detention_free_days': 8
            },
            {
                'code': 'TRTRA',
                'name': 'Trabzon Limanı',
                'city': 'Trabzon',
                'ardiye_free_days': 7,
                'detention_free_days': 9
            }
        ]
        
        for port_data in default_ports:
            existing_port = Port.query.filter_by(code=port_data['code']).first()
            if not existing_port:
                port = Port(**port_data)
                db.session.add(port)
        
        db.session.commit()

