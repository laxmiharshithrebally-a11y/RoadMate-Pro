from config import Config

def calculate_fuel(distance_km, mileage, fuel_price):
    req = round(distance_km / mileage, 2)
    return {'fuel_required_liters': req, 'fuel_cost': round(req * fuel_price, 2)}

def calculate_toll(distance_km):
    rate = 1.0 if distance_km <= 100 else 1.5 if distance_km <= 300 else 1.8
    return {'toll_cost': round(distance_km * rate, 2), 'toll_rate_per_km': rate}

def calculate_accommodation(band, days):
    lo, hi = Config.BUDGET_BANDS.get(band, (1500, 4000))
    avg = round((lo + hi) / 2, 2)
    nights = max(days - 1, 0)
    return {
        'accommodation_cost': round(avg * nights, 2),
        'nights': nights,
        'avg_price_per_night': avg,
        'budget_band': band
    }

def compute_full_cost(distance_km, mileage, fuel_price, band, days):
    f = calculate_fuel(distance_km, mileage, fuel_price)
    t = calculate_toll(distance_km)
    a = calculate_accommodation(band, days)
    total = round(f['fuel_cost'] + t['toll_cost'] + a['accommodation_cost'], 2)
    return {
        **f, **t, **a,
        'total_cost': total,
        'cost_per_km': round(total / distance_km, 2) if distance_km else 0
    }
