from datetime import datetime
import unicodedata
from fpdf import FPDF


UNICODE_REPLACEMENTS = {
    # Typographic punctuation
    "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2015": "-",
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
    "\u2026": "...", "\u2022": "-", "\u2023": ">", "\u2043": "-", "\u00a0": " ", "·": "-",
    # Math & Symbols
    "α": "alpha", "β": "beta", "±": "+/-", "≥": ">=", "≤": "<=", "×": "x", "°": " deg",
    "✔": "[OK]", "✓": "[OK]", "✗": "[X]", "✘": "[X]",
    "★": "*", "☆": "*", "◆": "*", "◇": "*", "●": "*", "○": "*",
    "█": "#", "■": "#", "□": "[ ]",
    # Textile / App Emojis to remove cleanly
    "🧵": "", "📊": "", "💬": "", "⚠️": "", "📥": "", "🔄": "",
    "🟢": "", "🔵": "", "🟡": "", "🔴": "",
}

# 1. Box Drawing characters (U+2500 - U+257F) - All 128 characters mapped
for _cp in range(0x2500, 0x2580):
    _ch = chr(_cp)
    _name = unicodedata.name(_ch, "")
    if "HORIZONTAL" in _name or "DASH" in _name:
        UNICODE_REPLACEMENTS[_ch] = "=" if "DOUBLE" in _name else "-"
    elif "VERTICAL" in _name:
        UNICODE_REPLACEMENTS[_ch] = "|"
    else:
        UNICODE_REPLACEMENTS[_ch] = "+"

# 2. Block elements (U+2580 - U+259F)
for _cp in range(0x2580, 0x25A0):
    UNICODE_REPLACEMENTS[chr(_cp)] = "#"

# 3. Geometric shapes (U+25A0 - U+25FF)
for _cp in range(0x25A0, 0x2600):
    _ch = chr(_cp)
    _name = unicodedata.name(_ch, "")
    if "UP" in _name:
        UNICODE_REPLACEMENTS[_ch] = "^"
    elif "DOWN" in _name:
        UNICODE_REPLACEMENTS[_ch] = "v"
    elif "RIGHT" in _name or "POINTER" in _name:
        UNICODE_REPLACEMENTS[_ch] = ">"
    elif "LEFT" in _name:
        UNICODE_REPLACEMENTS[_ch] = "<"
    elif "CIRCLE" in _name or "DIAMOND" in _name:
        UNICODE_REPLACEMENTS[_ch] = "*"
    elif "SQUARE" in _name or "RECTANGLE" in _name:
        UNICODE_REPLACEMENTS[_ch] = "[ ]" if "WHITE" in _name else "#"

# 4. Arrows & Dingbats (U+2190-U+21FF, U+2790-U+27BF, U+27F0-U+27FF, U+2900-U+297F, U+2B00-U+2BFF)
_arrow_ranges = (
    list(range(0x2190, 0x2200))
    + list(range(0x2790, 0x27C0))
    + list(range(0x27F0, 0x2800))
    + list(range(0x2900, 0x2980))
    + list(range(0x2B00, 0x2C00))
)
for _cp in _arrow_ranges:
    _ch = chr(_cp)
    try:
        _name = unicodedata.name(_ch, "")
    except Exception:
        continue
    if "ARROW" in _name or "POINTER" in _name or "DART" in _name:
        if "LEFT" in _name and "RIGHT" in _name:
            UNICODE_REPLACEMENTS[_ch] = "<-->"
        elif "UP" in _name and "DOWN" in _name:
            UNICODE_REPLACEMENTS[_ch] = "^v"
        elif "LEFT" in _name:
            UNICODE_REPLACEMENTS[_ch] = "<--"
        elif "RIGHT" in _name:
            UNICODE_REPLACEMENTS[_ch] = "-->"
        elif "UP" in _name:
            UNICODE_REPLACEMENTS[_ch] = "^"
        elif "DOWN" in _name:
            UNICODE_REPLACEMENTS[_ch] = "v"


def sanitize_text(text: str) -> str:
    for old, new in UNICODE_REPLACEMENTS.items():
        text = text.replace(old, new)
    out = []
    for c in text:
        try:
            c.encode("latin-1")
            out.append(c)
        except UnicodeEncodeError:
            cat = unicodedata.category(c)
            if cat.startswith("S") or cat.startswith("P"):
                out.append("-")
            elif cat.startswith("Z"):
                out.append(" ")
            elif cat.startswith("L") or cat.startswith("N"):
                decomp = unicodedata.normalize("NFKD", c)
                out.append("".join(d for d in decomp if ord(d) < 256))
            else:
                out.append("")
    return "".join(out)


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
    yarn_type: str = "Single Yarn (Ring Spun)",
    parameters: list = None,
    ai_report_text: str = "",
    yarn_count: float = 0.0,
    count_unit: str = "Ne",
    thick_places: int = 0,
    thin_places: int = 0,
    neps: int = 0,
) -> bytes:
    batch_no = sanitize_text(str(batch_no))
    yarn_type = sanitize_text(str(yarn_type))
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
    pdf.cell(0, 6, f"BATCH NO: {batch_no}  |  YARN TYPE: {yarn_type.upper()}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, f"Report Generated: {timestamp}  |  Developed by: Surya Srekanth", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Measured Values Table Header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(46, 64, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 7, "Parameter / Metric", border=1, fill=True, align="C")
    pdf.cell(50, 7, "Recorded Value", border=1, fill=True, align="C")
    pdf.cell(80, 7, "Unit / Standard", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")

    # Table Content
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(43, 38, 34)

    if not parameters:
        rows = [
            ("Yarn Count", f"{yarn_count}", count_unit),
            ("Thick Places (+50%)", f"{thick_places}", "per 1,000 m"),
            ("Thin Places (-50%)", f"{thin_places}", "per 1,000 m"),
            ("Neps Count (+200%)", f"{neps}", "per 1,000 m"),
        ]
    else:
        rows = parameters

    for item in rows:
        param, val, note = sanitize_text(str(item[0])), sanitize_text(str(item[1])), sanitize_text(str(item[2]))
        pdf.cell(60, 6, f"  {param}", border=1)
        pdf.cell(50, 6, f"  {val}", border=1, align="C")
        pdf.cell(80, 6, f"  {note}", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    # AI Findings Section Header
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(181, 84, 30)
    pdf.cell(0, 6, "AI DIAGNOSTIC REPORT & ACTION PLAN", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(181, 84, 30)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    def parse_markdown_blocks(raw_text: str):
        raw_lines = raw_text.split("\n")
        blocks = []
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i]
            stripped = line.strip()

            # Markdown Code Block delimiters (``` or ''')
            if stripped.startswith("```") or stripped.startswith("'''"):
                code_lines = []
                i += 1
                while i < len(raw_lines):
                    c_line = raw_lines[i]
                    c_stripped = c_line.strip()
                    if c_stripped.startswith("```") or c_stripped.startswith("'''"):
                        i += 1
                        break
                    code_lines.append(c_line.rstrip())
                    i += 1
                blocks.append(("code_block", code_lines))
                continue

            # Check for un-fenced ASCII diagram block
            is_diag = (
                (stripped.startswith(("+", "|")) and ("|" in stripped or "-" in stripped or "+" in stripped))
                or (stripped.startswith("[") and ("-->" in stripped or "->" in stripped or "|" in stripped or ("]" in stripped and len(stripped) < 35)))
                or (stripped in ("v", "^", "|", "||", "+", "-"))
                or (stripped.startswith("v") and len(stripped) < 6)
                or (stripped.startswith("^") and len(stripped) < 6)
                or ("--->" in stripped or "----" in stripped and not stripped.startswith("---"))
            )
            if is_diag:
                diag_lines = []
                while i < len(raw_lines):
                    d_line = raw_lines[i]
                    d_stripped = d_line.strip()
                    if not d_stripped:
                        break
                    if d_stripped.startswith("#") or (len(d_stripped) > 2 and d_stripped[0:2].isdigit() and d_stripped[1] in (".", ")")):
                        break
                    diag_lines.append(d_line.rstrip())
                    i += 1
                blocks.append(("code_block", diag_lines))
                continue

            if not stripped or stripped.startswith("---"):
                blocks.append(("spacer", ""))
                i += 1
                continue

            if stripped.startswith("#"):
                clean = stripped.lstrip("# ").replace("**", "").replace("*", "").strip()
                blocks.append(("heading", clean))
                i += 1
                continue

            if stripped.startswith("**") or (len(stripped) > 2 and stripped[0:2].isdigit() and stripped[1] in (".", ")")):
                clean = stripped.replace("**", "").strip()
                blocks.append(("subheading", clean))
                i += 1
                continue

            if stripped.startswith("- ") or stripped.startswith("* "):
                clean = stripped.lstrip("-* ").replace("**", "").replace("*", "").strip()
                blocks.append(("bullet", clean))
                i += 1
                continue

            clean = stripped.replace("**", "").replace("*", "").strip()
            blocks.append(("paragraph", clean))
            i += 1

        return blocks

    blocks = parse_markdown_blocks(ai_report_text)
    for b_type, b_content in blocks:
        if b_type == "code_block":
            clean_lines = [sanitize_text(l) for l in b_content if l.strip()]
            if not clean_lines:
                continue

            line_h = 3.6
            box_h = len(clean_lines) * line_h + 8.5
            if pdf.get_y() + box_h > 275:
                pdf.add_page()

            cur_y = pdf.get_y()
            # Draw container card background and border
            pdf.set_fill_color(248, 244, 236)
            pdf.set_draw_color(46, 64, 87)
            pdf.set_line_width(0.35)
            pdf.rect(10, cur_y, 190, box_h, "DF")

            # Left accent stripe (Rust #B5541E)
            pdf.set_fill_color(181, 84, 30)
            pdf.rect(10, cur_y, 2, box_h, "F")

            # Banner Header Badge
            pdf.set_xy(14, cur_y + 1.8)
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_text_color(181, 84, 30)
            pdf.cell(0, 3.5, "DIAGNOSTIC PROCESS FLOW & TROUBLESHOOTING MAP", new_x="LMARGIN", new_y="NEXT")

            # Monospace schematic lines
            pdf.set_font("Courier", "", 7.5)
            pdf.set_text_color(43, 38, 34)
            for c_line in clean_lines:
                pdf.set_x(14)
                pdf.cell(182, line_h, c_line, new_x="LMARGIN", new_y="NEXT")

            pdf.set_y(cur_y + box_h + 3)

        elif b_type == "spacer":
            pdf.ln(2)

        elif b_type == "heading":
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(46, 64, 87)
            pdf.multi_cell(0, 5, sanitize_text(b_content).upper(), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(30, 30, 30)

        elif b_type == "subheading":
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(46, 64, 87)
            pdf.multi_cell(0, 5.5, sanitize_text(b_content), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(30, 30, 30)

        elif b_type == "bullet":
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 5, f"  - {sanitize_text(b_content)}", new_x="LMARGIN", new_y="NEXT")

        elif b_type == "paragraph":
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 5, sanitize_text(b_content), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_draw_color(220, 220, 220)
    pdf.set_fill_color(246, 241, 228)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Report Generated via AI Yarn Defect Assistant  |  Developer: Surya Srekanth", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
