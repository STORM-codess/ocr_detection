# ocr/compare.py
from difflib import SequenceMatcher
import re

def clean_text(text):
    """Normalize text for reliable matching."""
    if not text:
        return None
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def similarity(a, b):
    """Fuzzy match similarity between two strings."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def compare_and_score(user, doc):
    """
    user: dict with 'name', 'dob', 'address'
    doc: dict with extracted fields

    returns:
      {
        status: "verified" / "failed",
        name_match: bool,
        dob_match: bool,
        address_confidence: float,
        document_details: extracted_doc_fields
      }
    """

    # Normalize all strings
    user_name = clean_text(user.get("name"))
    user_dob = clean_text(user.get("dob"))
    user_addr = clean_text(user.get("address"))

    doc_name = clean_text(doc.get("name"))
    doc_dob = clean_text(doc.get("dob"))
    doc_addr = clean_text(doc.get("address"))

    result = {
        "status": None,
        "name_match": False,
        "dob_match": False,
        "address_confidence": 0.0,
        "document_details": doc
    }

    # --- NAME MATCH ---
    if user_name and doc_name:
        result["name_match"] = (user_name == doc_name)

    # --- DOB MATCH ---
    if user_dob and doc_dob:
        result["dob_match"] = (user_dob == doc_dob)

    # If either fails → FAIL immediately
    if not (result["name_match"] and result["dob_match"]):
        result["status"] = "failed"
        return result

    # --- ADDRESS CONFIDENCE ---
    if user_addr and doc_addr:
        sim = similarity(user_addr, doc_addr)
    else:
        sim = 0.0

    result["address_confidence"] = round(sim, 2)
    result["status"] = "verified"

    return result
