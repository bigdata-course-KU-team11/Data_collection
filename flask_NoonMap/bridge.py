# coding: utf-8
from sqlalchemy import Column, Float, Integer, Table, Text
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# flask-sqlacodegen "sqlite:///bridge_db.db" --flask > bridge.py

t_BRIDGE = db.Table(
    'BRIDGE',
    db.Column('id', db.Integer),
    db.Column('bridge_name', db.Text),
    db.Column('address', db.Text),
    db.Column('etc_address', db.Text),
    db.Column('latitude', db.Float),
    db.Column('longitude', db.Float),
    db.Column('location_start', db.Text),
    db.Column('wl_station_code', db.Integer),
    db.Column('station_name', db.Text),
    db.Column('location', db.Text),
    db.Column('obs_date', db.Text),
    db.Column('WL', db.Float),
    db.Column('bridge_height', db.Float),
    db.Column('brid_height_origin', db.Float)
)
