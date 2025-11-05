from flask import Flask, render_template, request, flash
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev-secret"

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    city = ""
    country = ""
    units = "metric"

    if request.method == "POST":
        city = request.form["city"].strip()
        country = request.form["country"].strip().upper()
        units = request.form["units"]
        query = f"{city},{country}" if country else city

        # --- Fetch current weather ---
        params_current = {"q": query, "appid": API_KEY, "units": units}
        response_current = requests.get(BASE_URL_CURRENT, params=params_current)
        print(f"{params_current}")
        if response_current.status_code == 200:
            data = response_current.json()
            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
            }

            # --- Fetch 5-day forecast ---
            params_forecast = {"q": query, "appid": API_KEY, "units": units}
            response_forecast = requests.get(BASE_URL_FORECAST, params=params_forecast)

            if response_forecast.status_code == 200:
                forecast_json = response_forecast.json()
                forecast_list = forecast_json["list"]

                # Extract one temperature per day (midday data)
                daily_data = {}
                for entry in forecast_list:
                    date_txt = entry["dt_txt"]
                    date = date_txt.split(" ")[0]
                    time = date_txt.split(" ")[1]
                    if time == "12:00:00":  # pick midday values
                        daily_data[date] = entry["main"]["temp"]

                forecast_data = [
                    {"date": datetime.strptime(date, "%Y-%m-%d").strftime("%a %d"), "temp": temp}
                    for date, temp in daily_data.items()
                ]

            else:
                flash("Forecast data could not be loaded.", "warning")

        else:
            flash(f"City '{query}' not found. Please try again.", "danger")

    return render_template(
        "index.html",
        weather=weather_data,
        forecast=forecast_data,
        city=city,
        country=country,
        units=units,
    )


if __name__ == "__main__":
    app.run(debug=True)
