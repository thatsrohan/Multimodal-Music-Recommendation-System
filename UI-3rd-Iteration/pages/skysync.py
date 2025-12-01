from nicegui import ui
from .navbar import navbar
import Backend.WeatherBasedRecommender as W
import asyncio


def setup_skysync():

    @ui.page('/skysync')
    async def page():

        ui.add_head_html("""
<style>

body.skysync-theme {
    --c1: #E3F2FD;
    --c2: #BBDEFB;
    --c3: #90CAF9;
    background: linear-gradient(135deg, var(--c1), var(--c2), var(--c3));
    background-size: 300% 300%;
    animation: skyShift 12s ease infinite;
    color: #111;
    transition: background 600ms ease, color 300ms ease;
}
@keyframes skyShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Weather themes */
body.sky-sunny  { --c1:#FFE29F; --c2:#FFA99F; --c3:#FF719A; color:#111; }
body.sky-clear  { --c1:#A1C4FD; --c2:#C2E9FB; --c3:#E0F3FF; color:#111; }
body.sky-rainy  { --c1:#7A8CAA; --c2:#55667A; --c3:#3E4A57; color:white; }
body.sky-calm   { --c1:#D0E8F2; --c2:#CEE9E5; --c3:#EAF7FB; color:#111; }
body.sky-stormy { --c1:#2C3E50; --c2:#000000; --c3:#1C1C1C; color:#fff; }

/* Cards */
.sky-card {
    position: relative;
    border-radius: 18px;
    padding: 18px;
    background: rgba(255,255,255,0.55);
    color: inherit;
    backdrop-filter: blur(6px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.45);
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    transition: transform .22s ease, box-shadow .22s ease;
    overflow: hidden;
}
.sky-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.18);
}

/* Watermark emoji */
.sky-card[data-emoji]::after {
    content: attr(data-emoji);
    position: absolute;
    right: 12px;
    bottom: 8px;
    font-size: 42px;
    opacity: 0.12;
    pointer-events: none;
}

/* Fade animation */
.fade-in { animation: fadeIn 480ms ease both; }
@keyframes fadeIn {
    from { opacity:0; transform: translateY(8px); }
    to { opacity:1; transform:none; }
}

</style>
        """)

        navbar()

        with ui.column().classes("mt-16 w-full items-center"):

            ui.markdown("## 🌤 SkySync — Weather-Based Songs").classes("text-2xl fade-in")

            ui.label("Get song recommendations based on your local weather.") \
                .classes("text-gray-600 mb-4 fade-in")

            summary = ui.card().classes("p-4 rounded-xl shadow-lg sky-card fade-in")
            with summary:
                city_label = ui.label("City: -")
                mood_label = ui.label("Mood: -")
                emoji_label = ui.label("🌤")

            songs_container = ui.column().classes("w-3/4 gap-4 mt-4")
            

            emoji_map = {
                "sunny": "☀",
                "clear": "🌤",
                "rainy": "🌧",
                "calm": "🌥",
                "stormy": "⛈",
                "snow": "❄",
                "any": "🎵",
            }

            async def run_weather():

                loop = asyncio.get_running_loop()
                try:
                    data = await loop.run_in_executor(
                        None, W.get_weather_recommendations
                    )
                except Exception as e:
                    ui.notify(f"Weather backend error: {e}", color="red")
                    return

                if not data:
                    ui.notify("Could not fetch weather.", color="red")
                    return

                city = data.get("city", "Unknown")
                mood = data.get("detected_weather_mood", "any")
                emoji = emoji_map.get(mood, "🎵")

                city_label.set_text(f"City: {city}")
                mood_label.set_text(f"Mood: {mood}")
                emoji_label.set_text(emoji)

                ui.run_javascript(
                    f"document.body.className = 'skysync-theme sky-{mood}';"
                )

                songs_container.clear()

                songs = data.get("recommended_songs", [])
                if not songs:
                    ui.notify("No songs returned.", color="yellow")
                    return

                for s in songs:

                    track = s.get("track_name", "Unknown")
                    artist = s.get("artists", "Unknown")
                    tempo = s.get("tempo", "-")
                    energy = s.get("energy", "-")
                    valence = s.get("valence", "-")

                    with songs_container:
                        with ui.card().classes("sky-card fade-in"):
                            ui.markdown(f"### 🎵 {track}")
                            ui.label(f"Artist: {artist}")
                            ui.label(f"Tempo: {tempo}")
                            ui.label(f"Energy: {energy}")
                            ui.label(f"Valence: {valence}")

            ui.button(
                "Fetch Weather-Based Songs",
                on_click=run_weather
            ).classes(
                "bg-blue-600 text-white px-6 py-3 rounded-xl shadow-md "
                "hover:bg-blue-700 transition my-4"
            )