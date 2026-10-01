# app/pages/brands.py
#
# The Brands page: search/filter bar, table of brands, and an Add/Edit form
# that opens in a dialog (a popup box).
from app.services import activity_service
from nicegui import ui
from app.services import brand_service

# Every possible stage a brand can be in (full list arrives in Phase 5 —
# for now we use a short starter list so the dropdown isn't empty).
STAGE_OPTIONS = [
    "New", "Qualified", "Contacted", "Replied", "Interested",
    "Audit Offered", "Audit Completed", "Campaign Discussion",
    "Payment Pending", "Paying", "Active Client",
    "Lost", "Not Now", "No Response", "Not A Fit",
]

def brands_page():
    ui.label("Brands").classes("text-2xl font-bold")

    # --- state for search/filter, kept as a simple dict we can mutate ---
        # --- state for search/filter, kept as a simple dict we can mutate ---
    filters = {"search": "", "stage": "", "category": "", "lead_source": "", "min_lead_score": None}

    # --- table container we will refresh whenever data changes ---
    table_container = ui.column().classes("w-full")

    def refresh_table():
        table_container.clear()
        brands = brand_service.get_all_brands(
            search=filters["search"],
            stage=filters["stage"],
            category=filters["category"],
            lead_source=filters["lead_source"],
            min_lead_score=filters["min_lead_score"],
        )
        
        with table_container:
            if not brands:
                ui.label("No brands found. Add your first brand above.").classes("text-gray-500")
                return

            columns = [
                {"name": "brand_name", "label": "Brand", "field": "brand_name", "align": "left"},
                {"name": "contact_name", "label": "Contact", "field": "contact_name", "align": "left"},
                {"name": "category", "label": "Category", "field": "category", "align": "left"},
                {"name": "stage", "label": "Stage", "field": "stage", "align": "left"},
                {"name": "lead_score", "label": "Lead Score", "field": "lead_score", "align": "left"},
                {"name": "last_contact", "label": "Last Contact", "field": "last_contact", "align": "left"},
                {"name": "next_action", "label": "Next Action", "field": "next_action", "align": "left"},
                {"name": "next_action_date", "label": "Next Action Date", "field": "next_action_date", "align": "left"},
            ]
            rows = [
                {
                    "id": b.id,
                    "brand_name": b.brand_name,
                    "contact_name": b.contact_name,
                    "category": b.category,
                    "stage": b.stage,
                    "lead_score": b.lead_score,
                    "last_contact": b.last_contact,
                    "next_action": b.next_action,
                    "next_action_date": b.next_action_date,
                }
                for b in brands
            ]
            table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
            table.on("rowClick", lambda e: open_edit_dialog(e.args[1]["id"]))

        # --- Search + filter bar ---
    categories = brand_service.get_all_categories()
    lead_sources = brand_service.get_all_lead_sources()

    with ui.row().classes("items-center gap-4 flex-wrap"):
        search_input = ui.input("Search brand name").on(
            "keydown.enter", lambda: (filters.update(search=search_input.value), refresh_table())
        )

        stage_select = ui.select(
            ["All"] + STAGE_OPTIONS, value="All", label="Stage"
        ).on(
            "update:model-value",
            lambda e: (
                filters.update(stage="" if e.args == "All" else e.args),
                refresh_table(),
            ),
        )

        category_select = ui.select(
            ["All"] + categories, value="All", label="Category"
        ).on(
            "update:model-value",
            lambda e: (
                filters.update(category="" if e.args == "All" else e.args),
                refresh_table(),
            ),
        )

        lead_source_select = ui.select(
            ["All"] + lead_sources, value="All", label="Lead Source"
        ).on(
            "update:model-value",
            lambda e: (
                filters.update(lead_source="" if e.args == "All" else e.args),
                refresh_table(),
            ),
        )

        min_score_input = ui.number("Min Lead Score", min=0, max=100).on(
            "update:model-value",
            lambda e: (
                filters.update(min_lead_score=e.args if e.args not in (None, "") else None),
                refresh_table(),
            ),
        )

        def apply_search():
            filters["search"] = search_input.value
            refresh_table()

        ui.button("Search", on_click=apply_search)

        def clear_filters():
            filters.update(search="", stage="", category="", lead_source="", min_lead_score=None)
            search_input.value = ""
            stage_select.value = "All"
            category_select.value = "All"
            lead_source_select.value = "All"
            min_score_input.value = None
            refresh_table()

        ui.button("Clear", on_click=clear_filters).props("outline")

    # --- Add Brand button + dialog ---
    add_dialog = ui.dialog()
    with add_dialog:
        with ui.card().classes("w-96"):
            ui.label("Add Brand").classes("text-lg font-bold")
            new_name = ui.input("Brand name *")
            new_contact = ui.input("Contact name")
            new_category = ui.input("Category")
            new_city = ui.input("City")
            new_stage = ui.select(STAGE_OPTIONS, value="New", label="Stage")
            new_lead_source = ui.input("Lead source")
            new_lead_score = ui.number("Lead score", min=0, max=100, value=0)
            def save_new_brand():
                if not new_name.value:
                    ui.notify("Brand name is required", color="negative")
                    return
                brand_service.create_brand({
                    "brand_name": new_name.value,
                    "contact_name": new_contact.value or "",
                    "category": new_category.value or "",
                    "city": new_city.value or "",
                    "stage": new_stage.value,
                    "lead_source": new_lead_source.value or "",
                    "lead_score": int(new_lead_score.value or 0),
                })
                ui.notify(f"Added {new_name.value}", color="positive")
                new_name.value = ""
                new_contact.value = ""
                new_category.value = ""
                new_city.value = ""
                new_stage.value = "New"
                new_lead_source.value = ""
                new_lead_score.value = 0
                add_dialog.close()
                refresh_table()

            with ui.row():
                ui.button("Save", on_click=save_new_brand)
                ui.button("Cancel", on_click=add_dialog.close).props("outline")

    ui.button("+ Add Brand", on_click=add_dialog.open).classes("mt-2")

    # --- Edit dialog (built dynamically per brand) ---
    edit_dialog = ui.dialog()

    def open_edit_dialog(brand_id: int):
        brand = brand_service.get_brand_by_id(brand_id)
        if not brand:
            return

        edit_dialog.clear()
        with edit_dialog:
            with ui.card().classes("w-96"):
                ui.label(f"Edit: {brand.brand_name}").classes("text-lg font-bold")
                e_name = ui.input("Brand name *", value=brand.brand_name)
                e_contact = ui.input("Contact name", value=brand.contact_name)
                e_category = ui.input("Category", value=brand.category)
                e_city = ui.input("City", value=brand.city)
                e_stage = ui.select(STAGE_OPTIONS, value=brand.stage, label="Stage")
                e_notes = ui.textarea("Notes", value=brand.notes)
                e_lead_source = ui.input("Lead source", value=brand.lead_source)
                e_lead_score = ui.number("Lead score", min=0, max=100, value=brand.lead_score or 0)

                def save_edit():
                    if not e_name.value:
                        ui.notify("Brand name is required", color="negative")
                        return
                    brand_service.update_brand(brand.id, {
                        "brand_name": e_name.value,
                        "contact_name": e_contact.value or "",
                        "category": e_category.value or "",
                        "city": e_city.value or "",
                        "stage": e_stage.value,
                        "notes": e_notes.value or "",
                        "lead_source": e_lead_source.value or "",
                        "lead_score": int(e_lead_score.value or 0),
                    })
                    ui.notify("Saved", color="positive")
                    edit_dialog.close()
                    refresh_table()

                def delete_this():
                    brand_service.delete_brand(brand.id)
                    ui.notify("Deleted", color="warning")
                    edit_dialog.close()
                    refresh_table()

                with ui.row():
                    ui.button("Save", on_click=save_edit)
                    ui.button("Delete", on_click=delete_this).props("color=negative outline")
                    ui.button("Cancel", on_click=edit_dialog.close).props("outline")

                ui.separator().classes("my-2")
                ui.label("Log Activity").classes("font-semibold")

                act_type = ui.select(
                    ["Instagram DM", "LinkedIn Message", "Email", "Call", "Other"],
                    value="Instagram DM", label="Activity type"
                )
                act_message_number = ui.input("Message number (e.g. M1)")
                act_result = ui.select(
                    ["No response", "Replied", "Interested", "Not interested", "Meeting booked"],
                    label="Result"
                )
                act_next_action = ui.input("Next action")
                act_next_action_date = ui.input("Next action date (YYYY-MM-DD)")
                act_notes = ui.textarea("Activity notes")

                def save_activity():
                    activity_service.log_activity("brand", brand.id, {
                        "activity_type": act_type.value or "",
                        "message_number": act_message_number.value or "",
                        "result": act_result.value or "",
                        "next_action": act_next_action.value or "",
                        "next_action_date": act_next_action_date.value or "",
                        "notes": act_notes.value or "",
                    })
                    ui.notify("Activity logged", color="positive")
                    edit_dialog.close()
                    refresh_table()

                ui.button("Save Activity", on_click=save_activity).props("color=purple")
        edit_dialog.open()

    # Initial load
    refresh_table()