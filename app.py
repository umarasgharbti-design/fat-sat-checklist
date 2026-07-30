import streamlit as st
from fpdf import FPDF
from datetime import date

st.set_page_config(page_title="FAT/SAT Checklist", layout="centered")

# ---------- Checklist Definitions ----------

FAT_STRUCTURE = {
    "FAT Protocols": ["Drawing", "Dimensions", "Machine drawing with utilities"],
    "Nameplate": ["Nameplate"],
    "Toolkit": ["Toolkit"],
    "Manual": ["Technical documents", "Operational documents", "Maintenance documents", "Installation documents"],
    "Drawings": ["Electrical drawings", "P&ID", "Pneumatic drawings"],
    "Backups": ["HMI backup", "PLC backup"],
    "Certificates": ["Material certificates", "Instrument calibration certificate", "OEL certificate"],
    "Validation Certificates": ["IQ", "OQ"],
    "Alarm List": ["Alarm list"],
}

SAT_EXTRA_STRUCTURE = {
    "Site Activities": ["Machine placement", "Hard file documentation provided", "Receiving confirmation"],
}

# ---------- Session State Init ----------

if "checklist_data" not in st.session_state:
    st.session_state.checklist_data = {}

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

# Render FAT sections (always, since SAT includes FAT items)
for section, items in FAT_STRUCTURE.items():
    if section == "Certificates" and st.session_state.has_lef:
        render_section(section, items + ["HEPA certificates"], test_type)
    else:
        render_section(section, items, test_type)

# Render SAT-only sections
if test_type == "SAT":
    for section, items in SAT_EXTRA_STRUCTURE.items():
        render_section(section, items, test_type)

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

def generate_pdf(test_type, project_name, machine_name, checklist_data, validation_notes, survey_rating):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"{test_type} Report", ln=True)

    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"Project: {project_name}", ln=True)
    pdf.cell(0, 8, f"Machine: {machine_name}", ln=True)
    pdf.cell(0, 8, f"Date: {date.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(4)

    for section, items in checklist_data.items():
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, section, ln=True)
        pdf.set_font("Helvetica", size=10)
        for entry in items:
            line = f"- {entry['item']}: {entry['status']}"
            pdf.multi_cell(0, 6, line)
            if entry["notes"]:
                pdf.set_font("Helvetica", "I", 9)
                pdf.multi_cell(0, 5, f"   Notes: {entry['notes']}")
                pdf.set_font("Helvetica", size=10)
        pdf.ln(2)

    if test_type == "SAT":
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Validation", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 6, validation_notes or "N/A")
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Client Satisfaction Survey", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 8, f"Rating: {survey_rating} / 5", ln=True)

    return bytes(pdf.output())

st.subheader("Generate Report")

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
