"""
models.py — RoadMate Pro
All MySQL table definitions using SQLAlchemy ORM.
Tables are created automatically when app starts.
"""
from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.String(36),  primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name     = db.Column(db.String(120), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow,
                              onupdate=datetime.utcnow)

    trips = db.relationship('Trip', backref='user', lazy=True,
                            cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id':         self.id,
            'username':   self.username,
            'email':      self.email,
            'full_name':  self.full_name,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }


class Trip(db.Model):
    __tablename__ = 'trips'

    id                       = db.Column(db.String(36),  primary_key=True)
    user_id                  = db.Column(db.String(36),
                                         db.ForeignKey('users.id'), nullable=False)
    source                   = db.Column(db.String(100), nullable=False)
    destination              = db.Column(db.String(100), nullable=False)
    distance_km              = db.Column(db.Float,       nullable=False)
    travel_days              = db.Column(db.Integer,     nullable=False)
    vehicle_mileage          = db.Column(db.Float,       nullable=False)
    fuel_price               = db.Column(db.Float,       nullable=False)
    accommodation_budget     = db.Column(db.String(20),  nullable=False)
    estimated_duration_hours = db.Column(db.Float,       nullable=False)
    status                   = db.Column(db.String(20),  default='planned')
    notes                    = db.Column(db.Text,        nullable=True)
    packed_items             = db.Column(db.Text,        nullable=True)
    created_at               = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at               = db.Column(db.DateTime,    default=datetime.utcnow,
                                         onupdate=datetime.utcnow)

    costs = db.relationship('TripCost', backref='trip', lazy=True,
                            cascade='all, delete-orphan', uselist=False)

    def to_dict(self):
        return {
            'id':                       self.id,
            'user_id':                  self.user_id,
            'source':                   self.source,
            'destination':              self.destination,
            'distance_km':              self.distance_km,
            'travel_days':              self.travel_days,
            'vehicle_mileage':          self.vehicle_mileage,
            'fuel_price':               self.fuel_price,
            'accommodation_budget':     self.accommodation_budget,
            'estimated_duration_hours': self.estimated_duration_hours,
            'status':                   self.status,
            'notes':                    self.notes or '',
            'packed_items':             self.packed_items or '',
            'created_at':               str(self.created_at),
            'updated_at':               str(self.updated_at),
        }


class TripCost(db.Model):
    __tablename__ = 'trip_costs'

    id                   = db.Column(db.String(36), primary_key=True)
    trip_id              = db.Column(db.String(36),
                                     db.ForeignKey('trips.id'), nullable=False)
    user_id              = db.Column(db.String(36), nullable=False)
    fuel_required_liters = db.Column(db.Float, nullable=False)
    fuel_cost            = db.Column(db.Float, nullable=False)
    toll_cost            = db.Column(db.Float, nullable=False)
    toll_rate_per_km     = db.Column(db.Float, nullable=False)
    accommodation_cost   = db.Column(db.Float, nullable=False)
    nights               = db.Column(db.Integer, nullable=False)
    avg_price_per_night  = db.Column(db.Float, nullable=False)
    total_cost           = db.Column(db.Float, nullable=False)
    cost_per_km          = db.Column(db.Float, nullable=False)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':                   self.id,
            'trip_id':              self.trip_id,
            'user_id':              self.user_id,
            'fuel_required_liters': self.fuel_required_liters,
            'fuel_cost':            self.fuel_cost,
            'toll_cost':            self.toll_cost,
            'toll_rate_per_km':     self.toll_rate_per_km,
            'accommodation_cost':   self.accommodation_cost,
            'nights':               self.nights,
            'avg_price_per_night':  self.avg_price_per_night,
            'total_cost':           self.total_cost,
            'cost_per_km':          self.cost_per_km,
            'created_at':           str(self.created_at),
        }


class Location(db.Model):
    __tablename__ = 'locations'

    id                       = db.Column(db.String(36),  primary_key=True)
    route_key                = db.Column(db.String(200), nullable=False, index=True)
    name                     = db.Column(db.String(200), nullable=False)
    category                 = db.Column(db.String(50),  nullable=False)
    distance_from_route_km   = db.Column(db.Float,       default=0.0)
    city                     = db.Column(db.String(100), nullable=False)
    rating                   = db.Column(db.Float,       default=4.0)
    price_per_night          = db.Column(db.Float,       nullable=True)
    budget_band              = db.Column(db.String(20),  nullable=True)

    def to_dict(self):
        d = {
            'id':                     self.id,
            'route_key':              self.route_key,
            'name':                   self.name,
            'category':               self.category,
            'distance_from_route_km': self.distance_from_route_km,
            'city':                   self.city,
            'rating':                 self.rating,
        }
        if self.price_per_night:
            d['price_per_night'] = self.price_per_night
        if self.budget_band:
            d['budget_band'] = self.budget_band
        return d
