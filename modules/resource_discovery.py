from modules import data_layer as db
from config import Config

LABELS = {
    'fuel_station': 'Fuel Station',
    'hotel':        'Hotel / Accommodation',
    'emergency':    'Emergency Service',
    'rest_stop':    'Rest Stop',
}
ICONS = {
    'fuel_station': '⛽',
    'hotel':        '🏨',
    'emergency':    '🏥',
    'rest_stop':    '☕',
}

def discover_resources(src, dst, band=None):
    res = db.get_resources_for_route(src, dst)
    if band:
        lo, hi = Config.BUDGET_BANDS.get(band, (0, 99999))
        filtered = []
        for r in res:
            if r['category'] == 'hotel':
                if lo <= r.get('price_per_night', 0) <= hi:
                    filtered.append(r)
            else:
                filtered.append(r)
        res = filtered
    for r in res:
        r['category_label'] = LABELS.get(r['category'], r['category'])
        r['icon']           = ICONS.get(r['category'], '📍')
    grouped = {c: [] for c in LABELS}
    for r in res:
        if r.get('category') in grouped:
            grouped[r['category']].append(r)
    return {
        'all':     res,
        'grouped': grouped,
        'counts':  {c: len(v) for c, v in grouped.items()},
    }
