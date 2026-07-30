import streamlit as st
from datetime import date
from utils.checklist_data import get_structure
from utils.pdf_generator import generate_pdf, build_filename

st.set_page_config(page_title="FAT/SAT Checklist", layout="centered")

# ---------- Session State Init ----------

if "has_lef" not in st.session_state:
    st.session_state.has_lef = False

# ---------- UI ----------

st.title("FAT / SAT Checklist")

test_type = st.selectbox("Select Test Type", ["FAT", "SAT"])

project_name = st.text_input("Project / Client Name")
machine_name = st.text_input("Machine / Equipment Name")

st.session_state.has_lef = st.checkbox("Machine has LEF / Laminar Flow installed (adds HEPA certificate check)")

st.divider()

checklist_data = {}

def render_section(section, items, key_prefix):
    st.subheader(section)
    section_data = []
    for item in items:
        col1, col2 = st.columns([1, 2])
        with col1:
            status = st.radio(
                item,
                ["Available", "Unavailable"],
                key=f"{key_prefix}_{section}_{item}_status",
                horizontal=True,
            )
        with col2:
            notes = st.text_area(
                "Notes",
                key=f"{key_prefix}_{section}_{item}_notes",
                max_chars=300,
                height=68,
                label_visibility="collapsed",
                placeholder="Notes (optional)",
            )
        section_data.append({"item": item, "status": status, "notes": notes})
    checklist_data[section] = section_data

structure = get_structure(test_type, has_lef=st.session_state.has_lef)

for section, items in structure.items():
    render_section(section, items, test_type)

if test_type == "SAT":
    st.subheader("Validation")
    validation_notes = st.text_area(
        "Client Validation Notes (to be filled by client)",
        key="validation_notes",
        height=100,
        placeholder="Client writes their validation feedback here",
    )

    st.subheader("Client Satisfaction Survey")
    survey_rating = st.radio(
        "Rate our service (1 = Poor, 5 = Excellent)",
        [1, 2, 3, 4, 5],
        horizontal=True,
        key="survey_rating",
    )
else:
    validation_notes = None
    survey_rating = None

st.divider()

# ---------- PDF Generation ----------

st.subheader("Generate Report")

if st.button("Generate PDF"):
    if not project_name or not machine_name:
        st.warning("Please fill in Project Name and Machine Name before generating the report.")
    else:
        pdf_bytes = generate_pdf(
            test_type, project_name, machine_name,
            checklist_data, validation_notes, survey_rating
        )
        st.session_state["pdf_bytes"] = pdf_bytes
        st.session_state["pdf_filename"] = build_filename(test_type, project_name)
        st.success("PDF generated successfully.")

if "pdf_bytes" in st.session_state:
    st.download_button(
        label="Download PDF",
        data=st.session_state["pdf_bytes"],
        file_name=st.session_state["pdf_filename"],
        mime="application/pdf",
    )
