import os
import secrets

class Config:
    # ── SECRET KEY ────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    # ── MYSQL DATABASE ────────────────────────────────────────────────────
    # Change these if your MySQL password is different
    MYSQL_HOST     = os.environ.get('MYSQL_HOST',     'localhost')
    MYSQL_PORT     = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER     = os.environ.get('MYSQL_USER',     'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Lucky@123')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'roadmate')

    from urllib.parse import quote_plus
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── BUDGET BANDS ──────────────────────────────────────────────────────
    BUDGET_BANDS = {
        'budget':  (500,   1500),
        'mid':     (1500,  4000),
        'premium': (4000,  10000),
        'luxury':  (10000, 99999),
    }
