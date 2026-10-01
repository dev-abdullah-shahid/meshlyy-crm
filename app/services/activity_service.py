# app/services/activity_service.py
#
# Handles creating and listing activities, and — importantly —
# updating the related Brand or Creator when a new activity is logged.

from datetime import date
from app.database import SessionLocal
from app.models.activity import Activity
from app.models.brand import Brand
from app.models.creator import Creator


def get_activities_for_lead(lead_type: str, lead_id: int):
    """All activities for one specific brand or creator, newest first."""
    db = SessionLocal()
    results = (
        db.query(Activity)
        .filter(Activity.lead_type == lead_type, Activity.lead_id == lead_id)
        .order_by(Activity.created_at.desc())
        .all()
    )
    db.close()
    return results


def get_all_activities(limit: int = 200):
    """All activities across brands and creators, newest first."""
    db = SessionLocal()
    results = db.query(Activity).order_by(Activity.created_at.desc()).limit(limit).all()
    db.close()
    return results


def log_activity(lead_type: str, lead_id: int, data: dict):
    """
    Creates a new Activity record, AND updates the related brand/creator's
    last_contact, next_action, next_action_date (and first_contact if it's empty).

    This is the one place that keeps "activity history" and "current status"
    in sync, so the rest of the app doesn't have to think about it.
    """
    db = SessionLocal()

    activity = Activity(lead_type=lead_type, lead_id=lead_id, **data)
    db.add(activity)

    today_str = date.today().isoformat()  # e.g. "2026-09-24"

    # Find the related brand or creator and update its tracking fields.
    if lead_type == "brand":
        lead = db.query(Brand).filter(Brand.id == lead_id).first()
    else:
        lead = db.query(Creator).filter(Creator.id == lead_id).first()

    if lead:
        if not lead.first_contact:
            lead.first_contact = today_str
        lead.last_contact = today_str
        if data.get("message_number"):
            lead.message_number = data["message_number"]
        if data.get("next_action"):
            lead.next_action = data["next_action"]
        if data.get("next_action_date"):
            lead.next_action_date = data["next_action_date"]

    db.commit()
    db.close()