# app/pages/today.py
#
# The "Today" page — the first thing you should check each morning.
# Shows four sections computed from existing brand/creator data.

from nicegui import ui
from app.services.today_service import get_today_data


def render_lead_row(item: dict):
    """Renders one row for a prospect — reusable across all four sections."""
    with ui.row().classes("items-center justify-between w-full border-b py-1"):
        with ui.column().classes("gap-0"):
            ui.label(item["name"]).classes("font-semibold")
            ui.label(f'{item["lead_type"].capitalize()} · {item["stage"]}').classes(
                "text-xs text-gray-500"
            )
        with ui.column().classes("gap-0 items-end"):
            if item["next_action"]:
                ui.label(item["next_action"]).classes("text-sm")
            if item["next_action_date"]:
                ui.label(item["next_action_date"]).classes("text-xs text-gray-500")

        # Link to the right page (Brands or Creators) so they can act on it.
        target = "/brands" if item["lead_type"] == "brand" else "/creators"
        ui.link("Open", target).classes("text-purple-600 text-sm")


def render_section(title: str, items: list, empty_message: str):
    with ui.card().classes("w-full p-4"):
        ui.label(f"{title} ({len(items)})").classes("text-lg font-bold")
        if not items:
            ui.label(empty_message).classes("text-gray-500 text-sm")
        else:
            for item in items:
                render_lead_row(item)


def today_page():
    ui.label("Today").classes("text-2xl font-bold")
    ui.label("What needs your attention right now.").classes("text-gray-500 mb-2")

    data = get_today_data()

    render_section(
        "New Prospects", data["new_prospects"],
        "No new prospects awaiting first outreach."
    )
    render_section(
        "Replies", data["replies"],
        "No pending replies."
    )
    render_section(
        "Follow-ups Due", data["follow_ups"],
        "No follow-ups due today or overdue."
    )
    render_section(
        "Closing Actions", data["closing_actions"],
        "No prospects currently in a closing stage."
    )