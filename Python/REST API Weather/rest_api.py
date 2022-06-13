from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import sqlite3
from datetime import datetime
import pandas as pd
app = Flask(__name__)

@app.route('/cities')

def cities():
    connect = sqlite3.connect("weather.db")
    cursor = connect.cursor()
    cursor.execute('SELECT name FROM sqlite_schema')
    table = cursor.fetchall()
    connect.close()
    cities = list()
    for row in table:
        cities.append(row[0])
    return jsonify({"cities": cities})

@app.route('/mean')

def mean():
    value_type = request.args.get("value_type")
    city = request.args.get("city")
    types = ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']
    if value_type in types:
        connect = sqlite3.connect("weather.db")
        cursor = connect.cursor()
        cursor.execute(f'SELECT {value_type} FROM {city}')
        table = cursor.fetchall()
        connect.close()
        values = list()
        for row in table:
            values.append(row[0])
        mean = round(sum(values) / len(values), 2)
        return jsonify({"mean": mean})

@app.route('/records')

def records():
    city = request.args.get("city")
    start_dt = datetime.strptime(request.args.get("start_dt"), '%d.%m.%Y').date()
    end_dt = datetime.strptime(request.args.get("end_dt"), '%d.%m.%Y').date()
    connect = sqlite3.connect("weather.db")
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM {city}')
    table = cursor.fetchall()
    connect.close()
    records = list()
    for row in table:
        date = datetime.strptime(row[0], '%d.%m.%Y').date()
        if date >= start_dt and date <= end_dt:
            records.append({"date": row[0],"temp": row[1], "pcp": row[2], "clouds": row[3], 
                            "pressure": row[4], "himidity": row[5], "wind_speed": row[6]})
    
    return jsonify({"records": records})

@app.route('/moving_mean')

def moving_mean():
    value_type = request.args.get("value_type")
    city = request.args.get("city")
    types = ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']
    if value_type in types:
        connect = sqlite3.connect("weather.db")
        cursor = connect.cursor()
        cursor.execute(f'SELECT date,{value_type} FROM {city}')
        table = cursor.fetchall()
        connect.close()
        dates = list()
        values = list()
        for row in table:
            dates.append(row[0])
            values.append(row[1])
        series = pd.Series(values)
        moving_average = series.expanding().mean().round(2).tolist()
        moving_mean = list()
        for i in range(len(dates)):
            moving_mean.append({"date": dates[i], value_type: moving_average[i]})
        return jsonify({"moving_mean": moving_mean})

if __name__ == '__main__':
    app.run(port=10000)