import folium
import json
from flask import Flask, render_template, Markup, request
from flask_sqlalchemy import SQLAlchemy
from folium.plugins import MarkerCluster
# import bridge
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bridge.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# bridge.db.init_app(app)

app = Flask(__name__)  # bridge.db, rain_msg.db 연동
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bridge.db"
app.config['SQLALCHEMY_BINDS'] = {   # multiple databases
    'bridge_key': 'sqlite:///bridge.db',
    'rain_key': 'sqlite:///rain_msg.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#################################################################
db = SQLAlchemy(app)
# db.init_app(app)
#################################################################


class Bridge(db.Model):
    __tablename__ = 'BRIDGE'
    __bind_key__ = 'bridge_key'  # multiple db의 bind key
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


class Rain_msg(db.Model):
    # db.Model을 상속받으면 db.Column()메소드 사용 가능
    __tablename__ = 'RAIN_MSG'
    __bind_key__ = 'rain_key'  # multiple db의 bind key
    index = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.Text)
    location_id = db.Column(db.Text)
    location_name = db.Column(db.Text)
    md101_sn = db.Column(db.Text)
    msg = db.Column(db.Text)
#################################################################


db.create_all(bind='bridge_key')  # 테이블 생성
db.create_all(bind='rain_key')
#################################################################


@app.route('/home')
@app.route('/')
def home():
    status = request.args.get('status', '0')
    print(status)
    #############################################################################
    rain = Rain_msg.query.all()  # (SELECT * FROM 테이블명)과 동일함
    bridges = Bridge.query.filter_by(address="서울특별시").all()  # None이 반환됨, orm 연동이 잘 안된 것으로 추정
    # bridges = bridge.Bridge.query.get(1)
    print(bridges)  # list의 select 결과
    #############################################################################
    start_coords = (37.5838699, 127.0565831)  # 시작 좌표
    m = folium.Map(location=start_coords, zoom_start=9, width='100%')

    #############################################################################
    with open('sudo_geo.json', mode='rt', encoding='utf-8') as f:  # 수도권 지역 geojson 경계선 표시
        geo_sudo = json.loads(f.read())
        f.close()

    folium.GeoJson(
        geo_sudo,
        name='sudo_geo'
    ).add_to(m)
    #############################################################################
    folium_map = MarkerCluster().add_to(m)

    for i in bridges:
        print(i.latitude, i.longitude)
        text = "이름: " + str(i.bridge_name) + "\n높이: " + str(i.bridge_height) + "\n수위: " + str(i.WL)
        pp_text = folium.IFrame(text, width=100, height=150)
        pp = folium.Popup(pp_text, max_width=400)
        ic = folium.Icon(color='red', icon='info-sign')
        folium.Marker(
            location=[i.latitude, i.longitude],
            popup=pp,
            icon=ic,
        ).add_to(folium_map)
    #############################################################################
    _ = m._repr_html_()

    # get definition of map in body
    map_div = Markup(folium_map.get_root().html.render())  # html 소스를 리턴
    # html to be included in header
    hdr_txt = Markup(folium_map.get_root().header.render())
    # html to be included in <script>
    script_txt = Markup(folium_map.get_root().script.render())
    #############################################################################

    return render_template('index.html', status=status, map_div=map_div, hdr_txt=hdr_txt, script_txt=script_txt, result_rain=rain, result_brid=bridges)


if __name__ == '__main__':
    app.run()
