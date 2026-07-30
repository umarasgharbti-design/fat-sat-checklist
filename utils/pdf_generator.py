from fpdf import FPDF
from datetime import date


def clean_text(text):
    """Strip characters that core PDF fonts (Latin-1 only) can't render."""
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")


def write_line(pdf, text, height=6, style=""):
    """Safely write a line, resetting x to the left margin first."""
    pdf.set_x(pdf.l_margin)
    if style:
        pdf.set_font("Helvetica", style, pdf.font_size_pt)
    pdf.multi_cell(pdf.epw, height, clean_text(text))


def generate_pdf(test_type, project_name, machine_name, checklist_data, validation_notes=None, survey_rating=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    write_line(pdf, f"{test_type} Report", height=10)

    pdf.set_font("Helvetica", size=11)
    write_line(pdf, f"Project: {project_name}", height=8)
    write_line(pdf, f"Machine: {machine_name}", height=8)
    write_line(pdf, f"Date: {date.today().strftime('%Y-%m-%d')}", height=8)
    pdf.ln(4)

    for section, items in checklist_data.items():
        pdf.set_font("Helvetica", "B", 13)
        write_line(pdf, section, height=8)
        pdf.set_font("Helvetica", size=10)
        for entry in items:
            line = f"- {entry['item']}: {entry['status']}"
            write_line(pdf, line, height=6)
            if entry.get("notes"):
                pdf.set_font("Helvetica", "I", 9)
                write_line(pdf, f"   Notes: {entry['notes']}", height=5)
                pdf.set_font("Helvetica", size=10)
        pdf.ln(2)

    if test_type == "SAT":
        pdf.set_font("Helvetica", "B", 13)
        write_line(pdf, "Validation", height=8)
        pdf.set_font("Helvetica", size=10)
        write_line(pdf, validation_notes or "N/A", height=6)
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 13)
        write_line(pdf, "Client Satisfaction Survey", height=8)
        pdf.set_font("Helvetica", size=10)
        rating_text = f"Rating: {survey_rating} / 5" if survey_rating else "Rating: N/A"
        write_line(pdf, rating_text, height=8)

    return bytes(pdf.output())


def build_filename(test_type, project_name):
    safe_name = (project_name or "report").replace(" ", "_")
    return f"{test_type}_{safe_name}_{date.today()}.pdf"
