from nicegui import ui

def navbar():
    ui.header().classes(
        'bg-blue-600 text-white p-4 shadow-md flex gap-6 fixed top-0 left-0 w-full z-50'
    )
    with ui.row().classes('pl-4 gap-6'):
        ui.link('Home', '/')
        ui.link('VerseSync', '/versesync')
        ui.link('SkySync', '/skysync')
        ui.link('VibeSync', '/vibesync')
        ui.link('TasteSync', '/tastesync')