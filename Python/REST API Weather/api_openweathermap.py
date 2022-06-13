import requests
from datetime import datetime
import sqlite3
api = "68889189e96df020076471ee3f1ba02e"
cities_coordinates = {"Kyiv": {'lat': 50.433, 'lon': 30.513},
                      "Korosten'": {'lat': 50.959, 'lon': 28.639},
                      "Zhytomyr": {'lat': 50.265, 'lon': 28.677},
                      "Irpin": {'lat': 50.522, 'lon': 30.250},
                      "Odessa": {'lat': 46.477, 'lon': 30.733}
                      }
cities = list(cities_coordinates.keys())
connect = sqlite3.Connection('weather.db')
cursor = connect.cursor()
for city in cities:
    cursor.execute(f'''CREATE TABLE "{city}" (
 	"date" TEXT NOT NULL,
 	"temp" REAL NOT NULL,
 	"pcp" REAL NOT NULL,
 	"clouds" INTEGER NOT NULL,
 	"pressure" INTEGER NOT NULL,
    "humidity" INTEGER NOT NULL,
 	"wind_speed" REAL NOT NULL)''')
    request = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={cities_coordinates[city]["lat"]}&lon={cities_coordinates[city]["lon"]}&exclude=current,minutely,hourly,alerts,&appid={api}')
    json = request.json()
    for i in range(7):
        dt = json["daily"][i]["dt"]
        date = datetime.fromtimestamp(dt).strftime('%d.%m.%Y')
        temp_eve = json["daily"][i]["temp"]["eve"]
        temp = round(temp_eve - 273.15, 2)
        pcp = 0.0
        try:
            pcp = json["daily"][i]["snow"]
            pcp = json["daily"][i]["rain"]
        except:
            pass
        clouds = json["daily"][i]["clouds"]
        pressure = json["daily"][i]["pressure"]
        humidity = json["daily"][i]["humidity"]
        wind_speed = json["daily"][i]["wind_speed"]
        cursor.execute(f'''INSERT INTO "{city}" ("date","temp",
                       "pcp","clouds","pressure","humidity","wind_speed")
                        VALUES ("{date}",{temp},{pcp},{clouds},{pressure},{humidity},{wind_speed})''')
connect.commit()
connect.close()