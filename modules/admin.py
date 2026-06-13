"""
admin.py — RoadMate Pro Phase 1
Admin panel — now uses MySQL via data_layer.
"""
from modules import data_layer as db
from collections import defaultdict, Counter

ADMIN_USERNAME = 'admin'


def is_admin(user):
    return user and user.get('username', '').lower() == ADMIN_USERNAME


def get_admin_stats():
    users    = db.get_all_users()
    trips    = db.get_all_trips()
    user_map = {u['id']: u for u in users}

    total_revenue = 0
    total_km      = sum(t['distance_km'] for t in trips)
    total_fuel    = 0

    for t in trips:
        c = db.get_cost_by_trip(t['id'])
        t['costs'] = c
        t['user']  = user_map.get(t['user_id'], {})
        if c:
            total_revenue += c['total_cost']
            total_fuel    += c.get('fuel_required_liters', 0)

    trip_counts = Counter(t['user_id'] for t in trips)
    top_users = sorted(
        [{'user': user_map.get(uid, {}), 'trip_count': cnt}
         for uid, cnt in trip_counts.items()],
        key=lambda x: x['trip_count'], reverse=True)[:10]

    recent_trips  = sorted(trips, key=lambda t: t['created_at'],
                            reverse=True)[:10]

    route_count = defaultdict(int)
    for t in trips:
        route_count[f"{t['source']} → {t['destination']}"] += 1
    popular_routes = sorted(route_count.items(),
                            key=lambda x: x[1], reverse=True)[:10]

    return {
        'total_users':    len(users),
        'total_trips':    len(trips),
        'total_revenue':  round(total_revenue, 2),
        'total_km':       round(total_km, 1),
        'total_fuel_l':   round(total_fuel, 2),
        'avg_trip_cost':  round(total_revenue / max(len(trips), 1), 2),
        'top_users':      top_users,
        'recent_trips':   recent_trips,
        'popular_routes': [{'route': r, 'count': c}
                           for r, c in popular_routes],
        'all_users':      users,
    }
