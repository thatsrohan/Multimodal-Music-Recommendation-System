from nicegui import ui
from .navbar import navbar

def setup_home():

    @ui.page('/')
    def page():

        ui.add_head_html("""
        <style>

        /* ===== Hero Background ===== */
        body.home-theme {
            background: linear-gradient(135deg, #111 0%, #1A1A1A 40%, #2A0A3D 100%);
            background-size: 200% 200%;
            animation: bgShift 14s ease infinite;
            color: white;
        }
        @keyframes bgShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* ===== Hero title ===== */
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #FF5F6D, #FFC371, #7ED6DF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeUp 0.8s ease-out;
        }

        .hero-subtitle {
            font-size: 1.3rem;
            opacity: 0.85;
            animation: fadeUp 1.2s ease-out;
        }

        @keyframes fadeUp {
            from { opacity:0; transform: translateY(14px); }
            to   { opacity:1; transform: translateY(0); }
        }

        /* ===== Feature Cards ===== */
        .feature-card {
            padding: 22px;
            border-radius: 18px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.15);
            backdrop-filter: blur(8px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            transition: transform .22s ease, box-shadow .22s ease;
        }
        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 16px 40px rgba(0,0,0,0.35);
        }

        /* Fade animations */
        .fade-in { animation: fadeIn 800ms ease both; }
        @keyframes fadeIn {
            from { opacity:0; transform: translateY(8px); }
            to   { opacity:1; transform: translateY(0); }
        }

        </style>
        """)

        navbar()
        ui.run_javascript("document.body.className='home-theme';")

        # ========================== HERO SECTION ==========================
        with ui.column().classes('mt-24 items-center w-full'):

            ui.markdown("### 🎧 Listen. Feel. Sync.") \
                .classes("fade-in text-gray-300")

            ui.markdown("The next generation AI-powered music recommender.") \
                .classes("hero-title mt-2")

            ui.markdown(
                "Discover songs based on your mood, heartbeat, weather, and lyrics — all in real time."
            ).classes("hero-subtitle mt-4 mb-10 text-center w-3/4")

            ui.button(
                "Explore Features",
                on_click=lambda: ui.navigate.to('/versesync')
            ).classes(
                "bg-gradient-to-r from-red-500 to-orange-400 "
                "text-white px-8 py-3 rounded-xl shadow-lg hover:opacity-90 transition fade-in"
            )

        # ========================== FEATURE GRID ==========================
        with ui.row().classes("justify-center gap-8 mt-20 w-full flex-wrap"):

            # VibeSync
            with ui.card().classes("feature-card fade-in w-72"):
                ui.markdown("## 💓 VibeSync")
                ui.label("Music tuned to your heartbeat and facial emotions.")
                ui.button(
                    "Try",
                    on_click=lambda: ui.navigate.to('/vibesync')
                ).classes(
                    "bg-red-500 text-white px-4 py-2 rounded-lg mt-4 hover:bg-red-600"
                )

            # SkySync
            with ui.card().classes("feature-card fade-in w-72"):
                ui.markdown("## 🌤 SkySync")
                ui.label("Song recommendations powered by real-time weather.")
                ui.button(
                    "Try",
                    on_click=lambda: ui.navigate.to('/skysync')
                ).classes(
                    "bg-blue-500 text-white px-4 py-2 rounded-lg mt-4 hover:bg-blue-600"
                )

            # VerseSync
            with ui.card().classes("feature-card fade-in w-72"):
                ui.markdown("## ✍ VerseSync")
                ui.label("Paste lyrics and find matching songs instantly.")
                ui.button(
                    "Try",
                    on_click=lambda: ui.navigate.to('/versesync')
                ).classes(
                    "bg-purple-500 text-white px-4 py-2 rounded-lg mt-4 hover:bg-purple-600"
                )

            # ⭐ TasteSync (NEW)
            with ui.card().classes("feature-card fade-in w-72"):
                ui.markdown("## 🎧 TasteSync")
                ui.label("MF-based song recommendations using collaborative filtering.")
                ui.button(
                    "Try",
                    on_click=lambda: ui.navigate.to('/tastesync')
                ).classes(
                    "bg-teal-500 text-white px-4 py-2 rounded-lg mt-4 hover:bg-teal-600"
                )

        # ========================== FOOTER ==========================
        with ui.column().classes("mt-24 mb-10 opacity-70 items-center"):
            ui.markdown("Made for Final Year Project — Multimodal AI Recommender.")
            ui.label("Built with ❤ using Python, NiceGUI & Machine Learning.")