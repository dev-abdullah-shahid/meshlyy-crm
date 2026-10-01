# app/pages/activity.py
#
# The Activity Log page: a simple reverse-chronological list of every
# outreach interaction, across both brands and creators.

from nicegui import ui
from app.services import activity_service
from app.services.brand_service import get_brand_by_id
from app.services.creator_service import get_creator_by_id


def activity_log_page():
    ui.label("Activity Log").classes("text-2xl font-bold")

    container = ui.column().classes("w-full gap-2")

    activities = activity_service.get_all_activities()

    with container:
        if not activities:
            ui.label("No activity logged yet.").classes("text-gray-500")
            return

        for a in activities:
            # Look up the name of the brand or creator this activity belongs to.
            if a.lead_type == "brand":
                lead = get_brand_by_id(a.lead_id)
                lead_name = lead.brand_name if lead else "(deleted brand)"
            else:
                lead = get_creator_by_id(a.lead_id)
                lead_name = lead.name if lead else "(deleted creator)"

            with ui.card().classes("w-full p-3"):
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(a.created_at.strftime("%b %d, %Y")).classes("text-xs text-gray-500")
                    ui.label(a.lead_type.capitalize()).classes("text-xs text-gray-500")

                ui.label(lead_name).classes("font-bold")
                ui.label(f"Type: {a.activity_type or '—'}")
                if a.message_number:
                    ui.label(f"Message: {a.message_number}")
                ui.label(f"Result: {a.result or '—'}")
                if a.next_action:
                    ui.label(f"Next action: {a.next_action}")
                if a.next_action_date:
                    ui.label(f"Next action date: {a.next_action_date}")
                if a.notes:
                    ui.label(f"Notes: {a.notes}").classes("text-sm text-gray-600")