import pdfplumber
import docx
import re

def parse_pdf(file):
    """Extracts text from all pages of a PDF."""
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def parse_docx(file):
    """Extracts text from all paragraphs in a DOCX file."""
    try:
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_financials_from_text(text):
    """Extracts key financial metrics from raw text using regex."""
    financial_keywords = {
        "Revenue": r"(Revenue|Total Revenue|Sales)\D*\$?([\d,\.]+)",
        "Net Profit": r"(Net (Profit|Income|Earnings))\D*\$?([\d,\.]+)",
        "Total Assets": r"(Total Assets)\D*\$?([\d,\.]+)",
        "Liabilities": r"(Total Liabilities|Liabilities)\D*\$?([\d,\.]+)",
        "Equity": r"(Equity|Shareholders'? Equity)\D*\$?([\d,\.]+)",
        "Cash Flow": r"(Cash Flow|Operating Cash Flow)\D*\$?([\d,\.]+)"
    }

    results = {}
    for key, pattern in financial_keywords.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Search all matched groups and grab the last valid number
            groups = match.groups()
            for g in reversed(groups):
                if g and g.replace(',', '').replace('.', '').isdigit():
                    g = g.replace(',', '')
                    try:
                        results[key] = float(g)
                    except:
                        results[key] = g
                    break
            else:
                results[key] = "Not Found"
        else:
            results[key] = "Not Found"

    return results