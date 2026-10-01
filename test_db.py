# test_db.py
#
# A simple script to test that we can Create, Read, Update, and Delete a Brand.
# Run this from the terminal with: python test_db.py

from app.database import init_db, SessionLocal
from app.models.brand import Brand

# Step 1: Make sure the "brands" table exists in the database.
init_db()

# Step 2: Open a session (our workspace for talking to the database).
db = SessionLocal()

# ---- CREATE ----
new_brand = Brand(
    brand_name="Test Clothing Co",
    contact_name="Jane Doe",
    category="Fashion",
    city="Lahore",
    stage="New",
)
db.add(new_brand)       # stage the new brand for saving
db.commit()              # actually save it to the database file
db.refresh(new_brand)    # reload it so we get its auto-generated id
print("CREATED:", new_brand.id, new_brand.brand_name)

# ---- READ ----
found = db.query(Brand).filter(Brand.id == new_brand.id).first()
print("READ:", found.brand_name, "| stage:", found.stage)

# ---- UPDATE ----
found.stage = "Contacted"
db.commit()
updated = db.query(Brand).filter(Brand.id == new_brand.id).first()
print("UPDATED stage to:", updated.stage)

# ---- DELETE ----
db.delete(updated)
db.commit()
still_there = db.query(Brand).filter(Brand.id == new_brand.id).first()
print("AFTER DELETE, found:", still_there)  # should print: None

db.close()