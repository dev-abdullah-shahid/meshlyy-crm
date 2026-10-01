# app/pages/settings.py
#
# Settings page: currently just Demo Data controls.

from nicegui import ui
from app.services import demo_service


def settings_page():
    ui.label("Settings").classes("text-2xl font-bold")

    ui.label("Demo Data").classes("text-lg font-semibold mt-4")
    ui.label(
        "Demo data is clearly tagged and fully separate from real prospects. "
        "Use it to explore the app safely."
    ).classes("text-gray-500 text-sm mb-2")

    count_label = ui.label()

    def refresh_count():
        b, c = demo_service.count_demo_data()
        count_label.text = f"Currently loaded: {b} demo brands, {c} demo creators"

    def load():
        demo_service.load_demo_data()
        ui.notify("Demo data loaded", color="positive")
        refresh_count()

    def delete():
        demo_service.delete_demo_data()
        ui.notify("Demo data deleted", color="warning")
        refresh_count()

    with ui.row().classes("gap-4"):
        ui.button("Load Demo Data", on_click=load).props("color=purple")
        ui.button("Delete Demo Data", on_click=delete).props("color=negative outline")

    refresh_count()