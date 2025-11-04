import os
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-secret"

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

@app.route('/', methods=['GET', 'POST'])
def index():
    # variable init
    weather_data = None
    forecast_data = []
    city = ""
    country = ""
    units = request.args.get('units', 'metric')

    if request.method == 'POST':
        city = request.form['city'].strip()
        country = request.form['country'].strip().upper()
        query = f"{city},{country}" if country else city
        units = request.form.get('units', 'metric')

        params = {'q': query, 'appid': API_KEY, 'units': units}
        response = requests.get(BASE_CURRENT, params=params)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon']
            }

            # 5-day forecast (3-hour intervals)
            forecast_response = requests.get(BASE_FORECAST, params=params)
            if forecast_response.status_code == 200:
                forecast_raw = forecast_response.json()['list']
                # pick one forecast per day (every 8th entry)
                for i in range(0, len(forecast_raw), 8):
                    entry = forecast_raw[i]
                    forecast_data.append({
                        'date': entry['dt_txt'].split(' ')[0],
                        'temp': entry['main']['temp'],
                        'icon': entry['weather'][0]['icon']
                    })
        else:
            flash(f"City '{query}' not found. Please try again.", "danger")

    return render_template('index.html',
                weather=weather_data,
                forecast=forecast_data,
                city=city,
                country=country,
                units=units)
