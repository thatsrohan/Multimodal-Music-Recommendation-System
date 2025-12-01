from nicegui import ui
from .navbar import navbar
import Backend.PulseMoodBasedRecommender as P
import threading
import queue

def setup_vibesync():

    @ui.page('/vibesync')
    def page():

        ui.add_head_html("""
        <style>
        body.vibe-theme {
            background: linear-gradient(135deg, #ff9aaa, #ff6f8f, #ff3f6f);
            background-size: 300% 300%;
            animation: vibeShift 12s ease infinite;
            color: white;
        }
        @keyframes vibeShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .vibe-card {
            padding: 20px;
            border-radius: 16px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(6px);
            color: white;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .vibe-button {
            background: linear-gradient(90deg, rgba(255,255,255,0.18), rgba(255,255,255,0.08));
            color: white !important;
            border: 1px solid rgba(255,255,255,0.12);
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: 700;
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
            transition: transform .14s ease, box-shadow .14s ease;
        }
        .vibe-button:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(0,0,0,0.22); }
        .fade-in { animation: fadeIn 420ms ease both; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
        </style>
        """)

        ui.run_javascript("document.body.className='vibe-theme'")

        navbar()

        with ui.column().classes('mt-20 w-full items-center'):

            ui.markdown('## 💓 VibeSync — Pulse + Emotion Recommender').classes('text-white text-3xl fade-in')
            ui.label('Your webcam will detect emotion & pulse. Close the webcam window after 5 seconds.').classes('text-white/85 my-2 fade-in')

            result_container = ui.column().classes('w-full max-w-3xl mt-6 gap-4')
            q = queue.Queue()

            def run_vibesync():
                result_container.clear()
                ui.notify("Starting webcam detection…", color='#222')

                def worker():
                    try:
                        emotion, heart_rate, rec = P.detect_pulse_and_emotion()
                        q.put(('result', emotion, heart_rate, rec))
                    except Exception as e:
                        q.put(('error', str(e)))

                threading.Thread(target=worker, daemon=True).start()

                timer = None

                def poll():
                    nonlocal timer
                    if q.empty():
                        return
                    item = q.get()
                    if item[0] == 'error':
                        ui.notify(f"Backend error: {item[1]}", color='red')
                        print("VibeSync backend error:", item[1])
                    else:
                        _, emotion, heart_rate, rec = item
                        ui.notify(f"Detected:Emotion {emotion} — HR: {heart_rate}", color='#222')

                        if hasattr(rec, 'to_dict'):
                            rows = rec.to_dict(orient='records')
                        elif isinstance(rec, list):
                            rows = rec
                        elif isinstance(rec, dict):
                            rows = [rec]
                        else:
                            ui.notify("Invalid recommendation format", color='red')
                            print("Invalid recommendations:", rec)
                            rows = []

                        result_container.clear()
                        if not rows:
                            ui.notify("No recommendations found", color='yellow')
                        else:
                            for r in rows:
                                with result_container:
                                    with ui.card().classes('vibe-card fade-in'):
                                        ui.markdown(f"### 🎵 {r.get('track_name', 'Unknown Song')}").classes('text-white')
                                        ui.label(f"Artist: {r.get('artists', 'Unknown')}").classes('text-white/90')
                                        ui.label(f"Tempo: {r.get('tempo', '-') }").classes('text-white/80')
                                        ui.label(f"Energy: {r.get('energy', '-') }").classes('text-white/80')
                                        ui.label(f"Valence: {r.get('valence', '-') }").classes('text-white/80')

                    if timer:
                        timer.cancel()

                timer = ui.timer(0.5, poll, once=False)

            ui.button("Start VibeSync", on_click=run_vibesync).classes('vibe-button my-6')
