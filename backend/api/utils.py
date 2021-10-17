from datetime import datetime as dt

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


FONT = 'DejaVuSerif'
TITLE = 'List shopping of recipes'
SIGN = 'Foodgram by @z.abduev'
FILENAME = 'list_shopping_of_recipes'
DATE = f'{dt.now().date().strftime("%d/%m/%y")}'
HEIGHT = 650


def page_draw(pdf_obj):
    page = canvas.Canvas(pdf_obj, pagesize=A4)
    page.setTitle('Shopping list')
    page.setFont('DejaVuSerif', 10)
    page.drawCentredString(50, 820, DATE)
    page.drawCentredString(500, 820, SIGN)
    page.setFont('DejaVuSerif', 20)
    page.drawCentredString(300, 740, TITLE)
    page.setFont('DejaVuSerif', 16)
    page.line(30, 720, 565, 720)
    return page


def fill_page_with_data(data, page, height=HEIGHT):
    for key, item in data.items():
        page.drawString(
            50, height,
            f"{key} - {item['amount']} {item['measurement_unit']}."
        )
        height -= 25
    page.showPage()
    page.save()


def download_to_pdf(data):
    pdf_obj = HttpResponse(content_type='application/pdf')
    pdf_obj['Content-Disposition'] = f'attachment; filename={FILENAME}.pdf'
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    page = page_draw(pdf_obj)
    fill_page_with_data(data, page)
    return pdf_obj
