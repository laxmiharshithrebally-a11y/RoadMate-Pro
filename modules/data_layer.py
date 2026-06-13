"""
data_layer.py — RoadMate Pro Phase 1
All data operations now use MySQL via SQLAlchemy.
Same function names as before — rest of app unchanged.
"""
import uuid
from datetime import datetime
from extensions import db
from models import User, Trip, TripCost, Location


def gen_id():
    return str(uuid.uuid4())


def now():
    return datetime.utcnow()


# ── USERS ──────────────────────────────────────────────────────────────────

def get_all_users():
    return [u.to_dict() for u in User.query.all()]


def get_user_by_id(uid):
    u = User.query.filter_by(id=uid).first()
    return u.to_dict() if u else None


def get_user_by_email(email):
    u = User.query.filter(
        User.email.ilike(email.strip())).first()
    return u.to_dict() if u else None


def get_user_by_username(uname):
    u = User.query.filter(
        User.username.ilike(uname.strip())).first()
    return u.to_dict() if u else None


def create_user(username, email, pw_hash, full_name):
    u = User(
        id=gen_id(), username=username.strip(),
        email=email.strip(), password_hash=pw_hash,
        full_name=full_name.strip()
    )
    db.session.add(u)
    db.session.commit()
    return u.to_dict()


def update_user(uid, updates):
    u = User.query.filter_by(id=uid).first()
    if not u:
        return None
    for k, v in updates.items():
        if hasattr(u, k):
            setattr(u, k, v)
    u.updated_at = now()
    db.session.commit()
    return u.to_dict()


def get_user_password_hash(uid):
    u = User.query.filter_by(id=uid).first()
    return u.password_hash if u else None


# ── TRIPS ──────────────────────────────────────────────────────────────────

def get_trips_by_user(uid):
    trips = Trip.query.filter_by(user_id=uid).order_by(
        Trip.created_at.desc()).all()
    return [t.to_dict() for t in trips]


def get_trip_by_id(tid):
    t = Trip.query.filter_by(id=tid).first()
    return t.to_dict() if t else None


def create_trip(uid, p):
    t = Trip(
        id=gen_id(), user_id=uid,
        source=p['source'], destination=p['destination'],
        distance_km=p['distance_km'], travel_days=p['travel_days'],
        vehicle_mileage=p['vehicle_mileage'], fuel_price=p['fuel_price'],
        accommodation_budget=p['accommodation_budget'],
        estimated_duration_hours=p['estimated_duration_hours'],
        status='planned'
    )
    db.session.add(t)
    db.session.commit()
    return t.to_dict()


def delete_trip(tid, uid):
    t = Trip.query.filter_by(id=tid, user_id=uid).first()
    if not t:
        return False
    db.session.delete(t)
    db.session.commit()
    return True


def update_trip(tid, uid, updates):
    t = Trip.query.filter_by(id=tid, user_id=uid).first()
    if not t:
        return None
    for k, v in updates.items():
        if hasattr(t, k):
            setattr(t, k, v)
    t.updated_at = now()
    db.session.commit()
    return t.to_dict()


def get_all_trips():
    return [t.to_dict() for t in Trip.query.order_by(
        Trip.created_at.desc()).all()]


# ── COSTS ──────────────────────────────────────────────────────────────────

def create_trip_cost(tid, uid, d):
    c = TripCost(
        id=gen_id(), trip_id=tid, user_id=uid,
        fuel_required_liters=d['fuel_required_liters'],
        fuel_cost=d['fuel_cost'],
        toll_cost=d['toll_cost'],
        toll_rate_per_km=d.get('toll_rate_per_km', 1.5),
        accommodation_cost=d['accommodation_cost'],
        nights=d.get('nights', 0),
        avg_price_per_night=d.get('avg_price_per_night', 0),
        total_cost=d['total_cost'],
        cost_per_km=d['cost_per_km'],
    )
    db.session.add(c)
    db.session.commit()
    return c.to_dict()


def get_cost_by_trip(tid):
    c = TripCost.query.filter_by(trip_id=tid).first()
    return c.to_dict() if c else None


def get_costs_by_user(uid):
    return [c.to_dict() for c in
            TripCost.query.filter_by(user_id=uid).all()]


# ── LOCATIONS ──────────────────────────────────────────────────────────────

def get_resources_for_route(src, dst):
    key  = f"{src.lower()}_{dst.lower()}"
    key2 = f"{dst.lower()}_{src.lower()}"
    locs = Location.query.filter(
        Location.route_key.in_([key, key2, 'generic'])
    ).all()
    return [l.to_dict() for l in locs]


def seed_locations():
    """Seed location data if table is empty."""
    if Location.query.count() > 0:
        return

    locations = [
        # ── GENERIC ────────────────────────────────────────────────────
        Location(id=gen_id(), route_key='generic', name='BPCL Highway Fuel Station',   category='fuel_station', distance_from_route_km=0.2, city='En Route',    rating=4.0),
        Location(id=gen_id(), route_key='generic', name='Indian Oil NH Pump',           category='fuel_station', distance_from_route_km=0.3, city='En Route',    rating=3.9),
        Location(id=gen_id(), route_key='generic', name='HP Petrol Station',            category='fuel_station', distance_from_route_km=0.4, city='En Route',    rating=4.1),
        Location(id=gen_id(), route_key='generic', name='Highway Dhaba & Rest Stop',    category='rest_stop',    distance_from_route_km=0.0, city='En Route',    rating=3.7),
        Location(id=gen_id(), route_key='generic', name='Haldiram Highway Outlet',      category='rest_stop',    distance_from_route_km=0.1, city='En Route',    rating=4.2),
        Location(id=gen_id(), route_key='generic', name='District General Hospital',    category='emergency',    distance_from_route_km=3.0, city='Nearest Town', rating=4.0),
        Location(id=gen_id(), route_key='generic', name='Police Assistance Booth',      category='emergency',    distance_from_route_km=0.0, city='En Route',    rating=4.0),
        Location(id=gen_id(), route_key='generic', name='OYO Rooms Highway',            category='hotel',        distance_from_route_km=1.5, city='En Route',    rating=3.8, price_per_night=1200, budget_band='budget'),
        Location(id=gen_id(), route_key='generic', name='Treebo Mid Budget Hotel',      category='hotel',        distance_from_route_km=2.0, city='En Route',    rating=4.0, price_per_night=2500, budget_band='mid'),
        # ── HYDERABAD → MUMBAI ─────────────────────────────────────────
        Location(id=gen_id(), route_key='hyderabad_mumbai', name='Shell Pump Gulbarga',      category='fuel_station', distance_from_route_km=0.3, city='Gulbarga', rating=4.2),
        Location(id=gen_id(), route_key='hyderabad_mumbai', name='Reliance Petrol Solapur',  category='fuel_station', distance_from_route_km=0.5, city='Solapur',  rating=4.0),
        Location(id=gen_id(), route_key='hyderabad_mumbai', name='Hotel Sai International',  category='hotel',        distance_from_route_km=1.2, city='Solapur',  rating=3.8, price_per_night=1200, budget_band='budget'),
        Location(id=gen_id(), route_key='hyderabad_mumbai', name='Treebo Trend Pune East',   category='hotel',        distance_from_route_km=2.0, city='Pune',     rating=4.2, price_per_night=2500, budget_band='mid'),
        Location(id=gen_id(), route_key='hyderabad_mumbai', name='The Fern Pune',             category='hotel',        distance_from_route_km=3.0, city='Pune',     rating=4.5, price_per_night=5500, budget_band='premium'),
        Location(id=gen_id(), route_key='hyderabad_mumbai', name='NH65 Rest Area Gulbarga',   category='rest_stop',    distance_from_route_km=0.1, city='Gulbarga', rating=3.5),
        Location(id=gen_id(), route_key='hyderabad_mumbai', name='Apollo Emergency Clinic',   category='emergency',    distance_from_route_km=0.8, city='Solapur',  rating=4.5),
        # ── DELHI → MUMBAI ─────────────────────────────────────────────
        Location(id=gen_id(), route_key='delhi_mumbai', name='IOCL Pump Vadodara',       category='fuel_station', distance_from_route_km=0.3, city='Vadodara', rating=4.1),
        Location(id=gen_id(), route_key='delhi_mumbai', name='BPCL Station Surat',       category='fuel_station', distance_from_route_km=0.4, city='Surat',    rating=4.0),
        Location(id=gen_id(), route_key='delhi_mumbai', name='OYO Townhouse Vadodara',   category='hotel',        distance_from_route_km=1.5, city='Vadodara', rating=3.9, price_per_night=1100, budget_band='budget'),
        Location(id=gen_id(), route_key='delhi_mumbai', name='Lemon Tree Surat',         category='hotel',        distance_from_route_km=2.0, city='Surat',    rating=4.3, price_per_night=3200, budget_band='mid'),
        Location(id=gen_id(), route_key='delhi_mumbai', name='Courtyard Marriott Surat', category='hotel',        distance_from_route_km=3.0, city='Surat',    rating=4.6, price_per_night=6500, budget_band='premium'),
        Location(id=gen_id(), route_key='delhi_mumbai', name='Kota Rest Area',           category='rest_stop',    distance_from_route_km=0.2, city='Kota',     rating=3.6),
        Location(id=gen_id(), route_key='delhi_mumbai', name='Fortis Hospital Vadodara', category='emergency',    distance_from_route_km=1.0, city='Vadodara', rating=4.4),
        # ── BANGALORE → CHENNAI ────────────────────────────────────────
        Location(id=gen_id(), route_key='bangalore_chennai', name='BPCL Pump Krishnagiri',  category='fuel_station', distance_from_route_km=0.3, city='Krishnagiri', rating=4.1),
        Location(id=gen_id(), route_key='bangalore_chennai', name='Hotel Vellore Grand',    category='hotel',        distance_from_route_km=1.0, city='Vellore',     rating=3.7, price_per_night=1000, budget_band='budget'),
        Location(id=gen_id(), route_key='bangalore_chennai', name='The Accord Vellore',     category='hotel',        distance_from_route_km=1.5, city='Vellore',     rating=4.1, price_per_night=2800, budget_band='mid'),
        Location(id=gen_id(), route_key='bangalore_chennai', name='NH44 Food Court',        category='rest_stop',    distance_from_route_km=0.0, city='Krishnagiri', rating=3.8),
        Location(id=gen_id(), route_key='bangalore_chennai', name='CMC Hospital Vellore',   category='emergency',    distance_from_route_km=0.5, city='Vellore',     rating=4.9),
        # ── DELHI → JAIPUR ─────────────────────────────────────────────
        Location(id=gen_id(), route_key='delhi_jaipur', name='BPCL Pump Gurugram',          category='fuel_station', distance_from_route_km=0.3, city='Gurugram', rating=4.2),
        Location(id=gen_id(), route_key='delhi_jaipur', name='OYO Dharuhera',               category='hotel',        distance_from_route_km=1.0, city='Dharuhera', rating=3.7, price_per_night=800,   budget_band='budget'),
        Location(id=gen_id(), route_key='delhi_jaipur', name='Holiday Inn Express Jaipur',  category='hotel',        distance_from_route_km=2.0, city='Jaipur',    rating=4.4, price_per_night=3500,  budget_band='mid'),
        Location(id=gen_id(), route_key='delhi_jaipur', name='Taj Rambagh Palace Jaipur',   category='hotel',        distance_from_route_km=4.0, city='Jaipur',    rating=4.9, price_per_night=25000, budget_band='luxury'),
        Location(id=gen_id(), route_key='delhi_jaipur', name='NH48 Dhaba Stop',             category='rest_stop',    distance_from_route_km=0.0, city='Shahpura',  rating=3.8),
        Location(id=gen_id(), route_key='delhi_jaipur', name='SMS Hospital Jaipur',         category='emergency',    distance_from_route_km=1.5, city='Jaipur',    rating=4.2),
    ]

    for loc in locations:
        db.session.add(loc)
    db.session.commit()
    print(f"Seeded {len(locations)} locations into MySQL")
