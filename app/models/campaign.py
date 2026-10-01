# app/models/campaign.py
#
# Defines the "Campaign" table. A campaign links one Brand to one Creator.
#
# We store budget as text (like followers/spend elsewhere) to honor our
# data safety rule: if the budget isn't finalized yet, we store "Unknown"
# or leave it blank rather than guessing a number.

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Links to the Brand and Creator tables by their id.
    brand_id = Column(Integer, nullable=False)
    creator_id = Column(Integer, nullable=False)

    campaign_name = Column(String, nullable=False)
    budget = Column(String, default="Unknown")
    status = Column(String, default="Proposed")

    start_date = Column(String, default="")
    end_date = Column(String, default="")
    results = Column(String, default="")
    notes = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)