# app/main.py
#
# Entry point of the application. Sets up:
# - simple password protection (for production use)
# - left sidebar navigation
# - all page routes
# - host/port binding that works both locally and on Render

import os
import base64
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from nicegui import ui, app
from app.database import init_db
from app.components.theme import apply_theme, CARD, BORDER, PRIMARY, TEXT, GRAY
from app.pages.brands import brands_page
from app.pages.creators import creators_page
from app.pages.pipeline import pipeline_page
from app.pages.activity import activity_log_page
from app.pages.today import today_page
from app.pages.dashboard import dashboard_page
from app.pages.campaigns import campaigns_page
from app.pages.messages import messages_page
from app.pages.settings import settings_page

init_db()

# --- Simple password protection for production ---
# Reads credentials from environment variables so the real password
# never lives in the code itself. Locally, these fall back to defaults
# so you don't need to set anything to keep developing on localhost.
APP_USERNAME = os.environ.get("MESHLYY_USERNAME", "meshlyy")
APP_PASSWORD = os.environ.get("MESHLYY_PASSWORD", "changeme-locally")


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """
    Checks every request for a valid username/password using HTTP Basic
    Auth — the browser shows its own native login popup. Simple and
    reliable, good enough for an internal V1 tool.
    """
    async def dispatch(self, request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                scheme, credentials = auth_header.split()
                if scheme.lower() == "basic":
                    decoded = base64.b64decode(credentials).decode("utf-8")
                    username, password = decoded.split(":", 1)
                    if username == APP_USERNAME and password == APP_PASSWORD:
                        return await call_next(request)
            except Exception:
                pass  # falls through to the 401 below

        return Response(
            content="Authentication required.",
            status_code=401,
            headers={"WWW-Authenticate": 'Basic realm="Meshlyy"'},
        )


app.add_middleware(BasicAuthMiddleware)

# (label, path, Material icon name)
NAV_LINKS = [
    ("Dashboard", "/dashboard", "dashboard"),
    ("Today", "/today", "today"),
    ("Brands", "/brands", "storefront"),
    ("Creators", "/creators", "people"),
    ("Pipeline", "/pipeline", "insights"),
    ("Activity", "/activity", "history"),
    ("Campaigns", "/campaigns", "campaign"),
    ("Messages", "/messages", "forum"),
    ("Settings", "/settings", "settings"),
]


def show_navigation(active: str = ""):
    apply_theme()

    with ui.left_drawer(fixed=True).style(
        f"background-color:{CARD}; border-right:1px solid {BORDER};"
    ).props("width=240"):
        with ui.column().classes("p-4 gap-1 w-full"):
            with ui.row().classes("items-center gap-2 mb-1"):
                ui.html(
                    f'<div style="width:30px;height:30px;border-radius:9px;'
                    f'background:{PRIMARY};display:flex;align-items:center;'
                    f'justify-content:center;color:white;font-weight:800;'
                    f'font-size:14px;">M</div>'
                )
                ui.label("Meshlyy").classes("text-lg font-bold").style(f"color:{TEXT};")
            ui.label("Acquisition OS").classes("text-xs mb-4").style(f"color:{GRAY};")

            for label, path, icon in NAV_LINKS:
                is_active = active == path
                with ui.link(target=path).style("text-decoration:none; width:100%;"):
                    with ui.row().classes("items-center gap-3 w-full px-3 py-2").style(
                        f"border-radius:10px; "
                        f"background-color:{PRIMARY if is_active else 'transparent'}; "
                    ):
                        ui.icon(icon).style(
                            f"color:{'white' if is_active else GRAY}; font-size:20px;"
                        )
                        ui.label(label).style(
                            f"color:{'white' if is_active else TEXT}; font-size:14px; "
                            f"font-weight:{'700' if is_active else '500'};"
                        )


@ui.page("/")
def home_page():
    show_navigation()
    with ui.column().classes("w-full p-6"):
        ui.label("Meshlyy Acquisition OS").classes("text-2xl font-bold")
        ui.label("Internal client acquisition system.").style(f"color: {GRAY};")
        with ui.row().classes("gap-4 mt-4"):
            for label, path, _ in NAV_LINKS:
                ui.link(f"Go to {label}", path)


@ui.page("/dashboard")
def dashboard_route():
    show_navigation("/dashboard")
    with ui.column().classes("w-full p-6"):
        dashboard_page()


@ui.page("/today")
def today_route():
    show_navigation("/today")
    with ui.column().classes("w-full p-6"):
        today_page()


@ui.page("/brands")
def brands_route():
    show_navigation("/brands")
    with ui.column().classes("w-full p-6"):
        brands_page()


@ui.page("/creators")
def creators_route():
    show_navigation("/creators")
    with ui.column().classes("w-full p-6"):
        creators_page()


@ui.page("/pipeline")
def pipeline_route():
    show_navigation("/pipeline")
    with ui.column().classes("w-full p-6"):
        pipeline_page()


@ui.page("/activity")
def activity_route():
    show_navigation("/activity")
    with ui.column().classes("w-full p-6"):
        activity_log_page()


@ui.page("/campaigns")
def campaigns_route():
    show_navigation("/campaigns")
    with ui.column().classes("w-full p-6"):
        campaigns_page()


@ui.page("/messages")
def messages_route():
    show_navigation("/messages")
    with ui.column().classes("w-full p-6"):
        messages_page()


@ui.page("/settings")
def settings_route():
    show_navigation("/settings")
    with ui.column().classes("w-full p-6"):
        settings_page()


ui.run(
    title="Meshlyy Acquisition OS",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
)