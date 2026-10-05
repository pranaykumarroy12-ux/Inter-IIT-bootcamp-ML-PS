"""
PDF export utility for Meeting Records.
Generates a highly readable PDF document from the structured meeting record schema.
"""

from fpdf import FPDF
from typing import Dict, Any
import re
import textwrap

class MeetingPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "AI-Powered Meeting Assistant", border=False, ln=True, align="C")
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "Generated Meeting Record", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def sanitize_text(text: str) -> str:
    """Replaces unicode characters and forcefully wraps text."""
    if not isinstance(text, str):
        return ""
    
    replacements = {
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '--', '\u2026': '...', '\u2022': '-',
        '\u00a0': ' ', '\t': '    '
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
        
    # Strip invisible control characters (except newlines)
    text = re.sub(r'[\x00-\x09\x0B-\x1F\x7F-\x9F]', '', text)
    
    # Ensure latin-1 compliance
    text = text.encode('latin-1', 'ignore').decode('latin-1')
    
    # Wrap text at 85 chars to comfortably fit A4 width
    wrapped_lines = []
    for line in text.splitlines():
        if not line.strip():
            wrapped_lines.append("")
        else:
            wrapped_lines.append(textwrap.fill(line, width=85, break_long_words=True))
    
    return "\n".join(wrapped_lines)

def write_multiline(pdf: FPDF, text: str, indent: int = 0):
    """Bypasses FPDF multi_cell layout engine by drawing explicit wrapped lines."""
    clean_text = sanitize_text(text)
    for line in clean_text.splitlines():
        if indent > 0:
            pdf.cell(indent, 6, "", ln=False)
        pdf.cell(0, 6, line, ln=True)

def generate_meeting_pdf(json_record: Dict[str, Any]) -> bytes:
    """
    Takes the structured JSON output from Stage 3 and converts it to a formatted PDF.
    Returns the PDF as a bytearray.
    """
    pdf = MeetingPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- 1. Summary & Minutes ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. Meeting Summary & Minutes", ln=True)
    
    pdf.set_font("Helvetica", "", 11)
    summary_text = json_record.get("summary_and_minutes", "")
    summary_text = summary_text.replace("**", "").replace("###", "").strip()
    write_multiline(pdf, summary_text)
    pdf.ln(5)
    
    # --- 2. Key Decisions ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "2. Key Decisions", ln=True)
    
    pdf.set_font("Helvetica", "", 11)
    decisions = json_record.get("key_decisions", [])
    if not decisions:
        write_multiline(pdf, "No key decisions were explicitly agreed upon during this meeting.")
    else:
        for d in decisions:
            write_multiline(pdf, f"- {d}")
    pdf.ln(5)
    
    # --- 3. Action Items ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "3. Action Items", ln=True)
    
    action_items = json_record.get("action_items", [])
    if not action_items:
        pdf.set_font("Helvetica", "", 11)
        write_multiline(pdf, "No action items were assigned during this meeting.")
    else:
        for idx, item in enumerate(action_items, 1):
            pdf.set_font("Helvetica", "B", 11)
            write_multiline(pdf, f"Task {idx}: {item.get('task_description', '')}")
            
            pdf.set_font("Helvetica", "", 11)
            write_multiline(pdf, f"Owner: {item.get('owner', 'unspecified')}", indent=10)
            write_multiline(pdf, f"Deadline: {item.get('deadline', 'unspecified')}", indent=10)
            pdf.ln(3)

    return bytes(pdf.output())
