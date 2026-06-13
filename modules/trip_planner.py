from modules import data_layer as db
from modules.cost_engine import compute_full_cost

_BASE_ROUTES = {
    # ── HYDERABAD ──────────────────────────────────────────────────────────
    ('hyderabad','mumbai'):711,('hyderabad','bangalore'):570,
    ('hyderabad','chennai'):630,('hyderabad','delhi'):1500,
    ('hyderabad','pune'):559,('hyderabad','kolkata'):1500,
    ('hyderabad','nagpur'):500,('hyderabad','visakhapatnam'):620,
    ('hyderabad','warangal'):148,('hyderabad','tirupati'):550,
    ('hyderabad','kurnool'):215,('hyderabad','vijayawada'):275,
    ('hyderabad','ahmedabad'):1100,('hyderabad','bhopal'):900,
    ('hyderabad','nellore'):450,('hyderabad','ongole'):340,
    # ── MUMBAI ─────────────────────────────────────────────────────────────
    ('mumbai','delhi'):1415,('mumbai','bangalore'):984,
    ('mumbai','chennai'):1335,('mumbai','kolkata'):1982,
    ('mumbai','pune'):149,('mumbai','ahmedabad'):524,
    ('mumbai','goa'):597,('mumbai','nagpur'):837,
    ('mumbai','nashik'):185,('mumbai','aurangabad'):335,
    ('mumbai','surat'):284,('mumbai','vadodara'):397,
    ('mumbai','shirdi'):240,('mumbai','kolhapur'):380,
    # ── DELHI ──────────────────────────────────────────────────────────────
    ('delhi','bangalore'):2150,('delhi','chennai'):2200,
    ('delhi','kolkata'):1470,('delhi','jaipur'):268,
    ('delhi','agra'):200,('delhi','chandigarh'):245,
    ('delhi','amritsar'):450,('delhi','varanasi'):810,
    ('delhi','lucknow'):555,('delhi','haridwar'):210,
    ('delhi','shimla'):343,('delhi','dehradun'):300,
    ('delhi','manali'):570,('delhi','rishikesh'):240,
    ('delhi','jammu'):586,('delhi','srinagar'):876,
    ('delhi','kota'):440,('delhi','udaipur'):665,
    ('delhi','jodhpur'):600,('delhi','mathura'):145,
    ('delhi','ajmer'):390,('delhi','bhopal'):770,
    ('delhi','indore'):960,('delhi','ahmedabad'):940,
    ('delhi','nainital'):310,('delhi','mussoorie'):290,
    ('delhi','dharamshala'):480,('delhi','pushkar'):405,
    ('delhi','bikaner'):480,('delhi','jaisalmer'):770,
    # ── BANGALORE ──────────────────────────────────────────────────────────
    ('bangalore','chennai'):350,('bangalore','mysore'):143,
    ('bangalore','coimbatore'):370,('bangalore','mangalore'):352,
    ('bangalore','goa'):560,('bangalore','ooty'):265,
    ('bangalore','madurai'):440,('bangalore','pondicherry'):314,
    ('bangalore','hubli'):414,('bangalore','belgaum'):502,
    ('bangalore','hampi'):365,('bangalore','coorg'):255,
    ('bangalore','hassan'):180,('bangalore','kochi'):536,
    ('bangalore','trichy'):460,('bangalore','salem'):340,
    ('bangalore','vellore'):210,('bangalore','tirupati'):250,
    # ── CHENNAI ────────────────────────────────────────────────────────────
    ('chennai','coimbatore'):500,('chennai','madurai'):460,
    ('chennai','pondicherry'):161,('chennai','tirupati'):140,
    ('chennai','vellore'):145,('chennai','salem'):340,
    ('chennai','trichy'):335,('chennai','kochi'):680,
    ('chennai','kolkata'):1675,('chennai','visakhapatnam'):790,
    ('chennai','ooty'):560,('chennai','rameshwaram'):570,
    # ── KOLKATA ────────────────────────────────────────────────────────────
    ('kolkata','bhubaneswar'):440,('kolkata','patna'):580,
    ('kolkata','guwahati'):1000,('kolkata','siliguri'):600,
    ('kolkata','varanasi'):680,('kolkata','ranchi'):410,
    ('kolkata','dhanbad'):290,('kolkata','puri'):500,
    ('kolkata','jamshedpur'):270,('kolkata','cuttack'):460,
    # ── RAJASTHAN ──────────────────────────────────────────────────────────
    ('jaipur','udaipur'):395,('jaipur','jodhpur'):340,
    ('jaipur','ajmer'):132,('jaipur','bikaner'):330,
    ('jaipur','kota'):250,('jaipur','pushkar'):145,
    ('jaipur','jaisalmer'):575,('jaipur','ahmedabad'):540,
    ('jaipur','agra'):235,('jaipur','mount abu'):490,
    ('jaipur','alwar'):155,('jaipur','bharatpur'):185,
    ('udaipur','jodhpur'):250,('udaipur','jaisalmer'):490,
    ('udaipur','mount abu'):170,('udaipur','ahmedabad'):255,
    ('jodhpur','jaisalmer'):285,('jodhpur','bikaner'):240,
    ('jodhpur','ajmer'):200,('jodhpur','mount abu'):185,
    # ── GUJARAT ────────────────────────────────────────────────────────────
    ('ahmedabad','surat'):264,('ahmedabad','vadodara'):109,
    ('ahmedabad','rajkot'):216,('ahmedabad','jamnagar'):298,
    ('ahmedabad','bhavnagar'):200,('ahmedabad','gandhinagar'):25,
    ('ahmedabad','somnath'):390,('ahmedabad','dwarka'):440,
    ('rajkot','jamnagar'):88,('rajkot','somnath'):200,
    ('somnath','dwarka'):235,('vadodara','surat'):150,
    ('vadodara','rajkot'):225,
    # ── MAHARASHTRA ────────────────────────────────────────────────────────
    ('pune','nashik'):210,('pune','aurangabad'):235,
    ('pune','kolhapur'):230,('pune','nagpur'):715,
    ('pune','solapur'):255,('pune','shirdi'):185,
    ('aurangabad','ajanta'):100,('aurangabad','ellora'):30,
    ('nashik','shirdi'):88,('nagpur','amravati'):155,
    ('nagpur','jabalpur'):275,('nagpur','raipur'):295,
    # ── UTTAR PRADESH ──────────────────────────────────────────────────────
    ('lucknow','varanasi'):286,('lucknow','agra'):370,
    ('lucknow','kanpur'):85,('lucknow','prayagraj'):200,
    ('lucknow','gorakhpur'):265,('lucknow','allahabad'):200,
    ('varanasi','prayagraj'):125,('varanasi','gorakhpur'):226,
    ('agra','mathura'):55,('agra','fatehpur sikri'):38,
    ('kanpur','prayagraj'):200,('prayagraj','varanasi'):125,
    # ── SOUTH INDIA ────────────────────────────────────────────────────────
    ('kochi','thiruvananthapuram'):205,('kochi','calicut'):190,
    ('kochi','munnar'):130,('kochi','thekkady'):200,
    ('kochi','thrissur'):75,('kochi','alleppey'):55,
    ('thiruvananthapuram','kanyakumari'):90,
    ('thiruvananthapuram','madurai'):240,
    ('madurai','rameshwaram'):175,('madurai','munnar'):155,
    ('madurai','coimbatore'):213,('madurai','kanyakumari'):246,
    ('coimbatore','ooty'):90,('coimbatore','munnar'):150,
    ('coimbatore','salem'):160,('trichy','madurai'):135,
    ('trichy','thanjavur'):55,('pondicherry','bangalore'):314,
    ('mangalore','goa'):361,('mangalore','bangalore'):352,
    ('mangalore','calicut'):130,('calicut','bangalore'):420,
    ('mysore','ooty'):120,('mysore','coorg'):118,
    ('coorg','mangalore'):160,('ooty','coimbatore'):90,
    ('hassan','bangalore'):180,('hassan','mysore'):120,
    ('hubli','goa'):185,('belgaum','goa'):120,
    ('hampi','hubli'):135,('hampi','bangalore'):365,
    ('udupi','mangalore'):58,('udupi','goa'):250,
    # ── NORTHEAST & EAST ───────────────────────────────────────────────────
    ('guwahati','shillong'):100,('guwahati','jorhat'):300,
    ('guwahati','kaziranga'):190,('guwahati','silchar'):420,
    ('guwahati','tezpur'):175,('guwahati','dibrugarh'):440,
    ('bhubaneswar','puri'):60,('bhubaneswar','cuttack'):28,
    ('bhubaneswar','konark'):65,('bhubaneswar','rourkela'):335,
    ('patna','gaya'):110,('patna','varanasi'):285,
    ('ranchi','jamshedpur'):130,('ranchi','dhanbad'):170,
    ('ranchi','bokaro'):100,
    # ── HIMACHAL & UTTARAKHAND ─────────────────────────────────────────────
    ('shimla','manali'):270,('shimla','chandigarh'):115,
    ('shimla','dharamshala'):248,('shimla','kullu'):210,
    ('manali','dharamshala'):230,('manali','kullu'):40,
    ('dharamshala','amritsar'):230,('dharamshala','chandigarh'):240,
    ('dehradun','haridwar'):52,('dehradun','rishikesh'):42,
    ('dehradun','mussoorie'):35,('dehradun','nainital'):150,
    ('rishikesh','haridwar'):20,('haridwar','nainital'):280,
    ('nainital','delhi'):310,('mussoorie','haridwar'):90,
    # ── PUNJAB & HARYANA ───────────────────────────────────────────────────
    ('amritsar','ludhiana'):140,('amritsar','chandigarh'):230,
    ('amritsar','jalandhar'):80,('amritsar','pathankot'):120,
    ('ludhiana','chandigarh'):97,('ludhiana','jalandhar'):60,
    ('chandigarh','delhi'):245,('chandigarh','shimla'):115,
    # ── JAMMU & KASHMIR ────────────────────────────────────────────────────
    ('jammu','srinagar'):290,('jammu','delhi'):586,
    ('jammu','pathankot'):95,
    ('srinagar','gulmarg'):50,('srinagar','pahalgam'):95,
    ('srinagar','sonmarg'):80,('srinagar','leh'):430,
    # ── MADHYA PRADESH ─────────────────────────────────────────────────────
    ('bhopal','indore'):190,('bhopal','jabalpur'):290,
    ('bhopal','ujjain'):183,('bhopal','gwalior'):415,
    ('bhopal','panchmarhi'):195,
    ('indore','ujjain'):56,('indore','kota'):320,
    ('indore','ahmedabad'):430,
    ('jabalpur','khajuraho'):255,('jabalpur','pench'):190,
    # ── GOA ────────────────────────────────────────────────────────────────
    ('goa','bangalore'):560,('goa','pune'):455,
    ('goa','mangalore'):361,('goa','mumbai'):597,
    # ── ANDHRA & TELANGANA ─────────────────────────────────────────────────
    ('visakhapatnam','vijayawada'):350,
    ('visakhapatnam','hyderabad'):620,
    ('visakhapatnam','bhubaneswar'):450,
    ('vijayawada','chennai'):430,('vijayawada','bangalore'):530,
    ('tirupati','chennai'):140,('tirupati','bangalore'):250,
    ('tirupati','hyderabad'):550,
    ('nellore','chennai'):175,('nellore','hyderabad'):450,
    # ── ODISHA ─────────────────────────────────────────────────────────────
    ('bhubaneswar','puri'):60,('bhubaneswar','konark'):65,
    ('bhubaneswar','cuttack'):28,
    # ── CHHATTISGARH ───────────────────────────────────────────────────────
    ('raipur','nagpur'):295,('raipur','bhopal'):450,
    ('raipur','jabalpur'):310,
}

# Auto bidirectional
ROUTES = {}
for (a, b), d in _BASE_ROUTES.items():
    ROUTES[(a, b)] = d
    ROUTES[(b, a)] = d

AVG_SPEED = 60

def _norm(c):
    return c.strip().lower()

def estimate_distance(src, dst):
    return float(ROUTES.get((_norm(src), _norm(dst)), 600))

def estimate_duration(dist):
    return round(dist / AVG_SPEED, 1)

def get_all_cities():
    return sorted(set(c.title() for pair in ROUTES.keys() for c in pair))

def plan_trip(uid, form):
    src = form.get('source', '').strip()
    dst = form.get('destination', '').strip()
    try:
        mileage    = float(form['vehicle_mileage'])
        fuel_price = float(form['fuel_price'])
        days       = int(form['travel_days'])
        band       = form['accommodation_budget']
    except (KeyError, ValueError):
        return False, 'Invalid form data. Please check all fields.', {}
    if not src or not dst:
        return False, 'Source and destination are required.', {}
    if src.lower() == dst.lower():
        return False, 'Source and destination cannot be the same city.', {}
    if mileage <= 0 or fuel_price <= 0:
        return False, 'Mileage and fuel price must be positive.', {}
    if days < 1:
        return False, 'Travel days must be at least 1.', {}
    if band not in ('budget', 'mid', 'premium', 'luxury'):
        return False, 'Invalid budget band.', {}

    dist  = estimate_distance(src, dst)
    dur   = estimate_duration(dist)
    costs = compute_full_cost(dist, mileage, fuel_price, band, days)

    trip = db.create_trip(uid, {
        'source': src.title(), 'destination': dst.title(),
        'distance_km': dist, 'travel_days': days,
        'vehicle_mileage': mileage, 'fuel_price': fuel_price,
        'accommodation_budget': band, 'estimated_duration_hours': dur,
    })
    db.create_trip_cost(trip['id'], uid, costs)
    return True, 'Trip planned successfully!', {'trip': trip, 'costs': costs}
