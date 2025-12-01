from fastapi import FastAPI, Request
import requests
import pandas as pd
import asyncio

app=FastAPI()

df = pd.read_csv(r"Datasets\SpotifyRecommendationData.csv")

df['weather_mood'] = 'any'  # default mood

df.loc[(df['valence'] > 0.7) & (df['energy'] > 0.7), 'weather_mood'] = 'sunny'
df.loc[(df['valence'] > 0.5) & (df['tempo'] > 110), 'weather_mood'] = 'clear'
df.loc[(df['valence'] < 0.4) & (df['energy'] < 0.5), 'weather_mood'] = 'rainy'
df.loc[(df['energy'] < 0.4) & (df['tempo'] < 100), 'weather_mood'] = 'calm'
df.loc[(df['energy'] > 0.6) & (df['valence'] < 0.5), 'weather_mood'] = 'stormy'

# Weather code → mood mapping
weather_mapping = {
    0: "sunny",
    1: "clear", 2: "clear", 3: "clear",
    45: "calm", 48: "calm",
    51: "rainy", 53: "rainy", 55: "rainy",
    61: "rainy", 63: "rainy", 65: "rainy",
    80: "rainy", 81: "rainy", 82: "rainy",
    95: "stormy", 96: "stormy", 99: "stormy"
}

@app.get("/weather")
def get_weather(request: Request = None):

    # If running through FastAPI
    if request is not None:
        client_ip = request.client.host
    else:
        # If called from NiceGUI or terminal → simulate local IP
        client_ip = "127.0.0.1"

    # If running locally,fetching public IP
    if (
        client_ip.startswith("127.") or      # localhost
        client_ip.startswith("10.") or       # hotspot LAN IP
        client_ip.startswith("192.168.")     # home WiFi LAN IP
    ):
        try:
            client_ip = requests.get("https://api.ipify.org?format=json").json()['ip']
        except:
            # fallback if internet/ipify fails
            client_ip = "8.8.8.8"

    # Calling IP geolocation API
    ip_api_url = f"http://ip-api.com/json/{client_ip}"
    ip_data = requests.get(ip_api_url).json()

    lat = ip_data.get("lat")
    lon = ip_data.get("lon")

    if lat is None or lon is None:
        return {"error": "Could not detect location"}

    # Getting the weather
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather = requests.get(url).json()

    weather_code = weather["current_weather"]["weathercode"]

    mood = weather_mapping.get(weather_code, "any")

    # Filter songs by mood
    filtered = df[df["weather_mood"] == mood]

    # If not enough songs, fallback to whole dataset
    if len(filtered) < 10:
        filtered = df

    songs = filtered.sample(10).to_dict(orient="records")

    return {
        "ip": client_ip,
        "city": ip_data.get("city"),
        "detected_weather_mood": mood,
        "recommended_songs": songs
    }

# --------------------------------------------------
# API helper method (NON-BREAKING for NiceGUI UI)
# --------------------------------------------------
def get_weather_recommendations():
    return get_weather()
