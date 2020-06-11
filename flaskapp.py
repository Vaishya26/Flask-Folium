from flask import Flask, request, render_template
from flask import jsonify
import pymysql.cursors
import pymysql
import folium
# conn=pymysql.connect(host='harshit-data.czohtzq5psyg.ap-south-1.rds.amazonaws.com',user='harshit_test',password='harshitaws',db='harshit_base',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
conn=pymysql.connect(host='localhost',user='root',password='harshit',db='harshit_base',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
app = Flask(__name__)
@app.route('/q/<input_str>',methods = ['GET'])
def someName(input_str):
    val = "'"+input_str+"'"
    box_no = input_str[0:3]
    a = input_str[3:]
    if(len(a)>=11):
        if(a[11]=='A'):
            utc_hh = int(a[0:2])
            utc_mm = int(a[2:4])
            utc_ss = int(a[4:6])
            lat_raw = a[13:22]
            lng_raw = a[26:35]
            if((utc_mm + 30) >= 60):
                loc_hh = utc_hh + 6
                if(loc_hh>=24):
                    loc_hh = loc_hh - 24
                loc_mm = utc_mm - 30
            else:
                loc_hh = utc_hh + 5
                if(loc_hh>=24):
                    loc_hh = loc_hh - 24
                loc_mm = utc_mm + 30
            loc_t = str(loc_hh).zfill(2)+":"+str(loc_mm).zfill(2)+":"+str(utc_ss).zfill(2)
            lat = str(float(lat_raw[0:2]) + (float(lat_raw[2:])/60))
            lng = str(float(lng_raw[0:2]) + (float(lng_raw[2:])/60))
            gps = "'"+loc_t+"'"
            lat_f = "'"+lat+"'"
            lng_f = "'"+lng+"'"
            boxno = "'"+box_no+"'"
            cursor_ = conn.cursor()
            # sql = "INSERT INTO harshit_3 (raw_data,latitute,longitude,gps_time) VALUES(%s,%s,%s,%s)" % (val,lat_f,lng_f,gps)
            sql = "INSERT INTO harshit_aws(raw_data,box_no,latitude,longitude,gps_time) VALUES(%s,%s,%s,%s,%s)" % (val,boxno,lat_f,lng_f,gps)
            cursor_.execute(sql)
            conn.commit()
            z = str(cursor_.rowcount)
            cursor_.close()
            resp = jsonify("OK")
            resp.status_code = 200
            return resp
        elif(a[11]=='V'):
            utc_hh = int(a[0:2])
            utc_mm = int(a[2:4])
            utc_ss = int(a[4:6])
            if((utc_mm + 30) >= 60):
                loc_hh = utc_hh + 6
                if(loc_hh>=24):
                    loc_hh = loc_hh - 24
                loc_mm = utc_mm - 30
            else:
                loc_hh = utc_hh + 5
                if(loc_hh>=24):
                    loc_hh = loc_hh - 24
                loc_mm = utc_mm + 30
            loc_t = str(loc_hh).zfill(2)+":"+str(loc_mm).zfill(2)+":"+str(utc_ss).zfill(2)
            lat = "---"
            lng = "---"
            gps = "'"+loc_t+"'"
            lat_f = "'"+lat+"'"
            lng_f = "'"+lng+"'"
            boxno = "'"+box_no+"'"
            cursor_ = conn.cursor()
            # sql = "INSERT INTO harshit_3 (raw_data,latitute,longitude,gps_time) VALUES(%s,%s,%s,%s)" % (val,lat_f,lng_f,gps)
            sql = "INSERT INTO harshit_aws(raw_data,box_no,latitude,longitude,gps_time) VALUES(%s,%s,%s,%s,%s)" % (val,boxno,lat_f,lng_f,gps)
            cursor_.execute(sql)
            conn.commit()
            z = str(cursor_.rowcount)
            cursor_.close()
            resp = jsonify("OK")
            resp.status_code = 200
            return resp
        else:
            loc_t = "---"
            lat = "---"
            lng = "---"
            raw = "---"
            gps = "'"+loc_t+"'"
            lat_f = "'"+lat+"'"
            lng_f = "'"+lng+"'"
            raw_data = "'"+raw+"'"
            boxno = "'"+box_no+"'"
            cursor_ = conn.cursor()
            # sql = "INSERT INTO harshit_3 (raw_data,latitute,longitude,gps_time) VALUES(%s,%s,%s,%s)" % (val,lat_f,lng_f,gps)
            sql = "INSERT INTO harshit_aws(dummy_data,raw_data,box_no,latitude,longitude,gps_time) VALUES(%s,%s,%s,%s,%s,%s)" % (val,raw_data,boxno,lat_f,lng_f,gps)
            cursor_.execute(sql)
            conn.commit()
            z = str(cursor_.rowcount)
            cursor_.close()
            conn.close()
            resp = jsonify("OK")
            resp.status_code = 200
            return resp
    else:
        loc_t = "---"
        lat = "---"
        lng = "---"
        raw = "---"
        gps = "'"+loc_t+"'"
        lat_f = "'"+lat+"'"
        lng_f = "'"+lng+"'"
        raw_data = "'"+raw+"'"
        boxno = "'"+box_no+"'"
        cursor_ = conn.cursor()
        # sql = "INSERT INTO harshit_3 (raw_data,latitute,longitude,gps_time) VALUES(%s,%s,%s,%s)" % (val,lat_f,lng_f,gps)
        sql = "INSERT INTO harshit_aws(dummy_data,raw_data,box_no,latitude,longitude,gps_time) VALUES(%s,%s,%s,%s,%s,%s)" % (val,raw_data,boxno,lat_f,lng_f,gps)
        cursor_.execute(sql)
        conn.commit()
        z = str(cursor_.rowcount)
        cursor_.close()
        resp = jsonify("OK")
        resp.status_code = 200
        return resp


@app.route('/view')
def gui():
    cursor1 = conn.cursor()
    # sql = "SELECT * FROM harshit_3 ORDER BY id desc"
    sql = "SELECT * FROM harshit_aws ORDER BY id desc"
    cursor1.execute(sql)
    res = cursor1.fetchall()
    cursor1.close()
    return render_template('gui.html', result=res, content_type='application/json')

@app.route('/mapview',methods = ['GET'])
def map():
    data1 = request.args['boxno']
    box = "'"+data1+"'"
    cursor2 = conn.cursor()
    # sql = "SELECT * FROM harshit_aws ORDER BY id desc limit 1"
    sql = "SELECT * FROM harshit_aws WHERE box_no = %s ORDER BY id desc limit 1"
    cursor2.execute(sql,(data1,))
    res = cursor2.fetchall()
    cursor2.close()
    if(res):
        lat = float(res[0]['latitude'])
        lng = float(res[0]['longitude'])
        veh = res[0]['box_no']
        time = res[0]['gps_time']
        map = folium.Map(location=[lat, lng], zoom_start=15)
        folium.CircleMarker(location = [lat, lng], radius = 50, popup = 'vehicle-No:'+veh+'\nTime:'+time).add_to(map)
        folium.Marker(location = [lat, lng], radius = 50, popup = 'vehicle-No:'+veh+'\nTime:'+time).add_to(map)
        map.save(outfile='/var/www/html/flaskapp/templates/map.html')
        # return map._repr_html_()
        return render_template('map.html')
    else:
        return "Box Number Not Found!!"

@app.route('/home')
def home():
    return render_template('home.html')

    


    # return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
