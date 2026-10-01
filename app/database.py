# app/database.py
#
# This file sets up the connection to our SQLite database.
# Every other file that needs to talk to the database imports from here.
#
# DATABASE_PATH is read from an environment variable so the same code
# works both locally (data/meshlyy.db) and on Render (a persistent disk
# path like /var/data/meshlyy.db) without changing anything by hand.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Locally this defaults to "data/meshlyy.db" (same as before — nothing
# changes for local development). On Render, we set DATABASE_PATH to
# point at the persistent disk so data survives redeploys.
DB_PATH = os.environ.get("DATABASE_PATH", "data/meshlyy.db")

# Make sure the folder for the database file actually exists before
# SQLite tries to create/open the file inside it.
db_dir = os.path.dirname(DB_PATH)
if db_dir:
    os.makedirs(db_dir, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

# The "engine" is SQLAlchemy's connection to the database file.
# echo=False means it won't print every SQL command it runs.
engine = create_engine(DATABASE_URL, echo=False)

# Base is the parent class that all our table models (Brand, Creator, etc.)
# inherit from. It's how SQLAlchemy knows "this Python class = a database table".
Base = declarative_base()

# SessionLocal is a factory that creates new "sessions" — temporary
# workspaces where you make changes before saving ("committing") them.
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """
    Creates all tables in the database, based on the models we've defined.
    Safe to run multiple times — it only creates tables that don't exist yet.
    """
    Base.metadata.create_all(bind=engine)