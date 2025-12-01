from nicegui import ui
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import nicegui
import os

# Import pages
from pages.navbar import navbar
from pages.vibesync import setup_vibesync
from pages.skysync import setup_skysync
from pages.versesync import setup_versesync
from pages.home import setup_home
from pages.tastesync import setup_tastesync
def create_app():
    setup_home()
    setup_versesync()
    setup_skysync()
    setup_vibesync()
    setup_tastesync()
create_app()

ui.run(reload=False)