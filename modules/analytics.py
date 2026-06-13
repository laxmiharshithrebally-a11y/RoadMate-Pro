"""
Analytics Module — RoadMate Pro
Generates chart data, spending summaries, city stats, carbon footprint.
"""
from collections import defaultdict
from datetime import datetime


# Average CO2 emission per litre of petrol (kg)
CO2_PER_LITRE = 2.31


def get_spending_by_category(trips_with_costs):
    """Returns data for pie chart: fuel / toll / accommodation breakdown."""
    fuel  = sum(t['costs']['fuel_cost']          for t in trips_with_costs if t.get('costs'))
    toll  = sum(t['costs']['toll_cost']           for t in trips_with_costs if t.get('costs'))
    hotel = sum(t['costs']['accommodation_cost']  for t in trips_with_costs if t.get('costs'))
    total = fuel + toll + hotel or 1
    return {
        'cats':   ['Fuel', 'Tolls', 'Accommodation'],
        'amounts': [round(fuel, 2), round(toll, 2), round(hotel, 2)],
        'pcts': [
            round(fuel  / total * 100, 1),
            round(toll  / total * 100, 1),
            round(hotel / total * 100, 1),
        ],
        'colors': ['#1a73e8', '#e53935', '#f9a825'],
        'total':  round(total, 2),
    }


def get_monthly_spending(trips_with_costs):
    """Returns bar chart data: spending per month."""
    monthly = defaultdict(float)
    for t in trips_with_costs:
        if not t.get('costs'):
            continue
        try:
            month = datetime.fromisoformat(t['created_at']).strftime('%b %Y')
            monthly[month] += t['costs']['total_cost']
        except Exception:
            pass
    sorted_months = sorted(monthly.keys(),
                           key=lambda m: datetime.strptime(m, '%b %Y'))
    return {
        'months': sorted_months,
        'amounts': [round(monthly[m], 2) for m in sorted_months],
    }


def get_city_stats(trips_with_costs):
    """Returns most visited cities and most expensive routes."""
    city_count = defaultdict(int)
    route_cost = {}
    for t in trips_with_costs:
        city_count[t['source']]      += 1
        city_count[t['destination']] += 1
        key = f"{t['source']} → {t['destination']}"
        if t.get('costs'):
            route_cost[key] = t['costs']['total_cost']

    top_cities = sorted(city_count.items(), key=lambda x: x[1], reverse=True)[:5]
    top_routes = sorted(route_cost.items(),  key=lambda x: x[1], reverse=True)[:5]
    return {
        'top_cities': [{'city': c, 'count': n} for c, n in top_cities],
        'top_routes': [{'route': r, 'cost': round(v, 0)} for r, v in top_routes],
    }


def get_cost_trend(trips_with_costs):
    """Returns line chart data: total cost per trip over time."""
    sorted_trips = sorted(
        [t for t in trips_with_costs if t.get('costs')],
        key=lambda t: t['created_at']
    )
    return {
        'routes': [f"{t['source']}→{t['destination']}" for t in sorted_trips],
        'amounts': [t['costs']['total_cost'] for t in sorted_trips],
        'dates':  [t['created_at'][:10] for t in sorted_trips],
    }


def get_carbon_footprint(trips_with_costs):
    """Estimates CO2 emissions per trip."""
    results = []
    total_co2 = 0
    for t in trips_with_costs:
        if not t.get('costs'):
            continue
        litres = t['costs']['fuel_required_liters']
        co2    = round(litres * CO2_PER_LITRE, 2)
        total_co2 += co2
        results.append({
            'route':   f"{t['source']} → {t['destination']}",
            'litres':  litres,
            'co2_kg':  co2,
            'trees':   round(co2 / 21.7, 1),   # avg tree absorbs 21.7 kg CO2/year
        })
    results.sort(key=lambda x: x['co2_kg'], reverse=True)
    return {
        'trips':        results,
        'total_co2_kg': round(total_co2, 2),
        'total_trees':  round(total_co2 / 21.7, 1),
    }


def get_full_summary(trips_with_costs):
    """Master function — returns all analytics in one call."""
    if not trips_with_costs:
        return None
    return {
        'spending_by_category': get_spending_by_category(trips_with_costs),
        'monthly_spending':     get_monthly_spending(trips_with_costs),
        'city_stats':           get_city_stats(trips_with_costs),
        'cost_trend':           get_cost_trend(trips_with_costs),
        'carbon':               get_carbon_footprint(trips_with_costs),
        'totals': {
            'trips':    len(trips_with_costs),
            'spent':    round(sum(t['costs']['total_cost'] for t in trips_with_costs if t.get('costs')), 2),
            'km':       round(sum(t['distance_km'] for t in trips_with_costs), 1),
            'fuel_l':   round(sum(t['costs']['fuel_required_liters'] for t in trips_with_costs if t.get('costs')), 2),
            'avg_cost': round(
                sum(t['costs']['total_cost'] for t in trips_with_costs if t.get('costs'))
                / max(len(trips_with_costs), 1), 2
            ),
        },
    }
