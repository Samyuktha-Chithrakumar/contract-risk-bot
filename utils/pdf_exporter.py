from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_pdf(summary, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 40
    for line in summary.split("\n"):
        c.drawString(40, y, line)
        y -= 15
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    return filename
