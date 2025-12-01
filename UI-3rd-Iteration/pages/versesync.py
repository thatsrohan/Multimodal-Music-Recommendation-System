from nicegui import ui
from .navbar import navbar
import Backend.LyricBasedRecommender as L

def setup_versesync():
    @ui.page('/versesync')
    def page():

        ui.add_head_html("""
        <style>
        body.versesync-dreamy {
          background: linear-gradient(135deg, #FDEFF9 0%, #E8F7FF 50%, #FFF9E6 100%);
          color: #111; transition: background 500ms ease;
        }
        body.versesync-melancholy {
          background: linear-gradient(135deg, #ECE9F6 0%, #FFFFFF 50%, #E6EEF3 100%);
          color: #111; transition: background 500ms ease;
        }
        body.versesync-energetic {
          background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 50%, #FFD54F 100%);
          color: #111; transition: background 500ms ease;
        }

        .versesync-card {
          position: relative; border-radius: 14px; padding: 18px;
          box-shadow: 0 8px 20px rgba(0,0,0,0.08);
          background: rgba(255,255,255,0.85);
          backdrop-filter: blur(4px);
          border: 1px solid rgba(255,255,255,0.6);
          overflow: hidden;
          transition: transform .22s ease, box-shadow .22s ease;
        }
        .versesync-card:hover {
          transform: translateY(-6px);
          box-shadow: 0 14px 30px rgba(0,0,0,0.12);
        }
        .versesync-card::before {
          content: "“"; position: absolute; left: 12px; top: 4px;
          font-size: 96px; line-height: 1;
          color: rgba(0,0,0,0.04); pointer-events: none;
        }
        .versesync-meta {
          font-size: 0.9rem; color: rgba(0,0,0,0.6); margin-top: 8px;
        }
        .versesync-title {
          display:inline-block; padding-bottom:6px;
          border-bottom: 3px solid rgba(0,0,0,0.06);
          margin-bottom:8px;
        }
        .versesync-card[data-emoji]::after {
          content: attr(data-emoji);
          position: absolute; right: 10px; bottom: 8px;
          font-size: 28px; opacity: 0.12; pointer-events: none;
        }
        </style>
        """)

        navbar()

        with ui.column().classes('mt-16 w-full items-center'):

            ui.markdown('## ✍ VerseSync — Lyrics-Based Recommender').classes('fade-in')

            lyrics_box = ui.textarea(
                label='Paste song lyrics',
                placeholder='Enter lyrics here...',
            ).style('width: 80%; height: 200px;').classes('my-4')

            cards_container = ui.column().classes('w-3/4 gap-3')

            def run_lyrics():
                lyrics = (lyrics_box.value or "").strip()
                if not lyrics:
                    ui.notify('Please paste some lyrics first!', color='red')
                    return

                rec = L.recommendations(lyrics)

                if hasattr(rec, 'to_dict'):
                    rows = rec.to_dict(orient='records')
                else:
                    rows = rec

                cards_container.clear()

                if not rows:
                    ui.notify('No recommendations found.', color='yellow')
                    return

                ui.run_javascript("document.body.className='versesync-dreamy';")

                for r in rows:
                    with cards_container:
                        with ui.card().classes('versesync-card fade-in').props('data-emoji="🎵"'):
                            ui.markdown(
                                f"{r.get('track_name', r.get('song', r.get('text','Unknown')))}"
                            ).classes('versesync-title')
                            ui.label(f"Artist: {r.get('artists', r.get('artist', 'Unknown'))}")
                            if 'similarity' in r:
                                ui.label(f"Similarity: {r.get('similarity'):.3f}").classes('versesync-meta')
                            elif 'score' in r:
                                ui.label(f"Score: {r.get('score'):.3f}").classes('versesync-meta')

            ui.button('Recommend Songs', on_click=run_lyrics).classes('my-4')