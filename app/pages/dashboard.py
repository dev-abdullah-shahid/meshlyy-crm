# app/pages/dashboard.py
#
# The main Dashboard page — icon-based summary stats, pipeline counts,
# and metrics.

from nicegui import ui
from app.services import dashboard_service
from app.components.theme import TEXT, GRAY, PRIMARY, GREEN, AMBER, ACCENT

STAT_CONFIG = [
    ("new_prospects", "New Prospects", "person_add", PRIMARY),
    ("messages_sent", "Messages Sent", "send", PRIMARY),
    ("replies", "Replies", "reply", PRIMARY),
    ("interested", "Interested", "favorite", ACCENT),
    ("audits", "Audits", "fact_check", AMBER),
    ("applications", "Applications", "assignment", AMBER),
    ("signups", "Signups", "how_to_reg", AMBER),
    ("paying_brands", "Paying Brands", "attach_money", GREEN),
    ("verified_creators", "Verified Creators", "verified", GREEN),
    ("active_campaigns", "Active Campaigns", "campaign", ACCENT),
]


def stat_card(label: str, value: int, icon: str, color: str):
    with ui.card().classes("p-4 min-w-[190px]").style(f"border-top: 3px solid {color};"):
        with ui.row().classes("items-center gap-3"):
            ui.html(
                f'<div style="width:38px;height:38px;border-radius:11px;'
                f'background:{color}14;display:flex;align-items:center;'
                f'justify-content:center;">'
                f'<span class="material-icons" style="color:{color};font-size:20px;">{icon}</span>'
                f'</div>'
            )
            with ui.column().classes("gap-0"):
                ui.label(str(value)).classes("text-2xl font-bold").style(f"color:{TEXT};")
                ui.label(label).classes("text-xs").style(f"color:{GRAY};")


def metric_card(label: str, percent: float):
    with ui.card().classes("p-4 min-w-[160px]"):
        ui.label(f"{percent}%").classes("text-3xl font-bold").style(f"color:{GREEN};")
        ui.label(label).classes("text-sm").style(f"color:{GRAY};")


def pipeline_column(title: str, counts: dict):
    with ui.card().classes("p-4 min-w-[260px]"):
        ui.label(title).classes("font-bold text-sm mb-2").style(f"color:{PRIMARY};")
        if not counts:
            ui.label("No data yet.").style(f"color:{GRAY}; font-size:13px;")
        else:
            for stage, count in counts.items():
                with ui.row().classes("justify-between w-full py-1"):
                    ui.label(stage).style(f"color:{TEXT}; font-size:13px;")
                    ui.label(str(count)).classes("font-semibold").style(f"color:{PRIMARY};")


def dashboard_page():
    ui.label("Dashboard").classes("text-2xl font-bold")
    ui.label("Your acquisition funnel at a glance.").style(f"color:{GRAY};").classes("mb-2")

    summary = dashboard_service.get_summary_counts()

    ui.label("Overview").classes("text-lg font-semibold mt-4 mb-2")
    with ui.row().classes("gap-4 flex-wrap"):
        for key, label, icon, color in STAT_CONFIG:
            stat_card(label, summary[key], icon, color)

    ui.label("Pipeline").classes("text-lg font-semibold mt-6 mb-2")
    with ui.row().classes("gap-4 flex-wrap"):
        pipeline_column("BRANDS", dashboard_service.get_brand_pipeline_counts())
        pipeline_column("CREATORS", dashboard_service.get_creator_pipeline_counts())

    ui.label("Metrics").classes("text-lg font-semibold mt-6 mb-2")
    metrics = dashboard_service.get_metrics()
    with ui.row().classes("gap-4 flex-wrap"):
        metric_card("Reply Rate", metrics["reply_rate"])
        metric_card("Interest Rate", metrics["interest_rate"])
        metric_card("Audit Rate", metrics["audit_rate"])
        metric_card("Signup Rate", metrics["signup_rate"])
        metric_card("Paid Conversion", metrics["paid_conversion"])