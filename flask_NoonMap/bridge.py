# coding: utf-8
from sqlalchemy import Column, Float, Integer, Table, Text
from flask_sqlalchemy import SQLAlchemy

# flask-sqlacodegen "sqlite:///bridge.db" --flask > bridge.py

db = SQLAlchemy()


class Bridge(db.Model):
    __tablename__ = 'BRIDGE'
    bridge_name = db.Column(db.Text)
    address = db.Column(db.Text)
    etc_address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    brid_height_origin = db.Column(db.Float)
    location_start = db.Column(db.Text, primary_key=True)
    wl_station_code = db.Column(db.Integer)
    station_name = db.Column(db.Text)
    location = db.Column(db.Text)
    obs_date = db.Column(db.Text)
    WL = db.Column(db.Float)
    bridge_height = db.Column(db.Float)

# t_BRIDGE = db.Table(
#     'BRIDGE',
#     db.Column('bridge_name', db.Text),
#     db.Column('address', db.Text),
#     db.Column('etc_address', db.Text),
#     db.Column('latitude', db.Float),
#     db.Column('longitude', db.Float),
#     db.Column('brid_height_origin', db.Float),
#     db.Column('location_start', db.Text),
#     db.Column('wl_station_code', db.Integer),
#     db.Column('station_name', db.Text),
#     db.Column('location', db.Text),
#     db.Column('obs_date', db.Text),
#     db.Column('WL', db.Float),
#     db.Column('bridge_height', db.Float)
# )
