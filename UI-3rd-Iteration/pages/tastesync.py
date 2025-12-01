# tastesync.py
from nicegui import ui
from .navbar import navbar
import Backend.MFBasedRecommender as MF


def setup_tastesync():

    @ui.page('/tastesync')
    def page():

        navbar()

        # Global CSS (theme + animations)
        ui.add_head_html("""
        <style>
        body {
            background: linear-gradient(135deg, #0d0d0d, #14121a);
            color: white;
            font-family: 'Inter', sans-serif;
        }

        .taste-btn {
            background: linear-gradient(135deg, #06b6d4, #7c3aed);
            color: white !important;
            padding: 10px 22px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            transition: 0.18s ease;
        }
        .taste-btn:hover { transform: scale(1.03); filter: brightness(1.05); }

        .glass-card {
            background: rgba(255,255,255,0.04);
            backdrop-filter: blur(10px);
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 8px 24px rgba(124,58,237,0.08);
            transition: 0.22s ease;
            color: white;
        }
        .glass-card:hover { transform: translateY(-6px); box-shadow: 0 12px 34px rgba(124,58,237,0.12); }

        .meta { color: #cbd5e1; font-size: 0.95rem; }
        .score { color: #93c5fd; font-weight: 700; }

        .fade-in { animation: fadeIn 0.6s ease forwards; opacity: 0; }
        @keyframes fadeIn {
            to { opacity: 1; transform: translateY(0); }
            from { opacity: 0; transform: translateY(10px); }
        }
        </style>
        """)

        ui.markdown('## 🎧 *TasteSync — Matrix Factorization Recommender*') \
            .classes('text-3xl font-bold mb-4 fade-in')

        # REMOVE USER INPUTS → backend handles everything itself
        run_btn = ui.button('✨ Get Recommendations', on_click=lambda: run_mf()) \
            .classes('taste-btn')

        mf_cards = ui.column().classes('w-3/4 gap-3 mt-6')

        # ======================
        # RUN MF BACKEND + RENDER
        # ======================
        def run_mf():
            mf_cards.clear()
            ui.notify("Fetching MF recommendations...", color="blue")

            # Backend returns precomputed MF list
            try:
                recs = MF.get_mf_recommendations()
            except Exception as e:
                ui.notify(f"MF backend error: {e}", color='red')
                return

            if not recs:
                ui.notify("No MF recommendations returned.", color="yellow")
                return

            # Display MF recommendation cards
            for r in recs:
                song = r.get('track_name', r.get('song_id', 'Unknown'))
                artist = r.get('artist', 'Unknown')
                score = r.get('score', None)

                with mf_cards:
                    with ui.card().classes('glass-card fade-in'):
                        ui.markdown(f"### 🎵 {song}")
                        ui.markdown(f"*Artist:* {artist}").classes('meta')

                        meta_parts = []
                        if 'tempo' in r and r['tempo'] is not None:
                            meta_parts.append(f"⎈ {r['tempo']}")
                        if 'energy' in r and r['energy'] is not None:
                            meta_parts.append(f"⚡ {r['energy']:.2f}")
                        if 'valence' in r and r['valence'] is not None:
                            meta_parts.append(f"♥ {r['valence']:.2f}")

                        if meta_parts:
                            ui.label(" | ".join(meta_parts)).classes('meta mt-2')

                        if score is not None:
                            ui.label(f"Score: {score:.3f}").classes('score mt-2')