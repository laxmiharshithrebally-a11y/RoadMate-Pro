"""
auth.py — RoadMate Pro Phase 1
Authentication using MySQL via data_layer.
"""
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from modules import data_layer as db


def _valid_email(e):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', e))


def _valid_pw(p):
    if len(p) < 8:
        return False, 'Password must be at least 8 characters.'
    if not re.search(r'\d', p):
        return False, 'Password must contain at least one digit.'
    return True, ''


def register_user(username, email, password, full_name):
    username  = username.strip()
    email     = email.strip()
    full_name = full_name.strip()
    if not all([username, email, password, full_name]):
        return False, 'All fields are required.', {}
    if not _valid_email(email):
        return False, 'Invalid email address.', {}
    ok, msg = _valid_pw(password)
    if not ok:
        return False, msg, {}
    if db.get_user_by_email(email):
        return False, 'Email already registered.', {}
    if db.get_user_by_username(username):
        return False, 'Username already taken.', {}
    pw_hash = generate_password_hash(password,
                                     method='pbkdf2:sha256', salt_length=16)
    user = db.create_user(username, email, pw_hash, full_name)
    return True, 'Account created successfully.', user


def login_user(email, password):
    user = db.get_user_by_email(email.strip())
    if not user:
        return False, 'Invalid email or password.', {}
    pw_hash = db.get_user_password_hash(user['id'])
    if not check_password_hash(pw_hash, password):
        return False, 'Invalid email or password.', {}
    session['user_id']  = user['id']
    session['username'] = user['username']
    return True, 'Login successful.', user


def logout_user():
    session.clear()


def get_current_user():
    if not session.get('user_id'):
        return None
    return db.get_user_by_id(session['user_id'])


def is_authenticated():
    return bool(session.get('user_id'))


def update_profile(uid, full_name, email):
    if not full_name.strip() or not email.strip():
        return False, 'Name and email are required.'
    if not _valid_email(email):
        return False, 'Invalid email address.'
    ex = db.get_user_by_email(email)
    if ex and ex['id'] != uid:
        return False, 'Email already in use by another account.'
    db.update_user(uid, {'full_name': full_name.strip(),
                         'email':     email.strip()})
    return True, 'Profile updated successfully.'


def change_password(uid, current_pw, new_pw):
    pw_hash = db.get_user_password_hash(uid)
    if not pw_hash or not check_password_hash(pw_hash, current_pw):
        return False, 'Current password is incorrect.'
    ok, msg = _valid_pw(new_pw)
    if not ok:
        return False, msg
    new_hash = generate_password_hash(new_pw,
                                      method='pbkdf2:sha256', salt_length=16)
    db.update_user(uid, {'password_hash': new_hash})
    return True, 'Password changed successfully.'
