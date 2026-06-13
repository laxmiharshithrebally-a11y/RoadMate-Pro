"""
extensions.py — RoadMate Pro
Shared Flask extensions — created here to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
