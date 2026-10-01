# app/models/activity.py
#
# Defines the "Activity" table — one row per outreach interaction
# (a DM sent, a reply received, a call made, etc).

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Which prospect this activity belongs to.
    # lead_type is either "brand" or "creator", lead_id is that record's id.
    lead_type = Column(String, nullable=False)   # "brand" or "creator"
    lead_id = Column(Integer, nullable=False)

    activity_type = Column(String, default="")       # e.g. "Instagram DM", "Email", "Call"
    message_number = Column(String, default="")       # e.g. "M1", "M2"
    message_text = Column(String, default="")
    result = Column(String, default="")                # e.g. "No response", "Replied", "Interested"

    next_action = Column(String, default="")
    next_action_date = Column(String, default="")

    notes = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)