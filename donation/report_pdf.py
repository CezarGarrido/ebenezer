from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
import locale
from datetime import datetime
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def get_report_title(context):
    if context.get("employee"):
        return "RELATÓRIO DE VALORES RECEBIDOS POR FUNCIONÁRIO"
    elif context.get("donor"):
        return "RELATÓRIO DE VALORES RECEBIDOS POR DOADOR"
    return "RELATÓRIO GERAL DE DOAÇÕES"

def get_identification_lines(context):
    lines = []
    if context.get("employee"):
        emp = context["employee"]
        lines.append(f"Código............: {emp.id}")
        lines.append(f"Funcionário.......: {emp.name.upper()}")
    elif context.get("donor"):
        donor = context["donor"]
        lines.append(f"Código............: {donor.id}")
        lines.append(f"Doador............: {donor.name.upper()}")
    return lines

def truncate_name(name, max_len=45):
    """Trunca o nome sem cortar sobrenomes, adicionando '...' se necessário."""
    words = name.strip().split()
    truncated = ""
    for word in words:
        if len(truncated) + len(word) + 1 > max_len:
            break
        truncated += (word + " ")
    truncated = truncated.strip()
    if truncated != name:
        truncated += "..."
    return truncated

def generate_donation_report_pdf(context):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    PAGE_WIDTH, PAGE_HEIGHT = A4
    MARGIN_LEFT = 20 * mm
    MARGIN_RIGHT = 20 * mm
    MARGIN_TOP = 20 * mm
    MARGIN_BOTTOM = 20 * mm
    LINE_HEIGHT = 6 * mm
    FONT_SIZE = 10
    FONT_NAME = "Courier"

    x = MARGIN_LEFT
    y = PAGE_HEIGHT - MARGIN_TOP
    usable_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    c.setFont(FONT_NAME, FONT_SIZE)
    
    c.setTitle(get_report_title(context))
    page_number = 1
    
    styles = getSampleStyleSheet()
    para_style = styles["Normal"]
    para_style.fontName = "Helvetica"
    para_style.fontSize = 8
    para_style.leading = 10  # espaço entre linhas dentro da célula

    def draw_page_number():
        c.setFont("Helvetica", 8)
        c.drawCentredString(PAGE_WIDTH / 2, MARGIN_BOTTOM / 2, f"Página {page_number}")

    def draw_side_by_side(left, right):
        nonlocal y
        c.setFont(FONT_NAME, FONT_SIZE)
        right_width = c.stringWidth(right, FONT_NAME, FONT_SIZE)
        right_x = PAGE_WIDTH - MARGIN_RIGHT - right_width
        c.drawString(x, y, left)
        c.drawString(right_x, y, right)
        y -= LINE_HEIGHT

    def draw_text(text, bold=False, align="left"):
        nonlocal x, y
        font_name = f"{FONT_NAME}-Bold" if bold else FONT_NAME
        c.setFont(font_name, FONT_SIZE)
        text_width = c.stringWidth(text, font_name, FONT_SIZE)
        draw_x = x if align == "left" else (PAGE_WIDTH - text_width) / 2 if align == "center" else PAGE_WIDTH - MARGIN_RIGHT - text_width
        c.drawString(draw_x, y, text)
        y -= LINE_HEIGHT

    def write_line(text):
        nonlocal y, page_number
        c.setFont(FONT_NAME, FONT_SIZE)
        c.drawString(x, y, text)
        y -= LINE_HEIGHT
        if y < MARGIN_BOTTOM:
            draw_page_number()
            c.showPage()
            page_number += 1
            c.setFont(FONT_NAME, FONT_SIZE)
            y = PAGE_HEIGHT - MARGIN_TOP

    company = context["company"]
    donations = context["donations"]
    start_date = context["start_date"]
    end_date = context["end_date"]

    emi_date = datetime.now().strftime('%d/%m/%Y')
    draw_side_by_side(f"{company.name}", f"Emissão: {emi_date}")

    try:
        cnpj = company.legalentity.cnpj or "-"
    except:
        cnpj = "-"
    draw_side_by_side("Inscrição Estadual Nº ISENTO", f"C.G.C Nº: {cnpj}")
    c.line(MARGIN_LEFT, y, PAGE_WIDTH - MARGIN_RIGHT, y)
    y -= LINE_HEIGHT

    draw_text(get_report_title(context), bold=True, align="center")
    c.line(MARGIN_LEFT, y, PAGE_WIDTH - MARGIN_RIGHT, y)
    y -= LINE_HEIGHT

    write_line(f"Período...........: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}")
    for line in get_identification_lines(context):
        write_line(line)
    write_line("")

    table_header = ["ID", "Data", "Doador", "Valor Previsto", "Valor Recebido", "Diferença"]
    rows = []

    total_previsto = 0
    total_recebido = 0
    for d in donations:
        valor_previsto = d.amount or 0
        valor_recebido = d.paid_amount or 0
        diferenca = ((valor_recebido - valor_previsto) / valor_previsto * 100) if valor_previsto > 0 else 0.0
        total_previsto += valor_previsto
        total_recebido += valor_recebido
        donor_name = truncate_name(d.donor.name.upper(), max_len=28)
        donor_str = f"{d.donor.id} - {donor_name}"
        
        rows.append([
            str(d.id),
            d.paid_at.strftime('%d/%m/%Y') if d.paid_at else "-",
            donor_str,
            locale.currency(valor_previsto, grouping=True),
            locale.currency(valor_recebido, grouping=True),
            f"{diferenca:.2f}%"
        ])

    diferenca_total = ((total_recebido - total_previsto) / total_previsto * 100) if total_previsto > 0 else 0.0
    rows.append(["", "", "Totais:", locale.currency(total_previsto, grouping=True), locale.currency(total_recebido, grouping=True), f"{diferenca_total:.2f}%"])
        
    MIN_Y = MARGIN_BOTTOM
    def draw_table(data_block, y_pos):
        t = Table(data_block, colWidths=[40, 60, 160, 80, 80, 60])
        styles = [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),  # Coluna doador alinhada à esquerda
        ]
        if "Totais:" in data_block[-1]:
            styles.append(('FONTNAME', (2, -1), (5, -1), 'Helvetica-Bold'))
        styles.append(('ALIGN', (2, 1), (2, -1), 'LEFT'))  # Alinha coluna doador à esquerda
        t.setStyle(TableStyle(styles))
        t.setStyle(TableStyle(styles))
        t.wrapOn(c, usable_width, y_pos)
        t.drawOn(c, MARGIN_LEFT, y_pos - t._height)
        return t._height

    current_data = [table_header]
    for i, row in enumerate(rows):
        current_data.append(row)
        tmp_table = Table(current_data, colWidths=[40, 60, 160, 80, 80, 60])
        tmp_table.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 8)]))
        tmp_table.wrapOn(c, usable_width, y)
        estimated_height = tmp_table._height

        if y - estimated_height < MIN_Y:
            current_data.pop()
            height = draw_table(current_data, y)
            y -= height
            draw_page_number()
            c.showPage()
            page_number += 1
            c.setFont(FONT_NAME, FONT_SIZE)
            y = PAGE_HEIGHT - MARGIN_TOP
            current_data = [table_header, row]

    if current_data:
        height = draw_table(current_data, y)
        y -= height

    draw_page_number()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# Interfaces

def generate_general_report(user, start_date, end_date, donations):
    return generate_donation_report_pdf({
        "company": user.profile.company,
        "user": user,
        "start_date": start_date,
        "end_date": end_date,
        "donations": donations
    })

def generate_employee_report_pdf(employee, donations, start_date, end_date):
    return generate_donation_report_pdf({
        "company": employee.owner,
        "employee": employee,
        "start_date": start_date,
        "end_date": end_date,
        "donations": donations
    })

def generate_donor_report_pdf(donor, donations, start_date, end_date):
    return generate_donation_report_pdf({
        "company": donor.owner,
        "donor": donor,
        "start_date": start_date,
        "end_date": end_date,
        "donations": donations
    })
