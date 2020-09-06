import folium
# import os
import json
from flask import Flask, render_template, Markup, request
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from flask_dropzone import Dropzone
from flask_sqlalchemy import SQLAlchemy

#################################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///rain_msg.db"
app.config['SQLALCHEMY_BINDS'] = {   # multiple databases
    'rain': 'sqlite:///rain_msg.db',
    'bridge': 'sqlite:///bridge.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#################################################################
db = SQLAlchemy(app)
db.init_app(app)
# admin = Admin(name='test')  # sql alchemy와 연동 가능
# admin.init_app(app)
# Dropzone(app)
#
# basedir = os.path.abspath(os.path.dirname(__file__))
# upload = os.path.join(basedir, 'uploads')
#################################################################


class Bridge(db.Model):
    __tablename__ = 'BRIDGE'
    __bind_key__ = 'bridge'  # multiple db의 bind key
    bridge_name = db.Column(db.Text)
    address = db.Column(db.Text)
    etc_address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    brid_height_origin = db.Column(db.Float)
    location_start = db.Column(db.Text)
    wl_station_code = db.Column(db.Integer)
    station_name = db.Column(db.Text)
    location = db.Column(db.Text, primary_key=True)
    obs_date = db.Column(db.Text)
    WL = db.Column(db.Float)
    bridge_height = db.Column(db.Float)


class Rain_msg(db.Model):
    # db.Model을 상속받으면 db.Column()메소드 사용 가능
    __tablename__ = 'RAIN_MSG'
    __bind_key__ = 'rain'  # multiple db의 bind key
    index = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.Text)
    location_id = db.Column(db.Text)
    location_name = db.Column(db.Text)
    md101_sn = db.Column(db.Text)
    msg = db.Column(db.Text)
#################################################################


# admin.add_view(ModelView(Rain_msg, db.session))
#################################################################


db.create_all()  # 테이블 생성
#################################################################


@app.route('/home')
@app.route('/')
def home():
    status = request.args.get('status', '0')
    print(status)
    #############################################################################
    rain = Rain_msg.query.all()  # (SELECT * FROM 테이블명)과 동일함
    bridge = Bridge.query.filter_by(address="경기도", bridge_name="한평교").all()
    #############################################################################
    start_coords = (37.5838699, 127.0565831)
    folium_map = folium.Map(location=start_coords, zoom_start=11, width='100%')

    #############################################################################
    with open('seoul_geo.json', mode='rt', encoding='utf-8') as f:
        geo_seoul = json.loads(f.read())
        f.close()

    folium.GeoJson(
        geo_seoul,
        name='seoul_geo'
    ).add_to(folium_map)

    #############################################################################
    _ = folium_map._repr_html_()

    # get definition of map in body
    map_div = Markup(folium_map.get_root().html.render())
    # html to be included in header
    hdr_txt = Markup(folium_map.get_root().header.render())
    # html to be included in <script>
    script_txt = Markup(folium_map.get_root().script.render())
    #############################################################################

    return render_template('index.html', status=status, map_div=map_div, hdr_txt=hdr_txt, script_txt=script_txt, result_rain=rain, result_brid=bridge)


if __name__ == '__main__':
    app.run()
