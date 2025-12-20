from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from django.conf import settings
from datetime import datetime
import os

def draw_header_footer(c, width, height):
    # ===== HEADER =====
    today = datetime.now().strftime("%d %B %Y")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 1.5*cm, "PERSONS WITH DISABILITY (PWD) REGISTER")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 2.3*cm, f"Generated on: {today}")

    # ===== PAGE NUMBERS =====
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 1.2*cm, f"Page {c.getPageNumber()}")


def generate_pwd_pdf(response, records):
    page_size = A4
    c = canvas.Canvas(response, pagesizes=page_size)
    width, height = page_size

    # ===== WATERMARK LOGO =====
    logo_path = os.path.join(settings.BASE_DIR, "static/council_logo.png")

    def draw_watermark():
        if os.path.exists(logo_path):
            c.saveState()
            c.setFillAlpha(0.08)
            c.drawImage(
                logo_path,
                width/2 - 6*cm,
                height/2 - 6*cm,
                12*cm,
                12*cm,
                preserveAspectRatio=True,
                mask='auto'
            )
            c.restoreState()

    def signature_block():
        # ===== SIGNATURE BLOCK =====
        sig_y = 90
        c.setFont("Helvetica-Bold", 10)
        c.drawString(80, sig_y + 30, "Prepared By:")
        c.drawString(300, sig_y + 30, "Approved By:")

        c.setFont("Helvetica", 10)
        c.line(80, sig_y, 260, sig_y)
        c.line(300, sig_y, 560, sig_y)

        c.drawString(80, sig_y - 15, "PWD Desk Officer")
        c.drawString(380, sig_y - 15, "District Coordinating Director")

        c.drawString(80, sig_y - 30, "Date: ______________________")
        c.drawString(300, sig_y - 30, "Date: ______________________")

    # ===== LAYOUT SETTINGS =====
    x_left = 1.5 * cm
    x_right = width / 2 + 0.5 * cm
    y = height - 4 * cm
    box_height = 6 * cm
    column = 0

    draw_header_footer(c, width, height)
    draw_watermark()

    for index, record in enumerate(records, start=1):
        x = x_left if column == 0 else x_right

        # Card border
        c.rect(x - 0.3*cm, y - box_height, width/2 - 2*cm, box_height)

        # Photo
        if record.id_photo:
            img_path = os.path.join(settings.MEDIA_ROOT, record.id_photo.name)
            if os.path.exists(img_path):
                c.drawImage(
                    ImageReader(img_path),
                    x,
                    y - 5*cm,
                    4*cm,
                    5*cm,
                    preserveAspectRatio=True
                )

        text_x = x + 4.5*cm
        text_y = y - 0.8*cm

        c.setFont("Helvetica", 10)
        lines = [
            f"NAME: {record.full_name}",
            f"AGE: {record.date_of_birth}",
            f"GENDER: {record.gender}",
            f"DISABILITY TYPE: {record.disability_type}",
            f"CONTACT: {record.contact_number}",
            f"OCCUPATION: {record.occupation or 'N/A'}",
            f"COMMUNITY: {record.community}",
            f"AREA COUNCIL: {record.area_council}",
        ]

        for line in lines:
            c.drawString(text_x, text_y, line)
            text_y -= 0.55*cm

        column += 1

        if column == 2:
            column = 0
            y -= box_height + 0.8*cm



        # ===== New page =====
        if y < 3*cm:
            c.showPage()
            draw_header_footer(c, width, height)
            draw_watermark()
            y = height - 4 * cm
            column = 0

    
    signature_block()
    c.save()
