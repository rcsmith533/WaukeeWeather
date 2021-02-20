from datetime import datetime
from flask import Flask, render_template
import json
import requests
#from waitress import serve

API_KEY = 'fb95c40c2dc15842dd9248fc6090be5f'
ZIP_CODE = '50263'
CURRENT_URL = f'http://api.openweathermap.org/data/2.5/weather?zip={ZIP_CODE}&appid={API_KEY}&units=imperial'
FORECAST_URL = f'http://api.openweathermap.org/data/2.5/forecast?zip={ZIP_CODE},US&appid={API_KEY}&units=imperial'

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
weather, curr = useOnline()

app = Flask(__name__)

@app.route('/')
def index():
    weather, curr = useOnline('50263')
    return render_template('index.html',temp=curr['main']['temp'],feels_like=curr['main']['feels_like'],wind_speed=curr['wind']['speed'],weather=weather,len=len(weather))

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