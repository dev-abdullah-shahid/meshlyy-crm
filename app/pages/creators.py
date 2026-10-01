# app/pages/creators.py
#
# The Creators page: search/filter bar, table, Add/Edit dialogs.
# Structurally identical to brands.py — same pattern, different fields.
from app.services import activity_service
from nicegui import ui
from app.services import creator_service

STAGE_OPTIONS = [
    "New", "Qualified", "Contacted", "Replied", "Interested",
    "Application", "Verification", "Approved", "Verified",
    "Campaign Matched", "Active Creator",
]
VERIFICATION_OPTIONS = ["Unverified", "Pending", "Verified"]


def creators_page():
    ui.label("Creators").classes("text-2xl font-bold")

    filters = {"search": "", "stage": "", "verification": "", "niche": ""}
    table_container = ui.column().classes("w-full")

    def refresh_table():
        table_container.clear()
        creators = creator_service.get_all_creators(
            search=filters["search"],
            stage=filters["stage"],
            verification=filters["verification"],
            niche=filters["niche"],
        
        )
        with table_container:
            if not creators:
                ui.label("No creators found. Add your first creator above.").classes("text-gray-500")
                return

            columns = [
                {"name": "name", "label": "Name", "field": "name", "align": "left"},
                {"name": "niche", "label": "Niche", "field": "niche", "align": "left"},
                {"name": "followers", "label": "Followers", "field": "followers", "align": "left"},
                {"name": "engagement", "label": "Engagement", "field": "engagement", "align": "left"},
                {"name": "stage", "label": "Stage", "field": "stage", "align": "left"},
                {"name": "verification_status", "label": "Verification", "field": "verification_status", "align": "left"},
                {"name": "last_contact", "label": "Last Contact", "field": "last_contact", "align": "left"},
                {"name": "next_action", "label": "Next Action", "field": "next_action", "align": "left"},
            ]
            rows = [
                {
                    "id": c.id,
                    "name": c.name,
                    "niche": c.niche,
                    "followers": c.followers,
                    "engagement": c.engagement,
                    "stage": c.stage,
                    "verification_status": c.verification_status,
                    "last_contact": c.last_contact,
                    "next_action": c.next_action,
                }
                for c in creators
            ]
            table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
            table.on("rowClick", lambda e: open_edit_dialog(e.args[1]["id"]))

        # --- Search + filter bar ---
    niches = creator_service.get_all_niches()

    with ui.row().classes("items-center gap-4 flex-wrap"):
        search_input = ui.input("Search creator name").on(
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

        verification_select = ui.select(
            ["All"] + VERIFICATION_OPTIONS, value="All", label="Verification"
        ).on(
            "update:model-value",
            lambda e: (
                filters.update(verification="" if e.args == "All" else e.args),
                refresh_table(),
            ),
        )

        niche_select = ui.select(
            ["All"] + niches, value="All", label="Niche"
        ).on(
            "update:model-value",
            lambda e: (
                filters.update(niche="" if e.args == "All" else e.args),
                refresh_table(),
            ),
        )

        def apply_search():
            filters["search"] = search_input.value
            refresh_table()

        ui.button("Search", on_click=apply_search)

        def clear_filters():
            filters.update(search="", stage="", verification="", niche="")
            search_input.value = ""
            stage_select.value = "All"
            verification_select.value = "All"
            niche_select.value = "All"
            refresh_table()

        ui.button("Clear", on_click=clear_filters).props("outline")

    # --- Add Creator dialog ---
    add_dialog = ui.dialog()
    with add_dialog:
        with ui.card().classes("w-96"):
            ui.label("Add Creator").classes("text-lg font-bold")
            new_name = ui.input("Creator name *")
            new_instagram = ui.input("Instagram")
            new_niche = ui.input("Niche")
            new_city = ui.input("City")
            new_stage = ui.select(STAGE_OPTIONS, value="New", label="Stage")

            def save_new_creator():
                if not new_name.value:
                    ui.notify("Creator name is required", color="negative")
                    return
                creator_service.create_creator({
                    "name": new_name.value,
                    "instagram": new_instagram.value or "",
                    "niche": new_niche.value or "",
                    "city": new_city.value or "",
                    "stage": new_stage.value,
                })
                ui.notify(f"Added {new_name.value}", color="positive")
                new_name.value = ""
                new_instagram.value = ""
                new_niche.value = ""
                new_city.value = ""
                new_stage.value = "New"
                add_dialog.close()
                refresh_table()

            with ui.row():
                ui.button("Save", on_click=save_new_creator)
                ui.button("Cancel", on_click=add_dialog.close).props("outline")

    ui.button("+ Add Creator", on_click=add_dialog.open).classes("mt-2")

    # --- Edit dialog ---
    edit_dialog = ui.dialog()

    def open_edit_dialog(creator_id: int):
        creator = creator_service.get_creator_by_id(creator_id)
        if not creator:
            return

        edit_dialog.clear()
        with edit_dialog:
            with ui.card().classes("w-96"):
                ui.label(f"Edit: {creator.name}").classes("text-lg font-bold")
                e_name = ui.input("Creator name *", value=creator.name)
                e_instagram = ui.input("Instagram", value=creator.instagram)
                e_niche = ui.input("Niche", value=creator.niche)
                e_city = ui.input("City", value=creator.city)
                e_stage = ui.select(STAGE_OPTIONS, value=creator.stage, label="Stage")
                e_verification = ui.select(
                    VERIFICATION_OPTIONS, value=creator.verification_status, label="Verification"
                )
                e_notes = ui.textarea("Notes", value=creator.notes)

                def save_edit():
                    if not e_name.value:
                        ui.notify("Creator name is required", color="negative")
                        return
                    creator_service.update_creator(creator.id, {
                        "name": e_name.value,
                        "instagram": e_instagram.value or "",
                        "niche": e_niche.value or "",
                        "city": e_city.value or "",
                        "stage": e_stage.value,
                        "verification_status": e_verification.value,
                        "notes": e_notes.value or "",
                    })
                    ui.notify("Saved", color="positive")
                    edit_dialog.close()
                    refresh_table()

                def delete_this():
                    creator_service.delete_creator(creator.id)
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
                    ["Instagram DM", "TikTok Message", "Email", "Call", "Other"],
                    value="Instagram DM", label="Activity type"
                )
                act_message_number = ui.input("Message number (e.g. M1)")
                act_result = ui.select(
                    ["No response", "Replied", "Interested", "Not interested", "Applied"],
                    label="Result"
                )
                act_next_action = ui.input("Next action")
                act_next_action_date = ui.input("Next action date (YYYY-MM-DD)")
                act_notes = ui.textarea("Activity notes")

                def save_activity():
                    activity_service.log_activity("creator", creator.id, {
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
                    activity_service.log_activity("creator", creator.id, {
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

    refresh_table()