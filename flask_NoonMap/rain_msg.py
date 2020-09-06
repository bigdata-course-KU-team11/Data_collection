# coding: utf-8
from sqlalchemy import Column, Integer, Table, Text
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



t_RAIN_MSG = db.Table(
    'RAIN_MSG',
    db.Column('index', db.Integer),
    db.Column('create_date', db.Text),
    db.Column('location_id', db.Text),
    db.Column('location_name', db.Text),
    db.Column('md101_sn', db.Text),
    db.Column('msg', db.Text)
)
