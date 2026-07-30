from fpdf import FPDF
from datetime import date


def generate_pdf(test_type, project_name, machine_name, checklist_data, validation_notes=None, survey_rating=None):
    """
    Builds the FAT/SAT PDF report in memory and returns it as bytes.

    checklist_data: dict like {"Section Name": [{"item": str, "status": str, "notes": str}, ...]}
    """
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
            if entry.get("notes"):
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
        pdf.cell(0, 8, f"Rating: {survey_rating} / 5" if survey_rating else "Rating: N/A", ln=True)

    return bytes(pdf.output())


def build_filename(test_type, project_name):
    safe_name = (project_name or "report").replace(" ", "_")
    return f"{test_type}_{safe_name}_{date.today()}.pdf"
