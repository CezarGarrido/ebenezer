import locale
from datetime import datetime
from core.escbuilder.escprinter import ESCPrinter
from django.core.exceptions import ObjectDoesNotExist

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

CHARS_PER_LINE = 80
CHARS_PER_LINE_CONDENSED = 136
LEFT_MARGIN = 2
RIGHT_MARGIN = 1
RIGHT_MARGIN_CONDENSED = 2
MAX_LINE_WIDTH = CHARS_PER_LINE - LEFT_MARGIN - RIGHT_MARGIN
MAX_LINE_WIDTH_CONDENSED = CHARS_PER_LINE_CONDENSED - LEFT_MARGIN - RIGHT_MARGIN_CONDENSED

def _linha_pontilhada(esquerda, direita, largura=MAX_LINE_WIDTH):
    return f"{esquerda}{'.' * (largura - len(esquerda) - len(direita))}{direita}"

def print_centered(printer, text):
    printer.print(text.center(MAX_LINE_WIDTH))
    printer.lineFeed()

def print_centered_condensed(printer, text):
    printer.print(text.center(MAX_LINE_WIDTH_CONDENSED))
    printer.lineFeed()

def print_line_side_by_side(printer, left, right):
    min_margin = 2
    total_len = len(left) + len(right) + min_margin
    if total_len >= MAX_LINE_WIDTH:
        result = left + ' ' * min_margin + right
    else:
        space_between = MAX_LINE_WIDTH - len(left) - len(right)
        result = left + (' ' * space_between) + right
    printer.print(result)
    printer.lineFeed()

def print_line_side_by_side_condensed(printer, left, right):
    min_margin = 2
    total_len = len(left) + len(right) + min_margin
    if total_len >= MAX_LINE_WIDTH_CONDENSED:
        result = left + ' ' * min_margin + right
    else:
        space_between = MAX_LINE_WIDTH_CONDENSED - len(left) - len(right)
        result = left + (' ' * space_between) + right
    printer.print(result)
    printer.lineFeed()

def generate_report_header(printer, company, title):
    print_line_side_by_side(printer, company.name, f"Emissão: {datetime.now().strftime('%d/%m/%Y')}")
    try:
        cnpj = company.legalentity.cnpj or "-"
    except ObjectDoesNotExist:
        cnpj = "-"
    print_line_side_by_side(printer, "Inscrição Estadual Nº ISENTO", f"C.G.C Nº: {cnpj}")
    printer.lineFeed(3)
    printer.bold(True)
    print_centered(printer, title)
    printer.bold(False)
    printer.lineFeed(3)

def generate_table_header(printer):
    printer.condensed(True)
    print_centered_condensed(printer, "-" * MAX_LINE_WIDTH_CONDENSED)
    header_line = (
        "CÓDIGO".ljust(10) +
        "DATA".ljust(12) +
        "DOADOR".ljust(38) + 
        "VALOR PREVISTO".rjust(22) + 
        "VALOR RECEBIDO".rjust(25) + 
        "DIFERENÇA".rjust(20)
    )
    printer.print(header_line)
    printer.lineFeed()
    print_centered_condensed(printer, "-" * MAX_LINE_WIDTH_CONDENSED)
    printer.condensed(False)

def generate_donation_row(printer, donation):
    row_line = (
        f"{donation.id}".ljust(10) +
        (donation.expected_at.strftime('%d/%m/%Y') if donation.expected_at else "-").ljust(12) +
        f"{donation.donor.id} - {donation.donor.name}".ljust(38) +
        locale.currency(donation.amount or 0, grouping=True).rjust(22) +
        locale.currency(donation.paid_amount or 0, grouping=True).rjust(25)
    )
    valor_previsto = donation.amount or 0
    valor_pago = donation.paid_amount or 0
    dif_percentual = ((valor_pago - valor_previsto) / valor_previsto * 100) if valor_previsto > 0 else 0.0
    row_line += f"{dif_percentual:.2f}%".rjust(20)
    printer.print(row_line)
    printer.lineFeed()

def generate_report_footer(printer, total_previsto, total_recebido, page=1):
    print_centered(printer, "-" * MAX_LINE_WIDTH)
    printer.lineFeed()
    diferenca_total = ((total_recebido - total_previsto) / total_previsto * 100) if total_previsto > 0 else 0.0
    printer.print(_linha_pontilhada("Total Previsto", f":{locale.currency(total_previsto, grouping=True)}"))
    printer.lineFeed()
    printer.print(_linha_pontilhada("Total Recebido", f":{locale.currency(total_recebido, grouping=True)}"))
    printer.lineFeed()
    printer.print(_linha_pontilhada("Diferença", f":{diferenca_total:.2f}%"))
    printer.lineFeed(2)
    print_centered(printer, f"--- Página {page} ---")
    printer.formFeed()
    printer.reset()

def generate_page_footer(printer, total_previsto, total_recebido, page):
    print_centered_condensed(printer, "-" * MAX_LINE_WIDTH_CONDENSED)
    printer.lineFeed()
    printer.print(_linha_pontilhada("Subtotal Previsto", f":{locale.currency(total_previsto, grouping=True)}", MAX_LINE_WIDTH_CONDENSED))
    printer.lineFeed()
    printer.print(_linha_pontilhada("Subtotal Recebido", f":{locale.currency(total_recebido, grouping=True)}", MAX_LINE_WIDTH_CONDENSED))
    printer.lineFeed()
    print_centered_condensed(printer, f"--- Página {page} ---")
    printer.lineFeed()

def generate_donor_or_employee_report(entity, start_date, end_date, donations, title):
    printer = ESCPrinter()
    printer.initialize()
    printer.setMargins(2, 80)

    generate_report_header(printer, entity.owner, title)
    print_line_side_by_side(printer, f"Código..............: {entity.id}", "")
    print_line_side_by_side(printer, f"{title.split('POR ')[-1].capitalize()}..............: {entity.name.upper()}", "")
    print_line_side_by_side(printer, f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}", "")
    printer.lineFeed()

    generate_table_header(printer)
    total_previsto = 0
    total_recebido = 0
    page = 1
    first_page_items = 42
    other_pages_items = 60
    items_per_page = first_page_items
    item_count = 0

    printer.condensed(True)

    for donation in list(donations):
        total_previsto += donation.amount or 0
        total_recebido += donation.paid_amount or 0
        generate_donation_row(printer, donation)
        item_count += 1
        if item_count == items_per_page:
            generate_page_footer(printer, total_previsto, total_recebido, page)
            page += 1
            item_count = 0
            items_per_page = other_pages_items

    printer.condensed(False)
    generate_report_footer(printer, total_previsto, total_recebido, page)
    return printer.build()

def generate_donor_report(donor, start_date, end_date, donations):
    return generate_donor_or_employee_report(donor, start_date, end_date, donations, "RELATÓRIO DE VALORES RECEBIDOS POR DOADOR")

def generate_employee_report(employee, start_date, end_date, donations):
    return generate_donor_or_employee_report(employee, start_date, end_date, donations, "RELATÓRIO DE VALORES RECEBIDOS POR FUNCIONÁRIO")

def generate_general_report(user, start_date, end_date, donations):
    printer = ESCPrinter()
    printer.initialize()
    printer.setMargins(2, 80)

    generate_report_header(printer, user.profile.company, "RELATÓRIO GERAL DE DOAÇÕES")
    print_line_side_by_side(printer, f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}", "")
    printer.lineFeed()

    generate_table_header(printer)
    total_previsto = 0
    total_recebido = 0
    page = 1
    first_page_items = 45
    other_pages_items = 60
    items_per_page = first_page_items
    item_count = 0

    printer.condensed(True)

    for donation in list(donations):
        total_previsto += donation.amount or 0
        total_recebido += donation.paid_amount or 0
        generate_donation_row(printer, donation)
        item_count += 1
        if item_count == items_per_page:
            generate_page_footer(printer, total_previsto, total_recebido, page)
            page += 1
            item_count = 0
            items_per_page = other_pages_items

    printer.condensed(False)
    generate_report_footer(printer, total_previsto, total_recebido, page)
    return printer.build()
