# ocr/parser.py
import re

def extract_structured_fields(lines):
    """
    Extract structured fields (name, dob, address, fathers_name) from OCR lines.
    Returns values in lowercase (or None if not found).
    """

    # Normalize each line → lowercase, remove unwanted punctuation
    cleaned_lines = []
    for line in lines:
        if not line:
            continue
        line = line.lower()
        # keep letters, numbers, slash, hyphen and spaces
        line = re.sub(r"[^a-z0-9/\-\s]", " ", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            cleaned_lines.append(line)

    # Combine everything into one big string
    full_text = " ".join(cleaned_lines)

    # Initialize fields dict safely
    fields = {
        "name": None,
        "dob": None,
        "address": None,
        "fathers_name": None,
    }

    # ------------ NAME ------------
    # We only treat lines that look like "name: xyz"
    name_patterns = [
        r"\bname[:\- ]+([a-z ]+)$",
        r"\bstudent name[:\- ]+([a-z ]+)$",
        r"\bfull name[:\- ]+([a-z ]+)$",
    ]

    for line in cleaned_lines:
        line_clean = line.strip()
        for pat in name_patterns:
            m = re.search(pat, line_clean)
            if m:
                name_val = m.group(1).strip()
                name_val = re.sub(r"\s+", " ", name_val)
                fields["name"] = name_val or None
                break
        if fields["name"]:
            break

    # ------------ FATHER'S NAME ------------
    father_patterns = [
        r"\bfather'?s name[:\- ]+([a-z ]+)$",
        r"\bs\/o[:\- ]+([a-z ]+)$",
        r"\bf\/o[:\- ]+([a-z ]+)$",
    ]

    for line in cleaned_lines:
        line_clean = line.strip()
        for pat in father_patterns:
            m = re.search(pat, line_clean)
            if m:
                f_val = m.group(1).strip()
                f_val = re.sub(r"\s+", " ", f_val)
                fields["fathers_name"] = f_val or None
                break
        if fields["fathers_name"]:
            break

    # ------------ DOB ------------
    dob_patterns = [
        r"\bdob[:\- ]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
        r"\bdate of birth[:\- ]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
        r"\bbirth date[:\- ]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
        r"\bbirth[:\- ]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
    ]

    for pat in dob_patterns:
        m = re.search(pat, full_text)
        if m:
            fields["dob"] = m.group(1).strip()
            break

    # ------------ ADDRESS ------------
    # Capture lines after a line containing the word "address"
    address_lines = []
    start = False

    for line in cleaned_lines:
        if "address" in line and not start:
            start = True
            # If there is content on the same line after "address"
            parts = line.split("address", 1)
            tail = parts[1].strip()
            if tail:
                address_lines.append(tail)
            continue

        if start:
            # stop if another field label starts
            if any(x in line for x in [
                "dob", "date of birth", "birth", "name",
                "enrol", "enrl", "program", "dept", "father"
            ]):
                break
            address_lines.append(line)

    if address_lines:
        addr = " ".join(address_lines).strip()
        addr = re.sub(r"\s+", " ", addr)
        fields["address"] = addr or None

    return fields
