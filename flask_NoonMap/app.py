import folium
import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from folium.plugins import MarkerCluster
from datetime import datetime
import numpy as np
import pandas as pd
from tensorflow import keras
from apscheduler.schedulers.background import BackgroundScheduler
import urllib
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bridge_db.db"
app.config['SQLALCHEMY_BINDS'] = {
    'bridge_key': 'sqlite:///bridge_db.db',
    'rain_key': 'sqlite:///rain_msg.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#################################################################


class Bridge(db.Model):
    __tablename__ = 'BRIDGE'
    __bind_key__ = 'bridge_key'  # multiple db의 bind key
    id = db.Column(db.Integer, primary_key=True)
    bridge_name = db.Column(db.Text)
    address = db.Column(db.Text)
    etc_address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    brid_height_origin = db.Column(db.Float)
    location_start = db.Column(db.Text)
    wl_station_code = db.Column(db.Integer)
    station_name = db.Column(db.Text)
    location = db.Column(db.Text)
    obs_date = db.Column(db.DateTime)
    WL = db.Column(db.Float)
    bridge_height = db.Column(db.Float)


class Rain_msg(db.Model):
    __tablename__ = 'RAIN_MSG'
    __bind_key__ = 'rain_key'
    index = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.Text)
    location_id = db.Column(db.Text)
    location_name = db.Column(db.Text)
    md101_sn = db.Column(db.Text)
    msg = db.Column(db.Text)


#################################################################


db.create_all(bind='bridge_key')
db.create_all(bind='rain_key')


#################################################################


list_seoul = db.session.query(Bridge.latitude, Bridge.longitude,
                              Bridge.bridge_name, Bridge.bridge_height, Bridge.obs_date, Bridge.WL,
                              Bridge.address, Bridge.etc_address).group_by(Bridge.location_start).filter_by(address="서울특별시").all()

list_incheon = db.session.query(Bridge.latitude, Bridge.longitude,
                                Bridge.bridge_name, Bridge.bridge_height, Bridge.obs_date, Bridge.WL,
                                Bridge.address, Bridge.etc_address).group_by(Bridge.location_start).filter_by(address="인천광역시").all()

list_gyeonggi = db.session.query(Bridge.latitude, Bridge.longitude,
                                 Bridge.bridge_name, Bridge.bridge_height, Bridge.obs_date, Bridge.WL,
                                 Bridge.address, Bridge.etc_address).group_by(Bridge.location_start).filter_by(address="경기도").all()

brid_list = [p for (p,) in db.session.query(Bridge.location_start).group_by(Bridge.location_start).order_by(Bridge.id)]  # 교량 목록
loc_seoul = [p for (p,) in db.session.query(Bridge.location_start).group_by(Bridge.location_start).filter_by(address='서울특별시')]
loc_incheon = [p for (p,) in db.session.query(Bridge.location_start).group_by(Bridge.location_start).filter_by(address='인천광역시')]
loc_gyeonggi = [p for (p,) in db.session.query(Bridge.location_start).group_by(Bridge.location_start).filter_by(address='경기도')]

station_db_list = [p for (p,) in db.session.query(Bridge.wl_station_code).group_by(Bridge.location_start).order_by(Bridge.id)]  # 하천 수위 관측소 목록
wl_seoul = [p for (p,) in db.session.query(Bridge.wl_station_code).group_by(Bridge.location_start).filter_by(address='서울특별시')]
wl_incheon = [p for (p,) in db.session.query(Bridge.wl_station_code).group_by(Bridge.location_start).filter_by(address='인천광역시')]
wl_gyeonggi = [p for (p,) in db.session.query(Bridge.wl_station_code).group_by(Bridge.location_start).filter_by(address='경기도')]


#################################################################


def crawling_WL():
    url = 'http://www.hrfco.go.kr/sumun/waterlevelList.do'
    req = urllib.request.urlopen(url)
    res = req.read()
    soup = BeautifulSoup(res, 'html.parser')
    station_code = soup.find('table', {'summary': '검색결과'}).find_all('th')
    station_crawl_list = list(map(int, [str(i)[8:15] for i in station_code][6:]))
    wl = soup.find('table', {'summary': '검색결과'}).find_all('td')
    wl_list = [float(str(wl[i]).split(' ')[1]) for i in range(2, 815, 5)]
    wl_now = [[station_crawl_list[i], wl_list[i]] for i in range(len(station_crawl_list))]
    conn = sqlite3.connect('bridge_db.db')
    curs = conn.cursor()
    j = -1
    for i in station_db_list:
        j += 1
        if i in station_crawl_list:
            idx = station_crawl_list.index(i)
            x, y = wl_now[idx]
            now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            insert_temp = "INSERT INTO BRIDGE(bridge_name, address, etc_address, latitude, longitude, location_start," \
                          + " wl_station_code, station_name, location, obs_date, WL, bridge_height, brid_height_origin)" \
                          + " SELECT bridge_name, address, etc_address, latitude, longitude, location_start," \
                          + " wl_station_code, station_name, location, obs_date, WL, bridge_height, brid_height_origin" \
                          + " FROM BRIDGE WHERE wl_station_code = " + str(i) + " and location_start = '" + brid_list[j] + "' LIMIT 1;"
            curs.execute(insert_temp)
            conn.commit()
            insert_wl = "UPDATE BRIDGE SET obs_date='" + now + "', WL=" + str(y * 100) + " WHERE id = (SELECT max(id) FROM BRIDGE);"
            curs.execute(insert_wl)
            conn.commit()
        else:
            pass


scheduler1 = BackgroundScheduler()
scheduler1.add_job(func=crawling_WL, trigger='interval', hours=1, start_date='2020-09-15 17:00:00')
scheduler1.start()


#################################################################

def rescale(input_list, newmin, newmax):
    oldmin = np.min(input_list)
    oldmax = np.max(input_list)
    oldrange = (oldmax - oldmin)
    newrange = (newmax - newmin)

    newlist = []
    for i in input_list:
        newi = (((i - oldmin) * newrange) / oldrange) + newmin
        newlist.append(newi)

    return newlist


def re_rescale(input_value, oldmin, oldmax):
    oldrange = (oldmax - oldmin)
    oldi = round((input_value * oldrange) + oldmin, 0)
    return oldi


pred_tmp = []
def predict():
    global pred_tmp
    pred_tmp.clear()
    prediction = []
    for area_cnt in range(3):
        loc_area = []
        pred_area_wl = []
        if area_cnt == 0:
            loc_area = loc_seoul
        if area_cnt == 1:
            loc_area = loc_incheon
        if area_cnt == 2:
            loc_area = loc_gyeonggi
        for i in loc_area:
            time = [p for (p,) in db.session.query(Bridge.obs_date).filter_by(location_start=i)][-12:]
            value = [p for (p,) in db.session.query(Bridge.WL).filter_by(location_start=i)]
            std_value = rescale(value, 0, 1)[-12:]
            df = pd.DataFrame({'std_value': np.array(std_value)}, index=time)
            for j in range(12):
                df['shift_{}'.format(j)] = df['std_value'].shift(j)
            input_df = df.dropna().drop('std_value', axis=1)
            input_values = input_df.values
            input_data = input_values.reshape(input_values.shape[0], 12, 1)
            model_path = './model/' + i + '/lstm_model.hdf5'
            new_model = keras.models.load_model(model_path)
            new_result = new_model.predict(input_data)[0][0]
            pred_area_wl.append(re_rescale(new_result, min(value), max(value)))
        prediction.append(pred_area_wl)

    pred_tmp = prediction


predict()
scheduler2 = BackgroundScheduler()
scheduler2.add_job(func=predict, trigger='interval', hours=1, start_date='2020-09-15 17:04:00')
scheduler2.start()


#################################################################

area_value = None
list_area = None
len_area = None
danger = []


def pred_brid():
    global area_value
    global list_area
    global len_area
    global danger

    list_area = None
    len_area = None
    pred_wl = None

    if area_value == 'seoul':
        list_area = list_seoul
        pred_wl = pred_tmp[0]
    elif area_value == 'incheon':
        list_area = list_incheon
        pred_wl = pred_tmp[1]
    elif area_value == 'gyeonggi':
        list_area = list_gyeonggi
        pred_wl = pred_tmp[2]
    print(pred_wl)
    print(list_area)

    if list_area != None:
        len_area = len(list_area)

    #############################################################################

    start_coords = (37.5642135, 127.0016985)
    m = folium.Map(location=start_coords, zoom_start=9, width='100%')

    #############################################################################

    with open('sudo_geo.json', mode='rt', encoding='utf-8') as f:
        geo_sudo = json.loads(f.read())

    folium.GeoJson(
        geo_sudo,
        name='sudo_geo'
    ).add_to(m)

    #############################################################################

    folium_map = MarkerCluster().add_to(m)

    danger.clear()
    if list_area != None:
        for i in range(len(list_area)):
            text = """\
                <table style=width:100%>
                    <tr>
                        <th>교량 이름</th> <th>교량 높이</th> <th>예측 수위</th>
                    </tr>
                    <tr>
                        <td>{0}</td> <td>&nbsp;&nbsp;&nbsp;{1:.2f}m</td> <td>&nbsp;&nbsp;&nbsp;{2:.2f}m</td>
                    </tr>
                </table> """.format(str(list_area[i].bridge_name),
                                    list_area[i].bridge_height * 0.01,
                                    pred_wl[i] * 0.01)
            pp_text = folium.IFrame(text, width=350, height=80)
            pp = folium.Popup(pp_text, max_width=400)
            if list_area[i].bridge_height * 0.3 > pred_wl[i]:
                print('blue: ')
                print(pred_wl[i], list_area[i].bridge_height * 0.3)
                ic = folium.Icon(color='blue', icon='info-sign')
                danger.append('안전')
            elif list_area[i].bridge_height * 0.6 > pred_wl[i]:
                print('yellow: ')
                print(pred_wl[i], list_area[i].bridge_height * 0.6)
                ic = folium.Icon(color='orange', icon='info-sign')
                danger.append('주의')
            else:
                print('red: ')
                print(pred_wl[i])
                ic = folium.Icon(color='red', icon='info-sign')
                danger.append('위험')
            folium.Marker(
                location=[list_area[i].latitude, list_area[i].longitude],
                popup=pp,
                icon=ic,
            ).add_to(folium_map)

    folium_map.save('templates/map_{0}.html'.format(area_value))


@app.route('/map')
def mmap():
    global area_value

    return render_template('map_{0}.html'.format(area_value))


@app.route('/home')
@app.route('/')
def home():
    global area_value
    global list_area
    global len_area
    global danger

    if request.method == 'GET':
        area_value = request.args.get('btn_area', 0)
        print(area_value)

    predict_start = request.args.get('predict_start', 0)
    pred_brid()

    return render_template('index1.html', predict=predict_start, result_brid=list_area, len_brid=len_area, danger_text=danger)


if __name__ == '__main__':
    app.run()
