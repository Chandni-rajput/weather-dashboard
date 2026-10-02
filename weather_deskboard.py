import tkinter as tk
from tkinter import messagebox
import requests

# Convert weather code into simple text
def weather_text(code):
    codes = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light Drizzle",
        61: "Light Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Light Snow",
        80: "Rain Showers",
        95: "Thunderstorm"
    }
    return codes.get(code, "Unknown Weather")


def get_weather():
    city = city_entry.get().strip()

    # Input validation
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        # Find city latitude and longitude
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data:
            messagebox.showerror("Not Found", "City not found. Please enter a valid city.")
            return

        place = geo_data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]
        city_name = place["name"]
        country = place.get("country", "")

        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto"
        }

        response = requests.get(weather_url, params=weather_params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current"]

        # Data processing
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        condition = weather_text(current["weather_code"])

        result_label.config(
            text=f"📍 {city_name}, {country}\n\n"
                 f"🌡 Temperature: {temperature} °C\n"
                 f"💧 Humidity: {humidity}%\n"
                 f"💨 Wind Speed: {wind} km/h\n"
                 f"☁ Weather: {condition}"
        )

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Connection Error",
            "Could not connect to the weather service.\nCheck your internet connection."
        )
    except (KeyError, TypeError, ValueError):
        messagebox.showerror("Data Error", "Weather data could not be processed.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


# GUI
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("430x500")
root.resizable(False, False)

title = tk.Label(
    root,
    text="🌤 Weather Dashboard",
    font=("Arial", 22, "bold")
)
title.pack(pady=25)

instruction = tk.Label(
    root,
    text="Enter a city name to check current weather",
    font=("Arial", 11)
)
instruction.pack()

city_entry = tk.Entry(root, font=("Arial", 14), width=25)
city_entry.pack(pady=15)
city_entry.focus()

search_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 13, "bold"),
    command=get_weather
)
search_button.pack(pady=10)

result_label = tk.Label(
    root,
    text="Weather information will appear here",
    font=("Arial", 13),
    justify="left",
    wraplength=350
)
result_label.pack(pady=35)

root.mainloop()