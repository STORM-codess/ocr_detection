import streamlit as st
import requests

# ---------------- CONFIG ----------------
API_URL = "http://localhost:8000/extract-fields"
ALLOWED_TYPES = ["png", "jpg", "jpeg"]
# ----------------------------------------


st.set_page_config(
    page_title="Document Verifier",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document Verifier")
st.write("Upload a document and extract **Name, Date of Birth, and Address**")

st.divider()

# -------- TWO COLUMN LAYOUT --------
left_col, right_col = st.columns([1, 1.2])

# ================= LEFT SIDE =================
with left_col:
    st.subheader("⬆ Upload Document")

    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=ALLOWED_TYPES,
        help="Supported formats: PNG, JPG, JPEG"
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            caption="Uploaded Document",
            use_container_width=True
        )

        extract_btn = st.button("🔍 Extract Fields", use_container_width=True)
    else:
        extract_btn = False
        st.info("Upload a document image to continue.")

# ================= RIGHT SIDE =================
with right_col:
    st.subheader("📊 Extracted Details")

    if extract_btn and uploaded_file:
        with st.spinner("Processing document..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(API_URL, files=files, timeout=60)

                if response.status_code == 200:
                    data = response.json()

                    st.success("Extraction Successful ✅")

                    st.markdown("### 🧑 Name")
                    st.write(data.get("extracted_name", "—"))

                    st.markdown("### 📅 Date of Birth")
                    st.write(data.get("extracted_dob", "—"))

                    st.markdown("### 🏠 Address")
                    st.write(data.get("extracted_address", "—"))

                else:
                    st.error(
                        response.json().get("detail", "Extraction failed")
                    )

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI server.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    else:
        st.info("Extracted fields will appear here.")

