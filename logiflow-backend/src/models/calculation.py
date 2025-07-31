from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class Calculation(db.Model):
    __tablename__ = 'calculations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    port_id = db.Column(db.Integer, db.ForeignKey('ports.id'), nullable=False)
    container_type_id = db.Column(db.Integer, db.ForeignKey('container_types.id'), nullable=False)
    shipping_line_id = db.Column(db.Integer, db.ForeignKey('shipping_lines.id'), nullable=False)
    
    # Hesaplama tipi
    calculation_type = db.Column(db.String(20), nullable=False)  # 'ardiye' veya 'detention'
    
    # Tarih bilgileri
    vessel_departure = db.Column(db.Date, nullable=False)
    gate_in_date = db.Column(db.Date)
    gate_out_date = db.Column(db.Date)
    
    # Özel durumlar
    is_imo = db.Column(db.Boolean, default=False)  # Tehlikeli yük
    is_oog = db.Column(db.Boolean, default=False)  # Taşmalı yük
    
    # Hesaplama sonuçları
    free_days = db.Column(db.Integer)
    used_days = db.Column(db.Integer)
    remaining_days = db.Column(db.Integer)
    result_date = db.Column(db.Date)
    cost_per_day = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    
    # Hesaplama detayları (JSON)
    calculation_details = db.Column(db.Text)  # JSON string
    
    # Meta bilgiler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'port': self.port.to_dict() if self.port else None,
            'container_type': self.container_type.to_dict() if self.container_type else None,
            'shipping_line': self.shipping_line.to_dict() if self.shipping_line else None,
            'calculation_type': self.calculation_type,
            'vessel_departure': self.vessel_departure.isoformat() if self.vessel_departure else None,
            'gate_in_date': self.gate_in_date.isoformat() if self.gate_in_date else None,
            'gate_out_date': self.gate_out_date.isoformat() if self.gate_out_date else None,
            'is_imo': self.is_imo,
            'is_oog': self.is_oog,
            'free_days': self.free_days,
            'used_days': self.used_days,
            'remaining_days': self.remaining_days,
            'result_date': self.result_date.isoformat() if self.result_date else None,
            'cost_per_day': self.cost_per_day,
            'total_cost': self.total_cost,
            'calculation_details': json.loads(self.calculation_details) if self.calculation_details else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def set_calculation_details(self, details_dict):
        """Hesaplama detaylarını JSON olarak kaydet"""
        self.calculation_details = json.dumps(details_dict, ensure_ascii=False)
    
    def get_calculation_details(self):
        """Hesaplama detaylarını dict olarak getir"""
        if self.calculation_details:
            return json.loads(self.calculation_details)
        return {}
    
    @staticmethod
    def calculate_free_time(port, shipping_line, container_type, calculation_type, is_imo=False, is_oog=False):
        """Free time hesaplama algoritması"""
        
        # Temel free time
        if calculation_type == 'ardiye':
            base_free_days = port.ardiye_free_days
        else:  # detention
            base_free_days = port.detention_free_days
        
        # Hat çarpanı uygula
        free_days = int(base_free_days * shipping_line.multiplier)
        
        # Özel yük durumları
        if is_imo:
            free_days = max(1, free_days - 2)  # IMO yüklerde 2 gün azalt
        
        if is_oog:
            free_days = max(1, free_days - 1)  # OOG yüklerde 1 gün azalt
        
        # Konteyner tipine göre ayarlama
        if container_type.type_category in ['RF', 'OT', 'FR']:
            free_days = max(1, free_days - 1)  # Özel konteynerler için 1 gün azalt
        
        return free_days
    
    @staticmethod
    def calculate_business_days(start_date, end_date):
        """İş günü hesaplama (hafta sonları hariç)"""
        if not start_date or not end_date:
            return 0
        
        current_date = start_date
        business_days = 0
        
        while current_date <= end_date:
            # Pazartesi=0, Pazar=6
            if current_date.weekday() < 5:  # Pazartesi-Cuma
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days
    
    def calculate_result(self):
        """Hesaplama sonucunu hesapla ve kaydet"""
        
        # Free time hesapla
        self.free_days = self.calculate_free_time(
            self.port, 
            self.shipping_line, 
            self.container_type, 
            self.calculation_type,
            self.is_imo, 
            self.is_oog
        )
        
        # Hesaplama tipine göre kullanılan günleri hesapla
        if self.calculation_type == 'ardiye':
            # Ardiye: Gemi kalkış tarihinden gate out tarihine kadar
            if self.gate_out_date:
                self.used_days = self.calculate_business_days(self.vessel_departure, self.gate_out_date)
            else:
                # Gate out tarihi yoksa bugüne kadar
                self.used_days = self.calculate_business_days(self.vessel_departure, datetime.now().date())
        else:
            # Detention: Gate in tarihinden gate out tarihine kadar
            if self.gate_in_date and self.gate_out_date:
                self.used_days = self.calculate_business_days(self.gate_in_date, self.gate_out_date)
            elif self.gate_in_date:
                # Gate out tarihi yoksa bugüne kadar
                self.used_days = self.calculate_business_days(self.gate_in_date, datetime.now().date())
            else:
                self.used_days = 0
        
        # Kalan günleri hesapla
        self.remaining_days = max(0, self.free_days - self.used_days)
        
        # Sonuç tarihini hesapla
        if self.calculation_type == 'ardiye':
            start_date = self.vessel_departure
        else:
            start_date = self.gate_in_date or self.vessel_departure
        
        # Free time bitim tarihini hesapla
        current_date = start_date
        days_added = 0
        
        while days_added < self.free_days:
            if current_date.weekday() < 5:  # İş günü
                days_added += 1
            if days_added < self.free_days:
                current_date += timedelta(days=1)
        
        self.result_date = current_date
        
        # Maliyet hesaplama (örnek değerler)
        base_cost_per_day = {
            '20': 50,  # 20' konteyner için günlük maliyet (USD)
            '40': 75,  # 40' konteyner için günlük maliyet (USD)
            '45': 85   # 45' konteyner için günlük maliyet (USD)
        }
        
        self.cost_per_day = base_cost_per_day.get(self.container_type.size, 50)
        
        # Özel konteyner tipleri için maliyet artışı
        if self.container_type.type_category in ['RF', 'OT', 'FR']:
            self.cost_per_day *= 1.5
        
        # Toplam maliyet (sadece free time aşıldığında)
        if self.used_days > self.free_days:
            overtime_days = self.used_days - self.free_days
            self.total_cost = overtime_days * self.cost_per_day
        else:
            self.total_cost = 0
        
        # Hesaplama detaylarını kaydet
        details = {
            'base_free_days': self.port.ardiye_free_days if self.calculation_type == 'ardiye' else self.port.detention_free_days,
            'line_multiplier': self.shipping_line.multiplier,
            'imo_adjustment': -2 if self.is_imo else 0,
            'oog_adjustment': -1 if self.is_oog else 0,
            'container_adjustment': -1 if self.container_type.type_category in ['RF', 'OT', 'FR'] else 0,
            'calculation_steps': [
                f"Temel free time: {self.port.ardiye_free_days if self.calculation_type == 'ardiye' else self.port.detention_free_days} gün",
                f"Hat çarpanı ({self.shipping_line.name}): x{self.shipping_line.multiplier}",
                f"IMO ayarlaması: {-2 if self.is_imo else 0} gün",
                f"OOG ayarlaması: {-1 if self.is_oog else 0} gün",
                f"Konteyner tipi ayarlaması: {-1 if self.container_type.type_category in ['RF', 'OT', 'FR'] else 0} gün",
                f"Toplam free time: {self.free_days} gün"
            ]
        }
        
        self.set_calculation_details(details)

