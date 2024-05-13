from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import numpy as np
import os

# Used to change 100.0 to 100 
def format_amount(value):
    if value == int(value):
        return int(value)  
    else:
        return value  


def generate_pdf(from_date,to_date,all_expenses, all_incomes):

    # Path to project directory
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(project_folder, "custom_report.pdf")
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    flowables = []

    # Sorting transactions based on date
    all_expenses.sort(key=lambda x: x.date, reverse=True)
    all_incomes.sort(key=lambda x: x.date, reverse=True)

    # Calculating agregate values of expenses and income
    total_expenses = sum(expense.amount for expense in all_expenses)
    total_income = sum(income.amount for income in all_incomes)

    # Descriptive statistics
    mean_expense = np.mean([expense.amount for expense in all_expenses])
    mean_income = np.mean([income.amount for income in all_incomes])

    std_expense = np.std([expense.amount for expense in all_expenses])
    std_income = np.std([income.amount for income in all_incomes])

    median_expense = np.median([expense.amount for expense in all_expenses])
    median_income = np.median([income.amount for income in all_incomes])

    min_expense = min([expense.amount for expense in all_expenses])
    min_income = min([income.amount for income in all_incomes])

    max_expense = max([expense.amount for expense in all_expenses])
    max_income = max([income.amount for income in all_incomes])

    # Dictionary to track total amounts for each category
    expense_category_totals = {}
    income_category_totals = {}
    
    # Dictionary to track total amounts for each expense type
    expense_type_totals = {}

    # Header
    styles = getSampleStyleSheet()
    header = Paragraph("<u><b>Custom Report</b></u>", styles['Heading1'])
    flowables.append(header)
    flowables.append(Spacer(1, 50))  

    # Reporting Period
    period = Paragraph("<b>Reporting Period:</b>", styles['Heading2'])
    flowables.append(period) 

    peroid_txt = Paragraph(f"From: {from_date}, to: {to_date}",styles['Normal'])
    flowables.append(peroid_txt) 

    # Summary
    summary = Paragraph("<b>Summary:</b>", styles['Heading2'])
    flowables.append(summary)
    summary_txt = Paragraph("This report provides a detailed overview of the incomes and expenses for a specific period. It offers insights into the financial activities during this time frame, helping to analyze the financial health and performance. In addition to presenting income and expenses, the report offers key statistics to enhance understanding.")
    flowables.append(summary_txt)
    flowables.append(Spacer(1, 20))

    # Incomes
    income = Paragraph("<b>Income:</b>", styles['Heading2'])
    flowables.append(income)

    # Incomes Table
    income_data = [['Name','Category','Date', 'Amount']]
    
    for income in all_incomes:
        table_var = [income.name,income.category.name,income.date,format_amount(income.amount)]
        income_data.append(table_var)
        # Sum of incomes of the same category
        if income.category.name not in income_category_totals:
            income_category_totals[income.category.name] = income.amount
        else:
            income_category_totals[income.category.name] += income.amount

    income_table = Table(income_data)
    income_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(income_table)
    flowables.append(Spacer(1, 15))  

    # Desctriptive statisctics for income
    stat_income_txt = Paragraph("<b>Descriptive statistics:</b>", styles['Heading3'])
    flowables.append(stat_income_txt)

    count_income_txt = Paragraph(f"Count: {len(all_incomes)}",styles['Normal'])
    flowables.append(count_income_txt)

    min_income_txt = Paragraph(f"Min: {format_amount(min_income)}",styles['Normal'])
    flowables.append(min_income_txt)

    max_income_txt = Paragraph(f"Max: {format_amount(max_income)}",styles['Normal'])
    flowables.append(max_income_txt)
    
    mean_income_txt = Paragraph(f"Mean: {format_amount(round(mean_income,2))}",styles['Normal'])
    flowables.append(mean_income_txt)

    std_income_txt = Paragraph(f"Standard deviation: {format_amount(round(std_income,2))}",styles['Normal'])
    flowables.append(std_income_txt)

    median_income_txt = Paragraph(f"Median: {format_amount(round(median_income,2))}",styles['Normal'])
    flowables.append(median_income_txt)

    flowables.append(Spacer(1, 10)) 

    # Sum of income categories
    cat_income_txt = Paragraph("<b>Income by category:</b>", styles['Heading3'])
    flowables.append(cat_income_txt)

    for category, total_amount in income_category_totals.items():
        text_cat = Paragraph(f"Category: <b>{category}</b>", styles['Normal'])
        flowables.append(text_cat)
        text_rest = Paragraph(f"Total amount: {format_amount(total_amount)}, percentage share {round(format_amount(total_amount/total_income*100),2)}%", styles['Normal'])
        flowables.append(text_rest)
        flowables.append(Spacer(1, 5)) 

    flowables.append(Spacer(1, 20)) 

    # Expenses
    expenses = Paragraph("<b>Expenses:</b>", styles['Heading2'])
    flowables.append(expenses)

    # Expenses Table (Sample Table)
    expenses_data = [['Name','Category','Date', 'Amount']]
    
    for expense in all_expenses:
        table_var = [expense.name,expense.category.name,expense.date,format_amount(expense.amount)]
        expenses_data.append(table_var)
        #Sum of expenses of the same category
        if expense.category.name not in expense_category_totals:
            expense_category_totals[expense.category.name] = expense.amount
        else:
            expense_category_totals[expense.category.name] += expense.amount
        
        if expense.expense_type.name not in expense_type_totals:
            expense_type_totals[expense.expense_type.name] = expense.amount
        else:
            expense_type_totals[expense.expense_type.name] += expense.amount

    expenses_table = Table(expenses_data)
    expenses_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(expenses_table)
    flowables.append(Spacer(1, 15))  

    # Desctriptive statisctics for expenses
    stat_expense_txt = Paragraph("<b>Descriptive statistics:</b>", styles['Heading3'])
    flowables.append(stat_expense_txt)

    count_expense_txt = Paragraph(f"Count: {len(all_expenses)}",styles['Normal'])
    flowables.append(count_expense_txt)

    min_expense_txt = Paragraph(f"Min: {format_amount(min_expense)}",styles['Normal'])
    flowables.append(min_expense_txt)

    max_expense_txt = Paragraph(f"Max: {format_amount(max_expense)}",styles['Normal'])
    flowables.append(max_expense_txt)

    mean_expense_txt = Paragraph(f"Mean: {format_amount(round(mean_expense,2))}",styles['Normal'])
    flowables.append(mean_expense_txt)

    std_expense_txt = Paragraph(f"Standard deviation: {format_amount(round(std_expense,2))}",styles['Normal'])
    flowables.append(std_expense_txt)

    median_expense_txt = Paragraph(f"Median: {format_amount(round(median_expense,2))}",styles['Normal'])
    flowables.append(median_expense_txt)

    flowables.append(Spacer(1, 10)) 

    # Sum of expense categories
    cat_expense_txt = Paragraph("<b>Expenses by category:</b>", styles['Heading3'])
    flowables.append(cat_expense_txt)

    for category, total_amount in expense_category_totals.items():
        text_cat = Paragraph(f"Category: <b>{category}</b>", styles['Normal'])
        flowables.append(text_cat)
        text_rest = Paragraph(f"Total amount: {format_amount(total_amount)}, percentage share {round(format_amount(total_amount/total_expenses*100),2)}%", styles['Normal'])
        flowables.append(text_rest)
        flowables.append(Spacer(1, 5)) 

    flowables.append(Spacer(1, 10))  

    # Sum of expense types
    type_expense_txt = Paragraph("<b>Expenses by type:</b>", styles['Heading3'])
    flowables.append(type_expense_txt)

    for type, total_amount in expense_type_totals.items():
        text_typ = Paragraph(f"Type: <b>{type}</b>", styles['Normal'])
        flowables.append(text_typ)
        text_rest = Paragraph(f"Total amount: {format_amount(total_amount)}, percentage share {round(format_amount(total_amount/total_expenses)*100,2)}%", styles['Normal'])
        flowables.append(text_rest)
        flowables.append(Spacer(1, 5))   

    flowables.append(Spacer(1, 20)) 
    # Final Summary
    final_summary = Paragraph("<b>Final Summary:</b>", styles['Normal'])
    flowables.append(final_summary)

    flowables.append(Spacer(1, 20)) 

    # Final summary
    final_summary_details_text = f"Total Income: [{format_amount(total_income)}]<br/>Total Expenses: [{format_amount(total_expenses)}]<br/>Net Balance: [{format_amount(total_income-total_expenses)}]"
    final_summary_details = Paragraph(final_summary_details_text, styles['Normal'])
    flowables.append(final_summary_details)


    doc.build(flowables)

    return file_name