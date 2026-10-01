# app/services/campaign_service.py
#
# CRUD functions for Campaign, following the same pattern as brand_service
# and creator_service.

from app.database import SessionLocal
from app.models.campaign import Campaign


def get_all_campaigns(status: str = ""):
    db = SessionLocal()
    query = db.query(Campaign)
    if status:
        query = query.filter(Campaign.status == status)
    results = query.order_by(Campaign.created_at.desc()).all()
    db.close()
    return results


def get_campaign_by_id(campaign_id: int):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    db.close()
    return campaign


def create_campaign(data: dict):
    db = SessionLocal()
    campaign = Campaign(**data)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    db.close()
    return campaign


def update_campaign(campaign_id: int, data: dict):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if campaign:
        for key, value in data.items():
            setattr(campaign, key, value)
        db.commit()
    db.close()


def delete_campaign(campaign_id: int):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if campaign:
        db.delete(campaign)
        db.commit()
    db.close()


def count_active_campaigns():
    """
    'Active' = not yet Completed and not yet Results Delivered.
    Used by the Dashboard.
    """
    db = SessionLocal()
    count = (
        db.query(Campaign)
        .filter(~Campaign.status.in_(["Completed", "Results Delivered"]))
        .count()
    )
    db.close()
    return count