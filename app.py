import os
from functools import wraps
from flask import (Flask, render_template, request, redirect,
                   url_for, session, jsonify, flash, send_file)

from config    import Config
from extensions import db
from models    import User, Trip, TripCost, Location

from modules import auth
from modules import data_layer as dbl
from modules.trip_planner       import plan_trip, get_all_cities
from modules.resource_discovery import discover_resources
from modules.report_generator   import generate_report
from modules.pdf_generator      import generate_pdf
from modules.weather             import get_weather
from modules.analytics          import get_full_summary
from modules.excel_export       import generate_excel, HAS_OPENPYXL
from modules.admin              import is_admin, get_admin_stats
from modules.trip_notes         import get_packing_list, save_notes

app = Flask(__name__)
app.config.from_object(Config)

# ── INIT DATABASE ─────────────────────────────────────────────────────────
db.init_app(app)

with app.app_context():
    db.create_all()          # creates all tables if they don't exist
    dbl.seed_locations()     # seeds location data if table is empty
    print("MySQL connected and tables ready!")

# ── DECORATORS ────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*a, **kw):
        if not auth.is_authenticated():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*a, **kw)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*a, **kw):
        user = auth.get_current_user()
        if not user or not is_admin(user):
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*a, **kw)
    return decorated


@app.context_processor
def inject_globals():
    user = auth.get_current_user()
    if user:
        session['is_admin'] = is_admin(user)
    return {}


# ── PUBLIC ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if auth.is_authenticated():
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if auth.is_authenticated():
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        ok, msg, user = auth.register_user(
            request.form.get('username', ''),
            request.form.get('email', ''),
            request.form.get('password', ''),
            request.form.get('full_name', ''),
        )
        flash(msg, 'success' if ok else 'danger')
        if ok:
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if auth.is_authenticated():
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        ok, msg, user = auth.login_user(
            request.form.get('email', ''),
            request.form.get('password', ''),
        )
        if ok:
            return redirect(url_for('dashboard'))
        flash(msg, 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    auth.logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


# ── DASHBOARD ─────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    user  = auth.get_current_user()
    trips = dbl.get_trips_by_user(user['id'])
    for t in trips:
        t['costs'] = dbl.get_cost_by_trip(t['id'])
    total_spent = sum(t['costs']['total_cost']
                      for t in trips if t.get('costs'))
    total_km    = sum(t['distance_km'] for t in trips)
    return render_template('dashboard.html', user=user, trips=trips,
                           total_trips=len(trips),
                           total_spent=total_spent,
                           total_km=total_km)


# ── PLAN TRIP ─────────────────────────────────────────────────────────────
@app.route('/plan-trip', methods=['GET', 'POST'])
@login_required
def plan_trip_route():
    user   = auth.get_current_user()
    cities = get_all_cities()
    if request.method == 'POST':
        ok, msg, result = plan_trip(user['id'], request.form)
        flash(msg, 'success' if ok else 'danger')
        if ok:
            return redirect(url_for('trip_detail',
                                    trip_id=result['trip']['id']))
    return render_template('plan_trip.html', user=user,
                           budget_bands=Config.BUDGET_BANDS, cities=cities)


# ── TRIP DETAIL ───────────────────────────────────────────────────────────
@app.route('/trip/<trip_id>')
@login_required
def trip_detail(trip_id):
    user = auth.get_current_user()
    trip = dbl.get_trip_by_id(trip_id)
    if not trip or trip['user_id'] != user['id']:
        flash('Trip not found.', 'danger')
        return redirect(url_for('dashboard'))
    costs     = dbl.get_cost_by_trip(trip_id)
    resources = discover_resources(trip['source'], trip['destination'],
                                   trip['accommodation_budget'])
    report    = generate_report(trip_id, user['id'])
    return render_template('trip_detail.html', user=user, trip=trip,
                           costs=costs, resources=resources, report=report)


# ── TRIP NOTES ────────────────────────────────────────────────────────────
@app.route('/trip/<trip_id>/notes', methods=['GET'])
@login_required
def trip_notes_page(trip_id):
    user = auth.get_current_user()
    trip = dbl.get_trip_by_id(trip_id)
    if not trip or trip['user_id'] != user['id']:
        flash('Trip not found.', 'danger')
        return redirect(url_for('dashboard'))
    checklist = get_packing_list(trip['travel_days'],
                                 trip['accommodation_budget'])
    return render_template('trip_notes.html', user=user,
                           trip=trip, checklist=checklist)


@app.route('/trip/<trip_id>/notes', methods=['POST'])
@login_required
def save_trip_notes(trip_id):
    user      = auth.get_current_user()
    notes_txt = request.form.get('notes', '')
    ok, msg   = save_notes(trip_id, user['id'], notes_txt)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('trip_notes_page', trip_id=trip_id))


# ── DELETE TRIP ───────────────────────────────────────────────────────────
@app.route('/trip/<trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    user = auth.get_current_user()
    ok   = dbl.delete_trip(trip_id, user['id'])
    flash('Trip deleted.' if ok else 'Trip not found.',
          'success' if ok else 'danger')
    return redirect(url_for('dashboard'))


# ── PDF ───────────────────────────────────────────────────────────────────
@app.route('/trip/<trip_id>/pdf')
@login_required
def download_pdf(trip_id):
    user = auth.get_current_user()
    trip = dbl.get_trip_by_id(trip_id)
    if not trip or trip['user_id'] != user['id']:
        flash('Trip not found.', 'danger')
        return redirect(url_for('dashboard'))
    costs     = dbl.get_cost_by_trip(trip_id)
    resources = discover_resources(trip['source'], trip['destination'],
                                   trip['accommodation_budget'])
    buffer   = generate_pdf(trip, costs, user, resources)
    filename = (f"RoadMate_{trip['source']}_"
                f"{trip['destination']}_{trip_id[:6]}.pdf")
    return send_file(buffer, as_attachment=True,
                     download_name=filename,
                     mimetype='application/pdf')


# ── COMPARE ───────────────────────────────────────────────────────────────
@app.route('/compare')
@login_required
def compare_trips():
    user  = auth.get_current_user()
    trips = dbl.get_trips_by_user(user['id'])
    for t in trips:
        t['costs'] = dbl.get_cost_by_trip(t['id'])
    t1_id = request.args.get('t1')
    t2_id = request.args.get('t2')
    trip1 = next((t for t in trips if t['id'] == t1_id), None)
    trip2 = next((t for t in trips if t['id'] == t2_id), None)
    return render_template('compare.html', user=user, trips=trips,
                           trip1=trip1, trip2=trip2)


# ── ANALYTICS ─────────────────────────────────────────────────────────────
@app.route('/analytics')
@login_required
def analytics_page():
    user  = auth.get_current_user()
    trips = dbl.get_trips_by_user(user['id'])
    for t in trips:
        t['costs'] = dbl.get_cost_by_trip(t['id'])
    analytics = get_full_summary(trips) if trips else None
    return render_template('analytics.html', user=user, analytics=analytics)


# ── EXCEL EXPORT ──────────────────────────────────────────────────────────
@app.route('/export/excel')
@login_required
def export_excel():
    user  = auth.get_current_user()
    trips = dbl.get_trips_by_user(user['id'])
    for t in trips:
        t['costs'] = dbl.get_cost_by_trip(t['id'])
    if not trips:
        flash('No trips to export.', 'warning')
        return redirect(url_for('dashboard'))
    buffer, err = generate_excel(trips, user)
    if err:
        flash(f'Excel error: {err}', 'danger')
        return redirect(url_for('analytics_page'))
    fname = f"RoadMate_Trips_{user['username']}.xlsx"
    return send_file(buffer, as_attachment=True,
                     download_name=fname,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# ── ADMIN ─────────────────────────────────────────────────────────────────
@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    stats = get_admin_stats()
    return render_template('admin.html', stats=stats)


# ── PROFILE ───────────────────────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = auth.get_current_user()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            ok, msg = auth.update_profile(
                user['id'],
                request.form.get('full_name', ''),
                request.form.get('email', ''))
        elif action == 'change_password':
            ok, msg = auth.change_password(
                user['id'],
                request.form.get('current_password', ''),
                request.form.get('new_password', ''))
        elif action == 'delete_account':
            for t in dbl.get_trips_by_user(user['id']):
                dbl.delete_trip(t['id'], user['id'])
            from models import User as UserModel
            u = UserModel.query.filter_by(id=user['id']).first()
            if u:
                db.session.delete(u)
                db.session.commit()
            auth.logout_user()
            flash('Account deleted.', 'info')
            return redirect(url_for('index'))
        else:
            ok, msg = False, 'Unknown action.'
        flash(msg, 'success' if ok else 'danger')
        return redirect(url_for('profile'))
    trips = dbl.get_trips_by_user(user['id'])
    return render_template('profile.html', user=user,
                           trip_count=len(trips))


# ── API ───────────────────────────────────────────────────────────────────
@app.route('/api/cities')
def api_cities():
    return jsonify({'cities': get_all_cities()})


@app.route('/api/weather')
@login_required
def api_weather():
    city = request.args.get('city', 'Hyderabad')
    return jsonify(get_weather(city))


@app.route('/api/report/<trip_id>')
@login_required
def api_report(trip_id):
    user   = auth.get_current_user()
    report = generate_report(trip_id, user['id'])
    return jsonify(report) if report else (jsonify({'error': 'Not found'}), 404)


@app.route('/api/trips')
@login_required
def api_trips():
    user  = auth.get_current_user()
    trips = dbl.get_trips_by_user(user['id'])
    for t in trips:
        t['costs'] = dbl.get_cost_by_trip(t['id'])
    return jsonify({'trips': trips, 'count': len(trips)})


# ── ERRORS ───────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404


# ── TEMPLATE FILTERS ──────────────────────────────────────────────────────
@app.template_filter('enumerate')
def do_enumerate(iterable):
    return enumerate(iterable)


@app.template_filter('unique')
def do_unique(iterable):
    seen, result = set(), []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
