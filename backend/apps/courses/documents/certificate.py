from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


def _centered_wrapped_text(pdf, text, y, *, font, size, max_width, leading):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    page_width, _ = landscape(A4)
    for line in lines:
        pdf.drawCentredString(page_width / 2, y, line)
        y -= leading
    return y


def build_certificate_pdf(certificate):
    buffer = BytesIO()
    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    dark_panel = HexColor("#2D2342")
    primary = HexColor("#8B5CF6")
    accent = HexColor("#06B6D4")
    text_muted = HexColor("#64557A")

    pdf.setFillColor(dark_panel)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.roundRect(28, 28, page_width - 56, page_height - 56, 18, fill=1, stroke=0)
    pdf.setStrokeColor(primary)
    pdf.setLineWidth(3)
    pdf.roundRect(42, 42, page_width - 84, page_height - 84, 14, fill=0, stroke=1)

    pdf.setFillColor(accent)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(page_width / 2, page_height - 95, "CIBERSEGURA")
    pdf.setFillColor(dark_panel)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(page_width / 2, page_height - 145, "CERTIFICADO DE FINALIZACIÓN")
    pdf.setFillColor(text_muted)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(page_width / 2, page_height - 180, "Se certifica que")

    profile = getattr(certificate.user, "profile", None)
    full_name = (
        profile.full_name
        if profile and profile.full_name
        else certificate.user.username
    )
    pdf.setFillColor(dark_panel)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(page_width / 2, page_height - 225, full_name)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1)
    pdf.line(190, page_height - 238, page_width - 190, page_height - 238)

    pdf.setFillColor(text_muted)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 275,
        "completó la ruta adaptativa y aprobó el cuestionario del módulo",
    )
    pdf.setFillColor(primary)
    pdf.setFont("Helvetica-Bold", 18)
    y = _centered_wrapped_text(
        pdf,
        certificate.unit.title,
        page_height - 312,
        font="Helvetica-Bold",
        size=18,
        max_width=520,
        leading=22,
    )

    pdf.setFillColor(dark_panel)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(
        page_width / 2, max(112, y - 45), "Aprobación mínima alcanzada: 80%"
    )
    pdf.setFillColor(text_muted)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        80, 82, f"Fecha de emisión: {certificate.issued_at.strftime('%d/%m/%Y')}"
    )
    pdf.drawRightString(
        page_width - 80,
        82,
        f"Código de verificación: {certificate.verification_code}",
    )
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawCentredString(
        page_width / 2,
        58,
        "Certificado educativo de finalización. No constituye acreditación profesional.",
    )
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
