# app/pages/campaigns.py
#
# The Campaigns page: Add Campaign (pick a Brand + Creator), table of
# campaigns, and click-to-edit — same pattern as Brands/Creators.

from nicegui import ui
from app.services import campaign_service
from app.services.brand_service import get_all_brands, get_brand_by_id
from app.services.creator_service import get_all_creators, get_creator_by_id

STATUS_OPTIONS = [
    "Proposed", "Approved", "Payment Pending", "Paid",
    "Creators Selected", "Content In Progress", "Live",
    "Completed", "Results Delivered",
]


def campaigns_page():
    ui.label("Campaigns").classes("text-2xl font-bold")

    table_container = ui.column().classes("w-full")

    def refresh_table():
        table_container.clear()
        campaigns = campaign_service.get_all_campaigns()
        with table_container:
            if not campaigns:
                ui.label("No campaigns yet. Add your first campaign above.").classes("text-gray-500")
                return

            columns = [
                {"name": "campaign_name", "label": "Campaign", "field": "campaign_name", "align": "left"},
                {"name": "brand_name", "label": "Brand", "field": "brand_name", "align": "left"},
                {"name": "creator_name", "label": "Creator", "field": "creator_name", "align": "left"},
                {"name": "status", "label": "Status", "field": "status", "align": "left"},
                {"name": "budget", "label": "Budget", "field": "budget", "align": "left"},
                {"name": "start_date", "label": "Start", "field": "start_date", "align": "left"},
                {"name": "end_date", "label": "End", "field": "end_date", "align": "left"},
            ]
            rows = []
            for c in campaigns:
                brand = get_brand_by_id(c.brand_id)
                creator = get_creator_by_id(c.creator_id)
                rows.append({
                    "id": c.id,
                    "campaign_name": c.campaign_name,
                    "brand_name": brand.brand_name if brand else "(deleted brand)",
                    "creator_name": creator.name if creator else "(deleted creator)",
                    "status": c.status,
                    "budget": c.budget,
                    "start_date": c.start_date,
                    "end_date": c.end_date,
                })
            table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
            table.on("rowClick", lambda e: open_edit_dialog(e.args[1]["id"]))

    # --- Add Campaign dialog ---
    add_dialog = ui.dialog()
    with add_dialog:
        with ui.card().classes("w-96"):
            ui.label("Add Campaign").classes("text-lg font-bold")

            brands = get_all_brands()
            creators = get_all_creators()

            if not brands or not creators:
                ui.label(
                    "You need at least one Brand and one Creator before creating a campaign."
                ).classes("text-negative text-sm")
                ui.button("Close", on_click=add_dialog.close)
            else:
                brand_options = {b.id: b.brand_name for b in brands}
                creator_options = {c.id: c.name for c in creators}

                new_name = ui.input("Campaign name *")
                new_brand = ui.select(brand_options, label="Brand *")
                new_creator = ui.select(creator_options, label="Creator *")
                new_budget = ui.input("Budget (or leave blank for Unknown)")
                new_start = ui.input("Start date (YYYY-MM-DD)")
                new_end = ui.input("End date (YYYY-MM-DD)")

                def save_new_campaign():
                    if not new_name.value or not new_brand.value or not new_creator.value:
                        ui.notify("Campaign name, Brand, and Creator are required", color="negative")
                        return
                    campaign_service.create_campaign({
                        "campaign_name": new_name.value,
                        "brand_id": new_brand.value,
                        "creator_id": new_creator.value,
                        "budget": new_budget.value or "Unknown",
                        "start_date": new_start.value or "",
                        "end_date": new_end.value or "",
                        "status": "Proposed",
                    })
                    ui.notify(f"Added {new_name.value}", color="positive")
                    add_dialog.close()
                    refresh_table()

                with ui.row():
                    ui.button("Save", on_click=save_new_campaign)
                    ui.button("Cancel", on_click=add_dialog.close).props("outline")

    ui.button("+ Add Campaign", on_click=add_dialog.open).classes("mt-2")

    # --- Edit dialog ---
    edit_dialog = ui.dialog()

    def open_edit_dialog(campaign_id: int):
        campaign = campaign_service.get_campaign_by_id(campaign_id)
        if not campaign:
            return

        brand = get_brand_by_id(campaign.brand_id)
        creator = get_creator_by_id(campaign.creator_id)

        edit_dialog.clear()
        with edit_dialog:
            with ui.card().classes("w-96"):
                ui.label(f"Edit: {campaign.campaign_name}").classes("text-lg font-bold")
                ui.label(f"Brand: {brand.brand_name if brand else '(deleted)'}").classes("text-sm text-gray-500")
                ui.label(f"Creator: {creator.name if creator else '(deleted)'}").classes("text-sm text-gray-500")

                e_name = ui.input("Campaign name *", value=campaign.campaign_name)
                e_status = ui.select(STATUS_OPTIONS, value=campaign.status, label="Status")
                e_budget = ui.input("Budget", value=campaign.budget)
                e_start = ui.input("Start date (YYYY-MM-DD)", value=campaign.start_date)
                e_end = ui.input("End date (YYYY-MM-DD)", value=campaign.end_date)
                e_results = ui.textarea("Results", value=campaign.results)
                e_notes = ui.textarea("Notes", value=campaign.notes)

                def save_edit():
                    if not e_name.value:
                        ui.notify("Campaign name is required", color="negative")
                        return
                    campaign_service.update_campaign(campaign.id, {
                        "campaign_name": e_name.value,
                        "status": e_status.value,
                        "budget": e_budget.value or "Unknown",
                        "start_date": e_start.value or "",
                        "end_date": e_end.value or "",
                        "results": e_results.value or "",
                        "notes": e_notes.value or "",
                    })
                    ui.notify("Saved", color="positive")
                    edit_dialog.close()
                    refresh_table()

                def delete_this():
                    campaign_service.delete_campaign(campaign.id)
                    ui.notify("Deleted", color="warning")
                    edit_dialog.close()
                    refresh_table()

                with ui.row():
                    ui.button("Save", on_click=save_edit)
                    ui.button("Delete", on_click=delete_this).props("color=negative outline")
                    ui.button("Cancel", on_click=edit_dialog.close).props("outline")

        edit_dialog.open()

    refresh_table()