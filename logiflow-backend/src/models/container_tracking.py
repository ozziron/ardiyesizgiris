from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class ContainerTracking(db.Model):
    __tablename__ = 'container_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Konteyner bilgileri
    container_no = db.Column(db.String(20), nullable=False)
    bl_no = db.Column(db.String(50))
    booking_no = db.Column(db.String(50))
    
    # Gemi ve rota bilgileri
    vessel_name = db.Column(db.String(100))
    voyage_no = db.Column(db.String(20))
    loading_port = db.Column(db.String(100))
    discharge_port = db.Column(db.String(100))
    final_destination = db.Column(db.String(100))
    
    # Konum ve durum
    current_location = db.Column(db.String(100))
    status = db.Column(db.String(50))  # loaded, in_transit, discharged, delivered, etc.
    
    # Tarih bilgileri
    etd = db.Column(db.DateTime)  # Estimated Time of Departure
    eta = db.Column(db.DateTime)  # Estimated Time of Arrival
    atd = db.Column(db.DateTime)  # Actual Time of Departure
    ata = db.Column(db.DateTime)  # Actual Time of Arrival
    gate_in_date = db.Column(db.DateTime)
    gate_out_date = db.Column(db.DateTime)
    
    # Nakliye şirketi
    shipping_line = db.Column(db.String(50))
    
    # Takip detayları (JSON)
    tracking_details = db.Column(db.Text)  # JSON string for additional tracking info
    
    # Bildirim ayarları
    notifications_enabled = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    
    # Meta bilgiler
    is_active = db.Column(db.Boolean, default=True)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    tracking_history = db.relationship('TrackingHistory', backref='container_tracking', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'container_no': self.container_no,
            'bl_no': self.bl_no,
            'booking_no': self.booking_no,
            'vessel_name': self.vessel_name,
            'voyage_no': self.voyage_no,
            'loading_port': self.loading_port,
            'discharge_port': self.discharge_port,
            'final_destination': self.final_destination,
            'current_location': self.current_location,
            'status': self.status,
            'etd': self.etd.isoformat() if self.etd else None,
            'eta': self.eta.isoformat() if self.eta else None,
            'atd': self.atd.isoformat() if self.atd else None,
            'ata': self.ata.isoformat() if self.ata else None,
            'gate_in_date': self.gate_in_date.isoformat() if self.gate_in_date else None,
            'gate_out_date': self.gate_out_date.isoformat() if self.gate_out_date else None,
            'shipping_line': self.shipping_line,
            'tracking_details': json.loads(self.tracking_details) if self.tracking_details else None,
            'notifications_enabled': self.notifications_enabled,
            'email_notifications': self.email_notifications,
            'sms_notifications': self.sms_notifications,
            'is_active': self.is_active,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def set_tracking_details(self, details_dict):
        """Takip detaylarını JSON olarak kaydet"""
        self.tracking_details = json.dumps(details_dict, ensure_ascii=False)
    
    def get_tracking_details(self):
        """Takip detaylarını dict olarak getir"""
        if self.tracking_details:
            return json.loads(self.tracking_details)
        return {}


class TrackingHistory(db.Model):
    __tablename__ = 'tracking_history'
    
    id = db.Column(db.Integer, primary_key=True)
    container_tracking_id = db.Column(db.Integer, db.ForeignKey('container_tracking.id'), nullable=False)
    
    # Geçmiş bilgiler
    location = db.Column(db.String(100))
    status = db.Column(db.String(50))
    event_description = db.Column(db.Text)
    event_date = db.Column(db.DateTime)
    
    # Meta bilgiler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'container_tracking_id': self.container_tracking_id,
            'location': self.location,
            'status': self.status,
            'event_description': self.event_description,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

