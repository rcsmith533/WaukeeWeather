from datetime import datetime
from flask import Flask, render_template
import json
import requests
#from waitress import serve

API_KEY = 'fb95c40c2dc15842dd9248fc6090be5f'
ZIP_CODE = '50263'
CURRENT_URL = f'http://api.openweathermap.org/data/2.5/weather?zip={ZIP_CODE}&appid={API_KEY}&units=imperial'
FORECAST_URL = f'http://api.openweathermap.org/data/2.5/forecast?zip={ZIP_CODE},US&appid={API_KEY}&units=imperial'

def windDirection(degree):
    if degree <= 11.25:
        return 'N'
    elif 11.25 < degree < 33.75:
        return 'N/NE'
    elif 33.75 <= degree <= 56.25:
        return 'NE'
    elif 56.25 < degree < 78.75:
        return 'E/NE'
    elif 78.75 <= degree <= 101.25:
        return 'E'
    elif 101.25 < degree < 123.75:
        return 'E/SE'
    elif 123.75 <= degree <= 146.25:
        return 'SE'
    elif 146.25 < degree < 168.75:
        return 'S/SE'
    elif 168.75 <= degree <= 191.25:
        return 'S' 
    elif 191.25 < degree < 213.75:
        return 'S/SW'
    elif 213.75 <= degree <= 236.25:
        return 'SW'
    elif 236.25 < degree < 258.75:
        return 'W/SW'
    elif 258.75 <= degree <= 281.25:
        return 'W'
    elif 281.25 < degree < 303.75:
        return 'W/NW'
    elif 303.75 <= degree <= 326.25:
        return 'NW'
    elif 326.25 < degree < 348.75:
        return 'N/NW'
    elif 348.75 <= degree:
        return 'N'

def fixDT(myList):
    for i in myList:
        timeString = i['dt_txt']
        DT = datetime.strptime(timeString,'%Y-%m-%d %H:%M:%S')
        day = DT.strftime('%m/%d')
        time = DT.strftime('%I:%M %p')
        i['dt_txt'] = {'day':day,'time':time}

#For Testing
def useLocalFiles():
    weather = ''
    j = ''
    with open('CurrentData.txt') as json_file:
        data = json.load(json_file)
        j = data

    with open('5Day.txt') as json_file:
        data = json.load(json_file)
        weather = data['list']
        fixDT(weather)
    return weather,j

def useOnline(zip_code):
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={API_KEY}&units=imperial')
    curr = r.json()
    r = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},US&appid={API_KEY}&units=imperial')
    weather = r.json()['list']
    fixDT(weather)
    return weather, curr

#Used for testing with method above
#weather,curr = useLocalFiles()

#Use online files
#weather, curr = useOnline()

app = Flask(__name__)

@app.route('/')
def index():
    weather, curr = useOnline('50263')
    return render_template('index.html',temp=curr['main']['temp'],feels_like=curr['main']['feels_like'],wind_speed=curr['wind']['speed'],weather=weather,len=len(weather),gust=curr['wind']['gust'],direction=windDirection(curr['wind']['deg']))

@app.route('/clinton')
def clinton():
    weather, curr = useOnline('61727')
    return render_template('clinton.html',temp=curr['main']['temp'],feels_like=curr['main']['feels_like'],wind_speed=curr['wind']['speed'],weather=weather,len=len(weather))

@app.route('/wm')
def westminster():
    weather,curr = useOnline('80234')
    return render_template('wm.html',temp=curr['main']['temp'],feels_like=curr['main']['feels_like'],wind_speed=curr['wind']['speed'],weather=weather,len=len(weather))

#app.run(debug=True,host='192.168.0.7',port=80)
#serve(app,host='0.0.0.0',port=80, threads=1)

if __name__ == '__main__':
    app.run(threaded=True,port=80)
