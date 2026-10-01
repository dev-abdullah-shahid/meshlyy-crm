# app/components/theme.py
#
# Meshlyy's design system v2: a minimal, high-end blue/white theme.
# Change colors here and the whole app updates — pages don't hardcode colors.

from nicegui import ui

# --- Palette: minimal blue/white ---
BG = "#F5F7FB"          # page background — soft off-white, not stark white
CARD = "#FFFFFF"         # card background
CARD_ALT = "#F8FAFD"     # nested surfaces (pipeline columns, etc.)
BORDER = "#E4E9F2"       # hairline borders

PRIMARY = "#2563EB"      # main blue — buttons, active states, links
PRIMARY_LIGHT = "#60A5FA"
ACCENT = "#0EA5E9"       # secondary sky-blue accent

TEXT = "#0F172A"         # near-black navy for body text
GRAY = "#64748B"         # muted secondary text

GREEN = "#059669"
AMBER = "#D97706"
RED = "#DC2626"


def apply_theme():
    """Sets Quasar's color palette + injects global CSS. Call once per page."""
    ui.colors(
        primary=PRIMARY,
        secondary=ACCENT,
        accent=ACCENT,
        positive=GREEN,
        negative=RED,
        warning=AMBER,
    )
    ui.dark_mode().disable()

    ui.add_head_html(f"""
    <style>
        * {{
            transition: background-color .18s ease, border-color .18s ease,
                        box-shadow .2s ease, transform .18s ease, color .15s ease;
        }}

        body, .q-page, .nicegui-content {{
            background-color: {BG} !important;
            color: {TEXT};
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        .nicegui-content {{
            animation: fadeInUp .35s ease both;
        }}

        /* Cards: soft shadow at rest, lift + stronger shadow on hover */
        .q-card {{
            background-color: {CARD} !important;
            color: {TEXT} !important;
            border: 1px solid {BORDER};
            border-radius: 14px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
        }}
        .q-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.12), 0 4px 10px rgba(15, 23, 42, 0.06);
            border-color: {PRIMARY_LIGHT};
        }}

        /* Tables */
        .q-table {{
            background-color: {CARD} !important;
            color: {TEXT} !important;
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid {BORDER};
        }}
        .q-table thead th {{
            color: {PRIMARY} !important;
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            background-color: {CARD_ALT} !important;
        }}
        .q-table tbody tr {{
            transition: background-color .12s ease;
        }}
        .q-table tbody tr:hover {{
            background-color: #EFF4FE !important;
            cursor: pointer;
        }}

        /* Inputs */
        .q-field__control, .q-field__native, .q-field__label {{
            color: {TEXT} !important;
        }}
        .q-field--outlined .q-field__control {{
            border-radius: 10px;
            background-color: {CARD};
        }}
        .q-field--focused .q-field__control {{
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }}

        /* Buttons: depth + lift on hover, everywhere in the app */
        .q-btn {{
            border-radius: 10px;
            font-weight: 600;
            letter-spacing: 0.01em;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
        }}
        .q-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25);
        }}
        .q-btn:active {{
            transform: translateY(0px) scale(0.98);
        }}

        a {{
            color: {PRIMARY} !important;
            font-weight: 500;
        }}

        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: {BG}; }}
        ::-webkit-scrollbar-thumb {{ background: {PRIMARY_LIGHT}; border-radius: 4px; }}
    </style>
    """)


# ---------- Stage color logic (used by badges everywhere) ----------

def get_stage_color(stage: str) -> str:
    """Buckets any stage string into one of 4 semantic colors."""
    s = (stage or "").lower()
    lost_words = ["lost", "not now", "no response", "not a fit"]
    won_words = ["paying", "active client", "active creator", "completed",
                 "results delivered", "verified", "paid", "live"]
    pending_words = ["pending", "audit", "campaign discussion", "application",
                      "verification", "approved", "proposed", "selected",
                      "in progress"]

    if any(w in s for w in lost_words):
        return RED
    if any(w in s for w in won_words):
        return GREEN
    if any(w in s for w in pending_words):
        return AMBER
    if s in ("new", "qualified"):
        return GRAY
    return PRIMARY  # contacted / replied / interested / default


def stage_badge(stage: str):
    """A small rounded pill showing the stage name in its semantic color."""
    color = get_stage_color(stage)
    ui.html(
        f'<span style="background:{color}1A; color:{color}; padding:3px 12px; '
        f'border-radius:999px; font-size:11px; font-weight:700; '
        f'white-space:nowrap; border:1px solid {color}33;">{stage}</span>'
    )


def initials_avatar(name: str, color: str = None):
    """A small circular avatar showing a person/brand's initials."""
    color = color or PRIMARY
    parts = (name or "?").split()
    letters = "".join(p[0] for p in parts[:2]).upper() or "?"
    ui.html(
        f'<div style="width:34px;height:34px;min-width:34px;border-radius:50%;'
        f'background:{color}1A; color:{color}; font-size:12px;font-weight:800;'
        f'border:1.5px solid {color}40;'
        f'display:flex;align-items:center;justify-content:center;">{letters}</div>'
    )