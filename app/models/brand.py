# app/models/brand.py
#
# This file defines the "Brand" table.
# Each class attribute below becomes a column in the database table.

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Brand(Base):
    __tablename__ = "brands"

    # Primary key — a unique ID that auto-increments for every new brand.
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core identity
    brand_name = Column(String, nullable=False)   # required field
    contact_name = Column(String, default="")
    role = Column(String, default="")

    # Contact / social info
    instagram = Column(String, default="")
    linkedin = Column(String, default="")
    email = Column(String, default="")
    website = Column(String, default="")

    # Business info
    category = Column(String, default="")
    city = Column(String, default="")
    followers = Column(String, default="Unknown")  # text, not a number — see note below
    influencer_campaigns_before = Column(String, default="Unknown")
    estimated_marketing_spend = Column(String, default="Unknown")

    # Acquisition tracking
    lead_source = Column(String, default="")
    assigned_to = Column(String, default="")
    stage = Column(String, default="New")
    lead_score = Column(Integer, default=0)

    # Outreach timeline
    first_contact = Column(String, default="")       # stored as text date for simplicity
    last_contact = Column(String, default="")
    next_action = Column(String, default="")
    next_action_date = Column(String, default="")
    message_number = Column(String, default="")

    notes = Column(String, default="")

    # Timestamps — auto-filled by Python, not the user
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)