# app/services/dashboard_service.py
#
# Computes all the numbers shown on the Dashboard.
# Everything here reads from existing Brand/Creator/Activity data —
# no new tables, no fabricated numbers.
from app.services.campaign_service import count_active_campaigns
from app.services.brand_service import get_all_brands
from app.services.creator_service import get_all_creators
from app.services.activity_service import get_all_activities

# Stage groupings used for the summary counts.
# Defined once here so the whole dashboard stays consistent.
BRAND_AUDIT_STAGES = {"Audit Offered", "Audit Completed"}
BRAND_SIGNUP_STAGES = {"Payment Pending", "Paying", "Active Client"}
BRAND_PAYING_STAGES = {"Paying", "Active Client"}


def get_summary_counts():
    """
    Returns the top-row summary numbers shown on the dashboard.
    """
    brands = get_all_brands()
    creators = get_all_creators()
    activities = get_all_activities(limit=100000)  # effectively "all"

    new_prospects = sum(1 for b in brands if not b.first_contact) + \
                     sum(1 for c in creators if not c.first_contact)

    messages_sent = len(activities)
    replies = sum(1 for a in activities if a.result == "Replied")

    interested = sum(1 for b in brands if b.stage == "Interested") + \
                 sum(1 for c in creators if c.stage == "Interested")

    audits = sum(1 for b in brands if b.stage in BRAND_AUDIT_STAGES)
    applications = sum(1 for c in creators if c.stage == "Application")
    signups = sum(1 for b in brands if b.stage in BRAND_SIGNUP_STAGES)
    paying_brands = sum(1 for b in brands if b.stage in BRAND_PAYING_STAGES)
    verified_creators = sum(1 for c in creators if c.stage == "Verified" or c.verification_status == "Verified")

    # Campaigns don't exist yet (Phase 10) — show 0 honestly rather than fake data.
    active_campaigns = count_active_campaigns()

    return {
        "new_prospects": new_prospects,
        "messages_sent": messages_sent,
        "replies": replies,
        "interested": interested,
        "audits": audits,
        "applications": applications,
        "signups": signups,
        "paying_brands": paying_brands,
        "verified_creators": verified_creators,
        "active_campaigns": active_campaigns,
    }


def get_brand_pipeline_counts():
    """Returns {stage: count} for brands, only including stages with at least 1 brand."""
    brands = get_all_brands()
    counts = {}
    for b in brands:
        counts[b.stage] = counts.get(b.stage, 0) + 1
    return counts


def get_creator_pipeline_counts():
    """Returns {stage: count} for creators, only including stages with at least 1 creator."""
    creators = get_all_creators()
    counts = {}
    for c in creators:
        counts[c.stage] = counts.get(c.stage, 0) + 1
    return counts


def _safe_rate(numerator: int, denominator: int) -> float:
    """
    Returns numerator/denominator as a percentage, safely handling
    division by zero. If there's no data, we return 0 — never a fake
    or guessed number.
    """
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100, 1)


def get_metrics():
    """
    Returns the five conversion rates as percentages, computed from
    the same summary counts used on the dashboard's Overview section.
    """
    summary = get_summary_counts()

    reply_rate = _safe_rate(summary["replies"], summary["messages_sent"])
    interest_rate = _safe_rate(summary["interested"], summary["replies"])
    audit_rate = _safe_rate(summary["audits"], summary["interested"])
    signup_rate = _safe_rate(summary["signups"], summary["audits"])
    paid_conversion = _safe_rate(summary["paying_brands"], summary["signups"])

    return {
        "reply_rate": reply_rate,
        "interest_rate": interest_rate,
        "audit_rate": audit_rate,
        "signup_rate": signup_rate,
        "paid_conversion": paid_conversion,
    }