# app/models/message_template.py
#
# Static outreach message templates. Not a database table on purpose —
# these are fixed scripts you copy and personalize manually, not data
# you'll be editing through forms in V1.

BRAND_TEMPLATES = {
    "M1 — Observation": (
        "Hi [Contact Name], I came across [Brand Name] and noticed [specific "
        "observation about their content/product]. Really liked [specific detail]."
    ),
    "M2 — Insight": (
        "Following up — I looked closer at your recent [campaign/posts] and noticed "
        "[specific insight]. Thought it might be useful to share."
    ),
    "M3 — Platform Introduction": (
        "Quick intro: we're Meshlyy, we help brands like [Brand Name] connect with "
        "vetted creators for [specific use case]. Happy to share more if useful."
    ),
    "M4 — Offer": (
        "We'd love to run a quick free audit of your current creator/influencer "
        "approach and show you where the gaps are — no cost, no obligation."
    ),
    "M5 — Follow-up": (
        "Just floating this back to the top of your inbox — still happy to share "
        "that audit whenever it's useful for you."
    ),
}

CREATOR_TEMPLATES = {
    "M1 — Recognition": (
        "Hi [Name], really enjoyed your recent content on [specific post/topic] — "
        "[specific compliment]."
    ),
    "M2 — Validation": (
        "Your engagement and content quality stood out to us — we work with brands "
        "looking for creators exactly like you."
    ),
    "M3 — Pioneer Invite": (
        "We're building out our early creator group at Meshlyy and would love to "
        "have you as one of the first — [specific benefit]."
    ),
    "M4 — Follow-up": (
        "Circling back on this — still think you'd be a great fit, let me know if "
        "you have any questions."
    ),
}