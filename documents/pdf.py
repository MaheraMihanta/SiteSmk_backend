from io import BytesIO

from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_contract_pdf(contract):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(40, height - 50, 'Contrat de Location')

    pdf.setFont('Helvetica', 11)
    y = height - 90
    details = [
        f'Contrat N°: {contract.number}',
        f'Date: {contract.issue_date}',
        f'Status: {contract.status}',
    ]
    rental = contract.rental
    if rental:
        details += [
            f'Client: {rental.customer.get_full_name() or rental.customer.username}',
            f'Vehicule: {rental.vehicle.plate_number} - {rental.vehicle.make} {rental.vehicle.model}',
            f'Période: {rental.start_date} au {rental.end_date}',
            f'Tarif journalier: {rental.daily_rate_at_booking}',
            f'Caution: {rental.deposit_amount}',
        ]

    for line in details:
        pdf.drawString(40, y, line)
        y -= 18

    y -= 10
    pdf.drawString(40, y, 'Signature du client: __________________________')
    y -= 30
    pdf.drawString(40, y, 'Signature du propriétaire: _____________________')

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    filename = f"contract_{contract.number}.pdf"
    contract.pdf_file.save(filename, ContentFile(buffer.read()), save=True)
    return contract


def generate_invoice_pdf(invoice):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(40, height - 50, 'Facture')

    pdf.setFont('Helvetica', 11)
    y = height - 90
    details = [
        f'Facture N°: {invoice.number}',
        f'Date: {invoice.issue_date}',
        f'Status: {invoice.status}',
        f'Sous-total: {invoice.subtotal}',
        f'TVA ({invoice.tax_rate}%): {invoice.tax_amount}',
        f'Total: {invoice.total}',
    ]
    rental = invoice.rental
    if rental:
        details = [
            f'Client: {rental.customer.get_full_name() or rental.customer.username}',
            f'Vehicule: {rental.vehicle.plate_number} - {rental.vehicle.make} {rental.vehicle.model}',
            f'Période: {rental.start_date} au {rental.end_date}',
        ] + details

    for line in details:
        pdf.drawString(40, y, line)
        y -= 18

    y -= 10
    pdf.drawString(40, y, 'Signature (après impression): __________________________')

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    filename = f"invoice_{invoice.number}.pdf"
    invoice.pdf_file.save(filename, ContentFile(buffer.read()), save=True)
    return invoice
