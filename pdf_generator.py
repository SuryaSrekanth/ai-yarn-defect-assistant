from datetime import datetime
from fpdf import FPDF


def sanitize_text(text: str) -> str:
    replacements = {
        "\u2013": "-",  # en-dash
        "\u2014": "-",  # em-dash
        "\u2018": "'",  # left single quote
        "\u2019": "'",  # right single quote
        "\u201c": '"',  # left double quote
        "\u201d": '"',  # right double quote
        "\u2026": "...", # ellipsis
        "\u2022": "-",  # bullet point
        "\u00a0": " ",  # non-breaking space
        "·": "-",       # middle dot
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class TextileReportPDF(FPDF):

    def header(self):
        # Top Accent Ribbon (#B5541E Rust)
        self.set_fill_color(181, 84, 30)
        self.rect(0, 0, 210, 5, "F")

        # Lab Title Header (#2E4057 Slate Blue)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(46, 64, 87)
        self.set_y(10)
        self.cell(0, 7, "TEXTILE QUALITY CONTROL LABORATORY", align="C", new_x="LMARGIN", new_y="NEXT")

        # Report Subtitle
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(181, 84, 30)
        self.cell(0, 5, "YARN INSPECTION & AI DEFECT ANALYSIS REPORT", align="C", new_x="LMARGIN", new_y="NEXT")

        # Developer Attribution
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(80, 80, 80)
        self.cell(0, 4, "System Developer: Surya Srekanth", align="C", new_x="LMARGIN", new_y="NEXT")

        # Decorative Divider Line
        self.set_draw_color(43, 38, 34)
        self.set_line_width(0.4)
        self.line(10, 30, 200, 30)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, "Developed by Surya Srekanth | AI Yarn Defect Assistant", align="L")
        self.set_y(-15)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="R")


def generate_pdf_report(
    batch_no: str,
    yarn_count: float,
    count_unit: str,
    thick_places: int,
    thin_places: int,
    neps: int,
    ai_report_text: str,
) -> bytes:
    batch_no = sanitize_text(str(batch_no))
    count_unit = sanitize_text(str(count_unit))
    ai_report_text = sanitize_text(str(ai_report_text))

    pdf = TextileReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Batch & Inspection Info Card
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(46, 64, 87)
    pdf.cell(0, 6, f"BATCH NO: {batch_no}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, f"Report Generated: {timestamp}  |  Developed by: Surya Srekanth", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Measured Values Table Header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(46, 64, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(55, 7, "Parameter", border=1, fill=True, align="C")
    pdf.cell(45, 7, "Measured Value", border=1, fill=True, align="C")
    pdf.cell(90, 7, "Unit / Reference Standard", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")

    # Table Content
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(43, 38, 34)
    rows = [
        ("Yarn Count", f"{yarn_count}", count_unit),
        ("Thick Places (+50%)", f"{thick_places}", "per 1,000 m"),
        ("Thin Places (-50%)", f"{thin_places}", "per 1,000 m"),
        ("Neps Count (+200%)", f"{neps}", "per 1,000 m"),
    ]

    for param, val, note in rows:
        pdf.cell(55, 6, f"  {param}", border=1)
        pdf.cell(45, 6, f"  {val}", border=1, align="C")
        pdf.cell(90, 6, f"  {note}", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    # AI Findings Section Header
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(181, 84, 30)
    pdf.cell(0, 6, "AI DIAGNOSTIC REPORT & ACTION PLAN", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(181, 84, 30)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    # Parse and format AI markdown text into clean PDF text
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(30, 30, 30)

    lines = ai_report_text.split("\n")
    for line in lines:
        raw_line = line.strip()
        if not raw_line or raw_line.startswith("---"):
            pdf.ln(2)
            continue


        # Clean markdown formatting tags and sanitize unicode characters
        clean_text = raw_line.lstrip("-*# ").replace("**", "").replace("*", "").strip()
        clean_text = sanitize_text(clean_text)

        if raw_line.startswith("#"):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(46, 64, 87)
            pdf.multi_cell(0, 5, clean_text.upper(), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(30, 30, 30)
        elif raw_line.startswith("**") or (len(raw_line) > 2 and raw_line[0:2].isdigit()):
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(46, 64, 87)
            pdf.multi_cell(0, 5.5, clean_text, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(30, 30, 30)
        elif raw_line.startswith("- ") or raw_line.startswith("* "):
            pdf.multi_cell(0, 5, f"  - {clean_text}", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.multi_cell(0, 5, clean_text, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_draw_color(220, 220, 220)
    pdf.set_fill_color(246, 241, 228)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Report Generated via AI Yarn Defect Assistant  |  Developer: Surya Srekanth", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
