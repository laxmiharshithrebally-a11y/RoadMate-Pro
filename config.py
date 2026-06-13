import os
import secrets

class Config:
    # ── SECRET KEY ────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    SQLALCHEMY_DATABASE_URI = "sqlite:///roadmate.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── BUDGET BANDS ──────────────────────────────────────────────────────
    BUDGET_BANDS = {
        'budget':  (500,   1500),
        'mid':     (1500,  4000),
        'premium': (4000,  10000),
        'luxury':  (10000, 99999),
    }