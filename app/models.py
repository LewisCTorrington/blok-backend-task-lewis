from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    customer_name = db.Column(db.String(64))
    min_floor_number = db.Column(db.Integer)
    max_floor_number = db.Column(db.Integer)
    post_numbers = db.Column(db.String(64))
    min_area_living = db.Column(db.Float)

class Realty(db.Model):
    __tablename__ = 'realties'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    location_street_address = db.Column(db.String(64))
    location_specifier = db.Column(db.String(64))
    location_postcode = db.Column(db.String(64))
    area_living = db.Column(db.Float)
    floor_number = db.Column(db.Integer)