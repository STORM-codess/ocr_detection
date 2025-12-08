import streamlit as st
import tempfile
from ocr.extract import extract_clean_lines
from ocr.parser import extract_structured_fields
from ocr.compare import compare_fields

st.set_page_config(page_title="Document Verification Demo", layout="wide")

st.title("📄 Document Verification System (Phase 1 Demo)")

st.write("Upload a document and enter your details. The system will extract details from the ID and compare them to user input.")

# ---------------------
# STEP 1 – USER INPUT FORM
# ---------------------
st.header("Step 1: Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    user_name = st.text_input("Name")
    user_dob = st.text_input("Date of Birth (dd/mm/yyyy)")

with col2:
    user_address = st.text_area("Address")

# NORMALIZE inputs
user_details = {
    "name": user_name.lower().strip() if user_name else "",
    "dob": user_dob.lower().strip() if user_dob else "",
    "address": user_address.lower().strip() if user_address else ""
}

# ---------------------
# STEP 2 – FILE UPLOADER
# ---------------------
st.header("Step 2: Upload Document Image")
uploaded_file = st.file_uploader("Upload image (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_file.write(uploaded_file.read())
    temp_path = temp_file.name

    st.image(temp_path, caption="Uploaded Document", use_column_width=True)

    if st.button("Verify Document"):

        # STEP 3 — OCR (Hidden)
        lines = extract_clean_lines(temp_path)

        # STEP 4 — PARSE
        st.header("Extracted Document Details")
        doc_fields = extract_structured_fields(lines)

        # Only show name, dob, address
        filtered_doc = {
            "name": doc_fields.get("name"),
            "dob": doc_fields.get("dob"),
            "address": doc_fields.get("address")
        }

        st.json(filtered_doc)

        # ---------------------
        # STEP 5 — STRICT LOGIC
        # ---------------------

        # 1. Name must match EXACTLY
        if user_details["name"] != filtered_doc.get("name"):
            st.error("❌ Name does not match. Verification failed.")
            st.stop()

        # 2. DOB must match EXACTLY
        if user_details["dob"] != filtered_doc.get("dob"):
            st.error("❌ Date of Birth does not match. Verification failed.")
            st.stop()

        # If reached here → name & dob match
        st.success("✔ Name and Date of Birth match exactly.")

        # 3. Address → fuzzy match only
        from difflib import SequenceMatcher

        def address_similarity(a, b):
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()

        if user_details["address"] and filtered_doc.get("address"):
            sim = address_similarity(user_details["address"], filtered_doc["address"])
            st.metric("Address Match Confidence", f"{sim * 100:.2f}%")

            if sim > 0.7:
                st.success("✔ Address partially or fully matches.")
            else:
                st.warning("⚠ Address mismatch detected (low similarity).")

