from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf():
    # Ustalamy ścieżkę do folderu projektu
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(project_folder, "custom_raport.pdf")
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    flowables = []

    # Header
    styles = getSampleStyleSheet()
    header_text = "<u><b>Custom Report</b></u>"
    header = Paragraph(header_text, styles['Heading1'])
    flowables.append(header)
    flowables.append(Spacer(1, 12))  # Spacer

    # Reporting Period
    period_text = "<b>Reporting Period:</b> [Reporting Period]"
    period = Paragraph(period_text, styles['Normal'])
    flowables.append(period)
    flowables.append(Spacer(1, 12))  # Spacer

    # Summary
    summary_text = "<b>Summary:</b>"
    summary = Paragraph(summary_text, styles['Normal'])
    flowables.append(summary)

    # Detailed Information
    details_text = "<b>Detailed Information:</b>"
    details = Paragraph(details_text, styles['Normal'])
    flowables.append(details)

    # Expenses
    expenses_text = "<b>Expenses:</b>"
    expenses = Paragraph(expenses_text, styles['Normal'])
    flowables.append(expenses)

    # Expenses Table (Sample Table)
    expenses_data = [['Category', 'Amount', 'Description'],
                    ['Food', '50', 'Dinner'],
                    ['Transportation', '30', 'Bus Ticket'],
                    ['Entertainment', '20', 'Movie Tickets']]
    expenses_table = Table(expenses_data)
    expenses_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(expenses_table)
    flowables.append(Spacer(1, 12))  # Spacer

    # Incomes
    incomes_text = "<b>Incomes:</b>"
    incomes = Paragraph(incomes_text, styles['Normal'])
    flowables.append(incomes)

    # Incomes Table (Sample Table)
    incomes_data = [['Source', 'Amount', 'Description'],
                    ['Salary', '1000', 'May Salary'],
                    ['Sales', '200', 'Items on eBay']]
    incomes_table = Table(incomes_data)
    incomes_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(incomes_table)
    flowables.append(Spacer(1, 12))  # Spacer

    # Final Summary (Sample Summary)
    final_summary_text = "<b>Final Summary:</b>"
    final_summary = Paragraph(final_summary_text, styles['Normal'])
    flowables.append(final_summary)
    final_summary_details_text = "Total Expenses: [Total Expenses]<br/>Total Income: [Total Income]<br/>Net Balance: [Net Balance]"
    final_summary_details = Paragraph(final_summary_details_text, styles['Normal'])
    flowables.append(final_summary_details)


    doc.build(flowables)

    return file_name