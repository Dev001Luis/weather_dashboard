import os
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-secret-key"

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city = ""
    if request.method == 'POST':
        city = request.form['city']
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon']
            }
        else:
            flash(f"City '{city}' not found. Please try again.", "danger")

    return render_template('index.html', weather=weather_data, city=city)
