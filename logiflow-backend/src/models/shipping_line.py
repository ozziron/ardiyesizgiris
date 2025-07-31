from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ShippingLine(db.Model):
    __tablename__ = 'shipping_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200))
    multiplier = db.Column(db.Float, default=1.0)  # Free time çarpanı
    country = db.Column(db.String(50))
    website = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    calculations = db.relationship('Calculation', backref='shipping_line', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'full_name': self.full_name,
            'multiplier': self.multiplier,
            'country': self.country,
            'website': self.website,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def create_default_shipping_lines():
        """Varsayılan nakliye hatlarını oluştur"""
        default_lines = [
            {
                'code': 'MAEU',
                'name': 'Maersk Line',
                'full_name': 'A.P. Moller-Maersk',
                'multiplier': 1.0,
                'country': 'Denmark',
                'website': 'https://www.maersk.com'
            },
            {
                'code': 'MSC',
                'name': 'MSC',
                'full_name': 'Mediterranean Shipping Company',
                'multiplier': 1.2,
                'country': 'Switzerland',
                'website': 'https://www.msc.com'
            },
            {
                'code': 'CMA',
                'name': 'CMA CGM',
                'full_name': 'CMA CGM Group',
                'multiplier': 1.1,
                'country': 'France',
                'website': 'https://www.cma-cgm.com'
            },
            {
                'code': 'COSCO',
                'name': 'COSCO',
                'full_name': 'China Ocean Shipping Company',
                'multiplier': 0.9,
                'country': 'China',
                'website': 'https://www.cosco.com'
            },
            {
                'code': 'HAPAG',
                'name': 'Hapag-Lloyd',
                'full_name': 'Hapag-Lloyd AG',
                'multiplier': 1.1,
                'country': 'Germany',
                'website': 'https://www.hapag-lloyd.com'
            },
            {
                'code': 'EMC',
                'name': 'Evergreen',
                'full_name': 'Evergreen Marine Corporation',
                'multiplier': 1.0,
                'country': 'Taiwan',
                'website': 'https://www.evergreen-marine.com'
            },
            {
                'code': 'OOCL',
                'name': 'OOCL',
                'full_name': 'Orient Overseas Container Line',
                'multiplier': 1.0,
                'country': 'Hong Kong',
                'website': 'https://www.oocl.com'
            },
            {
                'code': 'YML',
                'name': 'Yang Ming',
                'full_name': 'Yang Ming Marine Transport Corporation',
                'multiplier': 0.9,
                'country': 'Taiwan',
                'website': 'https://www.yangming.com'
            },
            {
                'code': 'ZIM',
                'name': 'ZIM',
                'full_name': 'ZIM Integrated Shipping Services',
                'multiplier': 1.0,
                'country': 'Israel',
                'website': 'https://www.zim.com'
            },
            {
                'code': 'ONE',
                'name': 'ONE',
                'full_name': 'Ocean Network Express',
                'multiplier': 1.0,
                'country': 'Japan',
                'website': 'https://www.one-line.com'
            }
        ]
        
        for line_data in default_lines:
            existing_line = ShippingLine.query.filter_by(code=line_data['code']).first()
            if not existing_line:
                shipping_line = ShippingLine(**line_data)
                db.session.add(shipping_line)
        
        db.session.commit()

