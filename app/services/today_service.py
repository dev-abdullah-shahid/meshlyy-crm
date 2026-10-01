# app/services/today_service.py
#
# Computes the four "Today" sections by looking at existing Brand/Creator
# data. No new tables — this just filters/sorts what's already there.

from datetime import date
from app.services.brand_service import get_all_brands
from app.services.creator_service import get_all_creators

# Stages we consider "closing actions" — later-stage, high-effort steps.
BRAND_CLOSING_STAGES = {
    "Audit Offered", "Audit Completed", "Campaign Discussion", "Payment Pending"
}
CREATOR_CLOSING_STAGES = {
    "Application", "Verification", "Approved", "Campaign Matched"
}

# Stages we consider "dead" — not shown anywhere on Today.
BRAND_CLOSED_STAGES = {"Lost", "Not Now", "No Response", "Not A Fit", "Active Client"}
CREATOR_CLOSED_STAGES = {"Active Creator"}


def _is_overdue_or_today(next_action_date: str) -> bool:
    """
    Returns True if next_action_date is today or in the past.
    Dates are stored as plain text (YYYY-MM-DD), so we parse carefully
    and just skip anything that isn't a valid date instead of crashing.
    """
    if not next_action_date:
        return False
    try:
        parsed = date.fromisoformat(next_action_date.strip())
    except ValueError:
        return False
    return parsed <= date.today()


def get_today_data():
    """
    Returns a dict with four lists: new_prospects, replies, follow_ups, closing_actions.
    Each item is a dict with enough info to display on the Today page,
    plus 'lead_type' and 'id' so we can link back to the right record.
    """
    brands = [b for b in get_all_brands() if b.stage not in BRAND_CLOSED_STAGES]
    creators = [c for c in get_all_creators() if c.stage not in CREATOR_CLOSED_STAGES]

    new_prospects = []
    replies = []
    follow_ups = []
    closing_actions = []

    for b in brands:
        item = {
            "lead_type": "brand", "id": b.id, "name": b.brand_name,
            "stage": b.stage, "next_action": b.next_action,
            "next_action_date": b.next_action_date,
        }
        if not b.first_contact:
            new_prospects.append(item)
        if b.stage == "Replied":
            replies.append(item)
        if _is_overdue_or_today(b.next_action_date):
            follow_ups.append(item)
        if b.stage in BRAND_CLOSING_STAGES:
            closing_actions.append(item)

    for c in creators:
        item = {
            "lead_type": "creator", "id": c.id, "name": c.name,
            "stage": c.stage, "next_action": c.next_action,
            "next_action_date": c.next_action_date,
        }
        if not c.first_contact:
            new_prospects.append(item)
        if c.stage == "Replied":
            replies.append(item)
        if _is_overdue_or_today(c.next_action_date):
            follow_ups.append(item)
        if c.stage in CREATOR_CLOSING_STAGES:
            closing_actions.append(item)

    return {
        "new_prospects": new_prospects,
        "replies": replies,
        "follow_ups": follow_ups,
        "closing_actions": closing_actions,
    }