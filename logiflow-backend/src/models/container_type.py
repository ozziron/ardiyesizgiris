from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ContainerType(db.Model):
    __tablename__ = 'container_types'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(10), nullable=False)  # 20, 40, 45
    type_category = db.Column(db.String(20), nullable=False)  # DC, HC, OT, FR, RF
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    calculations = db.relationship('Calculation', backref='container_type', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'size': self.size,
            'type_category': self.type_category,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def create_default_container_types():
        """Varsayılan konteyner tiplerini oluştur"""
        default_types = [
            {
                'code': '20DC',
                'name': "20' Standart Konteyner",
                'size': '20',
                'type_category': 'DC',
                'description': '20 feet standart dry container'
            },
            {
                'code': '40DC',
                'name': "40' Standart Konteyner",
                'size': '40',
                'type_category': 'DC',
                'description': '40 feet standart dry container'
            },
            {
                'code': '40HC',
                'name': "40' Yüksek Konteyner",
                'size': '40',
                'type_category': 'HC',
                'description': '40 feet high cube container'
            },
            {
                'code': '45HC',
                'name': "45' Yüksek Konteyner",
                'size': '45',
                'type_category': 'HC',
                'description': '45 feet high cube container'
            },
            {
                'code': '20OT',
                'name': "20' Açık Üst Konteyner",
                'size': '20',
                'type_category': 'OT',
                'description': '20 feet open top container'
            },
            {
                'code': '40OT',
                'name': "40' Açık Üst Konteyner",
                'size': '40',
                'type_category': 'OT',
                'description': '40 feet open top container'
            },
            {
                'code': '20FR',
                'name': "20' Flat Rack",
                'size': '20',
                'type_category': 'FR',
                'description': '20 feet flat rack container'
            },
            {
                'code': '40FR',
                'name': "40' Flat Rack",
                'size': '40',
                'type_category': 'FR',
                'description': '40 feet flat rack container'
            },
            {
                'code': '20RF',
                'name': "20' Soğutmalı Konteyner",
                'size': '20',
                'type_category': 'RF',
                'description': '20 feet refrigerated container'
            },
            {
                'code': '40RF',
                'name': "40' Soğutmalı Konteyner",
                'size': '40',
                'type_category': 'RF',
                'description': '40 feet refrigerated container'
            }
        ]
        
        for type_data in default_types:
            existing_type = ContainerType.query.filter_by(code=type_data['code']).first()
            if not existing_type:
                container_type = ContainerType(**type_data)
                db.session.add(container_type)
        
        db.session.commit()

