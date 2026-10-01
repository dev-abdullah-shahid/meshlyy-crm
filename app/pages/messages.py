# app/pages/messages.py
#
# Simple message template library. Pick a template, see the text,
# copy it manually. No auto-sending (per Phase 12 rule).

from nicegui import ui
from app.models.message_template import BRAND_TEMPLATES, CREATOR_TEMPLATES


def render_template_list(templates: dict):
    for title, text in templates.items():
        with ui.card().classes("w-full p-3"):
            ui.label(title).classes("font-bold")
            box = ui.textarea(value=text).classes("w-full").props("readonly autogrow")

            def make_copy_handler(t=text):
                async def handler():
                    ui.run_javascript(f"navigator.clipboard.writeText({t!r})")
                    ui.notify("Copied to clipboard", color="positive")
                return handler

            ui.button("Copy", on_click=make_copy_handler()).props("outline size=sm")


def messages_page():
    ui.label("Messages").classes("text-2xl font-bold")
    ui.label("Select a template, edit as needed, and send manually.").classes("text-gray-500 mb-2")

    with ui.tabs().classes("w-full") as tabs:
        brand_tab = ui.tab("Brand Templates")
        creator_tab = ui.tab("Creator Templates")

    with ui.tab_panels(tabs, value=brand_tab).classes("w-full"):
        with ui.tab_panel(brand_tab):
            render_template_list(BRAND_TEMPLATES)
        with ui.tab_panel(creator_tab):
            render_template_list(CREATOR_TEMPLATES)