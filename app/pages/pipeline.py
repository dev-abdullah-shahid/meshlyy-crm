# app/pages/pipeline.py
#
# Kanban-style pipeline board for Brands and Creators.

from nicegui import ui
from app.services import brand_service, creator_service
from app.pages.brands import STAGE_OPTIONS as BRAND_STAGES
from app.pages.creators import STAGE_OPTIONS as CREATOR_STAGES
from app.components.theme import CARD_ALT, BORDER, TEXT, GRAY, get_stage_color, initials_avatar


def pipeline_page():
    ui.label("Pipeline").classes("text-2xl font-bold")
    ui.label("Use the dropdown on each card to move it to a new stage.").style(
        f"color:{GRAY};"
    ).classes("mb-2")

    with ui.tabs().classes("w-full") as tabs:
        brand_tab = ui.tab("Brands")
        creator_tab = ui.tab("Creators")

    with ui.tab_panels(tabs, value=brand_tab).classes("w-full").style("background: transparent;"):
        with ui.tab_panel(brand_tab):
            render_pipeline_board(
                stages=BRAND_STAGES,
                fetch_all=brand_service.get_all_brands,
                get_name=lambda b: b.brand_name,
                get_subtitle=lambda b: b.contact_name,
                update_stage=lambda id_, stage: brand_service.update_brand(id_, {"stage": stage}),
            )
        with ui.tab_panel(creator_tab):
            render_pipeline_board(
                stages=CREATOR_STAGES,
                fetch_all=creator_service.get_all_creators,
                get_name=lambda c: c.name,
                get_subtitle=lambda c: c.niche,
                update_stage=lambda id_, stage: creator_service.update_creator(id_, {"stage": stage}),
            )


def render_pipeline_board(stages, fetch_all, get_name, get_subtitle, update_stage):
    board = ui.row().classes("gap-3 items-start overflow-x-auto w-full pb-4")

    def refresh():
        board.clear()
        all_items = fetch_all()
        with board:
            for stage in stages:
                stage_items = [i for i in all_items if i.stage == stage]
                color = get_stage_color(stage)

                with ui.column().classes("min-w-[260px] gap-2").style(
                    f"background-color:{CARD_ALT}; border:1px solid {BORDER}; "
                    f"border-radius:14px; padding:12px;"
                ):
                    with ui.row().classes("items-center justify-between w-full"):
                        ui.label(stage).classes("font-bold text-sm").style(f"color:{TEXT};")
                        ui.html(
                            f'<span style="background:{color}1A; color:{color}; '
                            f'padding:2px 9px; border-radius:999px; font-size:11px; '
                            f'font-weight:700; border:1px solid {color}33;">{len(stage_items)}</span>'
                        )

                    if not stage_items:
                        ui.label("Empty").style(f"color:{GRAY}; font-size:12px;").classes("py-2")

                    for item in stage_items:
                        with ui.card().classes("w-full p-3 gap-2"):
                            with ui.row().classes("items-center gap-2 w-full"):
                                initials_avatar(get_name(item), color=color)
                                with ui.column().classes("gap-0"):
                                    ui.label(get_name(item)).classes("font-semibold text-sm").style(
                                        f"color:{TEXT};"
                                    )
                                    subtitle = get_subtitle(item)
                                    if subtitle:
                                        ui.label(subtitle).style(f"color:{GRAY}; font-size:11px;")

                            def make_handler(item_id):
                                def handler(e):
                                    update_stage(item_id, e.args)
                                    ui.notify(f"Moved to {e.args}", color="positive")
                                    refresh()
                                return handler

                            ui.select(stages, value=item.stage).classes("w-full").props(
                                "dense outlined"
                            ).on("update:model-value", make_handler(item.id))

    refresh()