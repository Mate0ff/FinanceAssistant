from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def format_amount(value):
    if value == int(value):
        return int(value)  
    else:
        return value  


def generate_pdf(from_date,to_date,all_expenses, all_incomes):
    # Ustalamy ścieżkę do folderu projektu
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(project_folder, "custom_report.pdf")
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    flowables = []

    # Header
    styles = getSampleStyleSheet()
    header_text = "<b>Custom Report</b>"
    header = Paragraph(header_text, styles['Title'])
    flowables.append(header)
    flowables.append(Spacer(1, 75))  # Spacer

    # Reporting Period
    period_text = f"<b>Reporting Period:</b> From: {from_date} To: {to_date}"
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
    flowables.append(Spacer(1, 20))  # Spacer

    # Incomes
    income_text = "<b>Income:</b>"
    income = Paragraph(income_text, styles['Normal'])
    flowables.append(income)

    # Incomes Table (Sample Table)
    income_data = [['Name','Category','Date', 'Amount']]
    
    for income in all_incomes:
        table_var = [income.name,income.category.name,income.date,format_amount(income.amount)]
        income_data.append(table_var)

    income_table = Table(income_data)
    income_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(income_table)
    flowables.append(Spacer(1, 20))  # Spacer

    # Expenses
    expenses_text = "<b>Expenses:</b>"
    expenses = Paragraph(expenses_text, styles['Normal'])
    flowables.append(expenses)

    # Expenses Table (Sample Table)
    expenses_data = [['Name','Category','Date', 'Amount']]
    
    for expense in all_expenses:
        table_var = [expense.name,expense.category.name,expense.date,format_amount(expense.amount)]
        expenses_data.append(table_var)


    expenses_table = Table(expenses_data)
    expenses_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(expenses_table)
    flowables.append(Spacer(1, 12))  # Spacer

    # Final Summary (Sample Summary)
    final_summary_text = "<b>Final Summary:</b>"
    final_summary = Paragraph(final_summary_text, styles['Normal'])
    flowables.append(final_summary)


    total_expenses = sum(expense.amount for expense in all_expenses)
    total_income = sum(income.amount for income in all_incomes)

    final_summary_details_text = f"Total Income: [{format_amount(total_income)}]<br/>Total Expenses: [{format_amount(total_expenses)}]<br/>Net Balance: [{format_amount(total_income-total_expenses)}]"
    final_summary_details = Paragraph(final_summary_details_text, styles['Normal'])
    flowables.append(final_summary_details)


    doc.build(flowables)

    return file_name