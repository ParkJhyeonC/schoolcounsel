from __future__ import annotations


def _escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def build_student_card_pdf(card: dict) -> bytes:
    lines = [
        'BT /F1 14 Tf 50 780 Td (Student Counseling Card) Tj ET',
        f"BT /F1 11 Tf 50 755 Td ({_escape('Name: ' + card['student_name'])}) Tj ET",
        f"BT /F1 11 Tf 50 738 Td ({_escape('Student ID: ' + card['student_id'])}) Tj ET",
        f"BT /F1 11 Tf 50 721 Td ({_escape('Class: ' + card['grade'] + '-' + card['class_name'])}) Tj ET",
        'BT /F1 11 Tf 50 695 Td (History) Tj ET',
    ]
    y = 678
    for item in card["history"]:
        row = f"{item['date']} | {item['method']} | {item['topic']} | {item['duration_minutes']}min"
        lines.append(f"BT /F1 10 Tf 50 {y} Td ({_escape(row[:100])}) Tj ET")
        y -= 14
        note = item.get("notes", "")
        if note:
            lines.append(f"BT /F1 10 Tf 65 {y} Td ({_escape('- ' + note[:90])}) Tj ET")
            y -= 14
        if y < 50:
            break

    content = "\n".join(lines).encode("latin-1", errors="replace")

    objs = []
    objs.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objs.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objs.append(b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n")
    objs.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objs.append(f"5 0 obj << /Length {len(content)} >> stream\n".encode() + content + b"\nendstream endobj\n")

    pdf = bytearray(b"%PDF-1.4\n")
    xref = [0]
    for obj in objs:
        xref.append(len(pdf))
        pdf.extend(obj)
    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(xref)}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in xref[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(f"trailer << /Size {len(xref)} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode())
    return bytes(pdf)
