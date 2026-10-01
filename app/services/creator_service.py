# app/services/creator_service.py
#
# Same CRUD pattern as brand_service.py, applied to Creator.

from app.database import SessionLocal
from app.models.creator import Creator


def get_all_creators(search: str = "", stage: str = "", niche: str = "", verification: str = ""):
    db = SessionLocal()
    query = db.query(Creator)

    if search:
        query = query.filter(Creator.name.ilike(f"%{search}%"))

    if stage:
        query = query.filter(Creator.stage == stage)

    if niche:
        query = query.filter(Creator.niche == niche)

    if verification:
        query = query.filter(Creator.verification_status == verification)

    results = query.order_by(Creator.created_at.desc()).all()
    db.close()
    return results


def get_creator_by_id(creator_id: int):
    db = SessionLocal()
    creator = db.query(Creator).filter(Creator.id == creator_id).first()
    db.close()
    return creator


def create_creator(data: dict):
    db = SessionLocal()
    creator = Creator(**data)
    db.add(creator)
    db.commit()
    db.refresh(creator)
    db.close()
    return creator


def update_creator(creator_id: int, data: dict):
    db = SessionLocal()
    creator = db.query(Creator).filter(Creator.id == creator_id).first()
    if creator:
        for key, value in data.items():
            setattr(creator, key, value)
        db.commit()
    db.close()


def delete_creator(creator_id: int):
    db = SessionLocal()
    creator = db.query(Creator).filter(Creator.id == creator_id).first()
    if creator:
        db.delete(creator)
        db.commit()
    db.close()


def get_all_niches():
    db = SessionLocal()
    rows = db.query(Creator.niche).distinct().all()
    db.close()
    return sorted({r[0] for r in rows if r[0]})