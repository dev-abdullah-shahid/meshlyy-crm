# app/services/brand_service.py
#
# All functions for creating, reading, updating, and deleting Brands.
# The UI (pages/brands.py) calls these functions — it never touches
# the database directly. This keeps things organized and easier to debug.

from app.database import SessionLocal
from app.models.brand import Brand


def get_all_brands(search: str = "", stage: str = "", category: str = "",
                    lead_source: str = "", min_lead_score: int = None):
    """
    Returns a list of brands, optionally filtered by search text, stage,
    category, lead source, and a minimum lead score.
    """
    db = SessionLocal()
    query = db.query(Brand)

    if search:
        # Case-insensitive search on brand_name
        query = query.filter(Brand.brand_name.ilike(f"%{search}%"))

    if stage:
        query = query.filter(Brand.stage == stage)

    if category:
        query = query.filter(Brand.category == category)

    if lead_source:
        query = query.filter(Brand.lead_source == lead_source)

    if min_lead_score is not None:
        query = query.filter(Brand.lead_score >= min_lead_score)

    results = query.order_by(Brand.created_at.desc()).all()
    db.close()
    return results


def get_brand_by_id(brand_id: int):
    db = SessionLocal()
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    db.close()
    return brand


def create_brand(data: dict):
    """
    Creates a new brand from a dictionary of field values.
    """
    db = SessionLocal()
    brand = Brand(**data)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    db.close()
    return brand


def update_brand(brand_id: int, data: dict):
    """
    Updates an existing brand's fields with new values.
    """
    db = SessionLocal()
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if brand:
        for key, value in data.items():
            setattr(brand, key, value)
        db.commit()
    db.close()


def delete_brand(brand_id: int):
    db = SessionLocal()
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if brand:
        db.delete(brand)
        db.commit()
    db.close()


def get_all_categories():
    """Returns a sorted list of distinct, non-empty categories currently in use."""
    db = SessionLocal()
    rows = db.query(Brand.category).distinct().all()
    db.close()
    return sorted({r[0] for r in rows if r[0]})

def get_all_lead_sources():
    """Returns a sorted list of distinct, non-empty lead sources currently in use."""
    db = SessionLocal()
    rows = db.query(Brand.lead_source).distinct().all()
    db.close()
    return sorted({r[0] for r in rows if r[0]})