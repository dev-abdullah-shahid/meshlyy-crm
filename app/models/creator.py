# app/models/creator.py
#
# Defines the "Creator" table — same structure style as Brand.

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Creator(Base):
    __tablename__ = "creators"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core identity
    name = Column(String, nullable=False)
    instagram = Column(String, default="")
    tiktok = Column(String, default="")
    email = Column(String, default="")
    city = Column(String, default="")

    # Creator-specific info
    niche = Column(String, default="")
    followers = Column(String, default="Unknown")        # text on purpose — see Brand notes
    engagement = Column(String, default="Unknown")
    brand_deals_before = Column(String, default="Unknown")

    # Acquisition tracking
    lead_source = Column(String, default="")
    assigned_to = Column(String, default="")
    stage = Column(String, default="New")

    # Outreach timeline
    first_contact = Column(String, default="")
    last_contact = Column(String, default="")
    next_action = Column(String, default="")
    next_action_date = Column(String, default="")
    message_number = Column(String, default="")

    verification_status = Column(String, default="Unverified")

    notes = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)