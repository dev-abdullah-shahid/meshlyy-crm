# app/services/demo_service.py
#
# Loads and deletes DEMO DATA — clearly separate from real prospects.
# We tag every demo row's lead_source as "DEMO DATA" so we can find
# and delete exactly those rows later, without touching real data.

from app.database import SessionLocal
from app.models.brand import Brand
from app.models.creator import Creator

DEMO_TAG = "DEMO DATA"

DEMO_BRANDS = [
    {"brand_name": "Aurora Apparel", "contact_name": "Sara Khan", "category": "Fashion",
     "city": "Lahore", "stage": "New", "lead_source": DEMO_TAG, "lead_score": 6},
    {"brand_name": "Bloom Skincare", "contact_name": "Ali Raza", "category": "Beauty",
     "city": "Karachi", "stage": "Contacted", "lead_source": DEMO_TAG, "lead_score": 8},
    {"brand_name": "Crestline Fitness", "contact_name": "Meher Iqbal", "category": "Fitness",
     "city": "Islamabad", "stage": "Interested", "lead_source": DEMO_TAG, "lead_score": 9},
]

DEMO_CREATORS = [
    {"name": "Zara Vlogs", "niche": "Lifestyle", "city": "Lahore",
     "stage": "New", "lead_source": DEMO_TAG, "verification_status": "Unverified"},
    {"name": "Fit With Faraz", "niche": "Fitness", "city": "Karachi",
     "stage": "Contacted", "lead_source": DEMO_TAG, "verification_status": "Pending"},
    {"name": "Beauty By Bisma", "niche": "Beauty", "city": "Islamabad",
     "stage": "Verified", "lead_source": DEMO_TAG, "verification_status": "Verified"},
]


def load_demo_data():
    db = SessionLocal()
    for data in DEMO_BRANDS:
        db.add(Brand(**data))
    for data in DEMO_CREATORS:
        db.add(Creator(**data))
    db.commit()
    db.close()


def delete_demo_data():
    db = SessionLocal()
    db.query(Brand).filter(Brand.lead_source == DEMO_TAG).delete()
    db.query(Creator).filter(Creator.lead_source == DEMO_TAG).delete()
    db.commit()
    db.close()


def count_demo_data():
    db = SessionLocal()
    b = db.query(Brand).filter(Brand.lead_source == DEMO_TAG).count()
    c = db.query(Creator).filter(Creator.lead_source == DEMO_TAG).count()
    db.close()
    return b, c