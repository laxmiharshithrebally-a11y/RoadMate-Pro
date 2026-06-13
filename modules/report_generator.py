from datetime import datetime
from modules import data_layer as db


def generate_report(trip_id, uid):
    trip  = db.get_trip_by_id(trip_id)
    costs = db.get_cost_by_trip(trip_id)
    user  = db.get_user_by_id(uid)
    if not trip or not costs or not user:
        return None
    return {
        'report_id':    f"RPT-{trip_id[:8].upper()}",
        'trip_id':      trip_id,
        'traveler':     user['full_name'],
        'generated_at': datetime.utcnow().isoformat(),
        'route':        f"{trip['source']} → {trip['destination']}",
        'distance_km':  trip['distance_km'],
        'total_cost':   costs['total_cost'],
        'fuel_cost':    costs['fuel_cost'],
        'toll_cost':    costs['toll_cost'],
        'hotel_cost':   costs['accommodation_cost'],
    }
