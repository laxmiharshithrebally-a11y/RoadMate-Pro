from modules import data_layer as db

def get_packing_list(travel_days, accommodation_budget):
    base = [
        {'item': 'Valid ID / Aadhaar Card', 'category': 'Documents',   'packed': False},
        {'item': 'Driving Licence',          'category': 'Documents',   'packed': False},
        {'item': 'Vehicle RC & Insurance',   'category': 'Documents',   'packed': False},
        {'item': 'Cash (emergency)',         'category': 'Finance',     'packed': False},
        {'item': 'Credit / Debit Card',      'category': 'Finance',     'packed': False},
        {'item': 'Phone Charger',            'category': 'Electronics', 'packed': False},
        {'item': 'Power Bank',               'category': 'Electronics', 'packed': False},
        {'item': 'First Aid Kit',            'category': 'Safety',      'packed': False},
        {'item': 'Sunglasses',               'category': 'Personal',    'packed': False},
        {'item': 'Water Bottle (2L)',         'category': 'Food',        'packed': False},
        {'item': 'Snacks / Dry Fruits',      'category': 'Food',        'packed': False},
    ]
    if travel_days >= 2:
        base += [
            {'item': f'Clothes ({travel_days} sets)', 'category': 'Clothing',   'packed': False},
            {'item': 'Toothbrush & Paste',            'category': 'Toiletries', 'packed': False},
            {'item': 'Soap / Shower Gel',             'category': 'Toiletries', 'packed': False},
            {'item': 'Deodorant',                     'category': 'Toiletries', 'packed': False},
        ]
    if travel_days >= 4:
        base += [
            {'item': 'Travel Pillow', 'category': 'Comfort', 'packed': False},
            {'item': 'Eye Mask',      'category': 'Comfort', 'packed': False},
        ]
    if accommodation_budget in ('premium', 'luxury'):
        base += [
            {'item': 'Formal Outfit', 'category': 'Clothing', 'packed': False},
        ]
    return base


def save_notes(trip_id, uid, notes_text):
    result = db.update_trip(trip_id, uid, {'notes': notes_text.strip()})
    return (True, 'Notes saved.') if result else (False, 'Trip not found.')
