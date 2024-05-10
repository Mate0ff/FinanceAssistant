from flask import render_template, redirect, url_for, flash,request, session
from app.forms import RegistrationForm, LoginForm, CreateExpenseForm, CreateIncomeForm, LimitForm,DatePickerForm
from app.models import User, Expense, ExpenseType, ExpenseCategory, IncomeCategory, Income
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, datetime


@app.context_processor
def utility_processor():
    def is_expense(transaction):
        return isinstance(transaction, Expense)

    def is_income(transaction):
        return isinstance(transaction, Income)

    return dict(is_expense=is_expense, is_income=is_income)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    expenses = Expense.query.filter_by(user=current_user).all()
    incomes = Income.query.filter_by(user=current_user).all()

    incomes_all = [income for income in incomes]
    expenses_all = [expense for expense in expenses]


    total_expenses = sum(expense.amount for expense in expenses)
    total_incomes = sum(income.amount for income in incomes)

    exp_needs = Expense.query.filter_by(user=current_user, type_id=1).all()
    exp_wants = Expense.query.filter_by(user=current_user, type_id=2).all()
    exp_other = Expense.query.filter_by(user=current_user, type_id=3).all()

    balance = total_incomes - total_expenses

    transactions = expenses + incomes

    abc = transactions.copy()

    transactions.sort(key=lambda x: x.date, reverse=True)
    abc.sort(key=lambda x: x.date, reverse=False)

    current_user.saldo = round(balance, 2)
    db.session.commit()

    table = []
    set_variable = set()

    for expense in expenses:
        set_variable.add(str(expense.date.strftime('%m.%Y')))
        
    for x in set_variable:
        sum_variable_needs = 0
        sum_variable_wants = 0
        sum_variable_other = 0
        dict_variable = dict()
        dict_variable["date"] = x
      
        for expense in expenses:
            if expense.date.strftime('%m') == x.split('.')[0] and expense.date.strftime('%Y') == x.split('.')[1] and expense in exp_needs:
                sum_variable_needs += expense.amount
            elif expense.date.strftime('%m') == x.split('.')[0] and expense.date.strftime('%Y') == x.split('.')[1] and expense in exp_wants:
                sum_variable_wants += expense.amount
            elif expense.date.strftime('%m') == x.split('.')[0] and expense.date.strftime('%Y') == x.split('.')[1] and expense in exp_other:
                sum_variable_other += expense.amount
        
        dict_variable["amount_needs"] = sum_variable_needs
        dict_variable["amount_wants"] = sum_variable_wants
        dict_variable["amount_other"] = sum_variable_other
        table.append(dict_variable)

    form = DatePickerForm()

    month_year = date.today().strftime('%m.%Y')
   
    if form.validate_on_submit():
        selected_date = form.date.data
        month_year = selected_date.strftime('%m.%Y')
        expenses = Expense.query.filter_by(user=current_user, date = selected_date).all()
        incomes = Income.query.filter_by(user=current_user, date = selected_date).all()
        transactions = expenses + incomes
        transactions.sort(key=lambda x: x.date, reverse=True)
    
    lables_all = []

    month_trans = []

    month_expenses = []
    plot1_data=[]
    exp_dt = []

    month_incomes = []
    plot2_data=[]
    inc_dt = []


    # LISTA Z DATA WSZYSTKICH TRANSAKCJI W OBECNYM MIESIACU
    for transaction in abc:
        if transaction.date.strftime("%m.%Y") == month_year: 
            lables_all.append(str(transaction.date))
            month_trans.append(transaction)

    lables_all = list(set(lables_all))
    
    dates_datetime = [datetime.strptime(data, "%Y-%m-%d") for data in lables_all]
    sorted_dates = sorted(dates_datetime)
    sorted_lables = [data.strftime("%Y-%m-%d") for data in sorted_dates]

    # ZBIERAM SZYSTKIE EXPENSES Z OBECNEGO MIESIACA
    for expense in expenses_all:
        if expense.date.strftime("%m.%Y") == month_year:  
            month_expenses.append(expense)

    for expense in month_expenses:
        exp_dt.append(str(expense.date))
    exp_dt = set(exp_dt)

    # ZBIERAM SZYSTKIE INCOMES Z OBECNEGO MIESIACA
    for income in incomes_all:
        if income.date.strftime("%m.%Y") == month_year:  
            month_incomes.append(income)

    for income in month_incomes:
        inc_dt.append(str(income.date))
    inc_dt = set(inc_dt)


    # Dostaje dni bez wydatkow/przychodow w miesiacu

    exc_incomes = list(set(lables_all).symmetric_difference(inc_dt))
    exc_expenses = list(set(lables_all).symmetric_difference(exp_dt))


    # sprawdzam czy transakcja jest przychoden czy wydatkiem zeby wypisac ja na dobrym wykresie

    for trans in month_trans:
        if  isinstance(trans, Expense):
             plot1_data.append((str(trans.date),trans.amount))
        elif isinstance(trans, Income):		
            plot2_data.append((str(trans.date),trans.amount))

    

    for i in exc_expenses:
        plot1_data.append((str(i),0))

    for i in exc_incomes :
        plot2_data.append((str(i),0))
    

    plot1_data = sorted(plot1_data, key=lambda x: x[0])
    plot2_data = sorted(plot2_data, key=lambda x: x[0])

    # Sprawdzam czy jednego dnia sa wiecej niz 1 wydatek/przychodw
    new1_data = []
    new2_data = []

    for date1, value1 in plot1_data:
        found = False
        for i in range(len(new1_data)):
            if new1_data[i][0] == date1:
                new1_data[i] = (date1, new1_data[i][1] + value1)
                found = True
                break
        if not found:
            new1_data.append((date1, value1))

    for date2, value2 in plot2_data:
        found = False
        for i in range(len(new2_data)):
            if new2_data[i][0] == date2:
                new2_data[i] = (date2, new2_data[i][1] + value2)
                found = True
                break
        if not found:
            new2_data.append((date2, value2))


    values_exp = [row[1] for row in new1_data]
    values_inc = [row[1] for row in new2_data]

        
    return render_template('home.html', transactions=transactions,sorted_lables=sorted_lables,
                            values_exp=values_exp,values_inc=values_inc,table=table,form=form)

@app.route("/expenses", methods=['GET', 'POST'])
@login_required
def expenses():
    expenses = Expense.query.filter_by(user=current_user).all()
    expenses.sort(key=lambda x: x.date, reverse=True)

    exp_needs = Expense.query.filter_by(user=current_user, type_id=1).all()
    exp_wants = Expense.query.filter_by(user=current_user, type_id=2).all()
    exp_other = Expense.query.filter_by(user=current_user, type_id=3).all()

    expenses_all = []
    table = []
    set_variable = set()

    # dictionary of expenses dates in format mm.YYYY
    for expense in expenses:
        set_variable.add(str(expense.date.strftime('%m.%Y')))
        expenses_all.append(expense)
   
    expenses_all.sort(key=lambda x: x.date, reverse=False)

    # checking if mm.YYYY from dictionary equals mm.YYYY of expense
    for x in set_variable:
        sum_variable_needs = 0
        sum_variable_wants = 0
        sum_variable_other = 0
        dict_variable = dict()
        dict_variable["date"] = x
      
        for expense in expenses:
            if expense.date.strftime('%m') == x.split('.')[0] and expense.date.strftime('%Y') == x.split('.')[1] and expense in exp_needs:
                sum_variable_needs += expense.amount
            elif expense.date.strftime('%m') == x.split('.')[0] and expense.date.strftime('%Y') == x.split('.')[1] and expense in exp_wants:
                sum_variable_wants += expense.amount
            elif expense.date.strftime('%m') == x.split('.')[0] and expense.date.strftime('%Y') == x.split('.')[1] and expense in exp_other:
                sum_variable_other += expense.amount
        
        dict_variable["amount_needs"] = sum_variable_needs
        dict_variable["amount_wants"] = sum_variable_wants
        dict_variable["amount_other"] = sum_variable_other
        table.append(dict_variable)

    # tabela ktory wyglada tak ("data", expense)

    form = DatePickerForm()

    # bar plot and date picker
    ###########################################################################################
    month_year = date.today().strftime('%m.%Y')

    if form.validate_on_submit():
        selected_date = form.date.data
        month_year = selected_date.strftime('%m.%Y')
        expenses = Expense.query.filter_by(user=current_user, date=selected_date).all()

    plot2_list = []

    for expense in expenses_all:
        if expense.date.strftime("%m.%Y") == month_year:  
            plot2_list.append(expense)

    plot2_data=[]
    variable_needs = 0
    variable_wants = 0
    variable_other = 0

    for expense in plot2_list:
        element = (str(expense.date),expense.amount)
        plot2_data.append(element)
        if expense.expense_type.name.lower() == 'needs':
            variable_needs += expense.amount
        if expense.expense_type.name.lower() == 'wants':
            variable_wants += expense.amount
        if expense.expense_type.name.lower() == 'other':
            variable_other += expense.amount
        
    lables_pie = ["wants","needs","other"]
    values_pie =[variable_wants,variable_needs,variable_other]

    new_data = []

    for date1, value1 in plot2_data:
        found = False
        for i in range(len(new_data)):
            if new_data[i][0] == date1:
                new_data[i] = (date1, new_data[i][1] + value1)
                found = True
                break
        if not found:
            new_data.append((date1, value1))

    lables_bar = list(set([row[0] for row in plot2_data]))

    dates_datetime = [datetime.strptime(data, "%Y-%m-%d") for data in lables_bar]
    sorted_dates = sorted(dates_datetime)
    sorted_lables = [data.strftime("%Y-%m-%d") for data in sorted_dates]


    values_bar = [row[1] for row in new_data]
    
    return render_template('expenses.html', expenses=expenses,
                            table=table, values_bar=values_bar,sorted_lables=sorted_lables, values_pie = values_pie, lables_pie = lables_pie ,form=form)

@app.route("/income", methods=['GET', 'POST'])
@login_required
def income():
    incomes = Income.query.filter_by(user=current_user).all()
    incomes.sort(key=lambda x: x.date, reverse=True)

    income_all = []

    for income in incomes:
        income_all.append(income)
    income_all.sort(key=lambda x: x.date, reverse=False)

    form = DatePickerForm()

    month_year = date.today().strftime('%m.%Y')

    # Jeśli formularz został przesłany
    if form.validate_on_submit():
        selected_date = form.date.data
        month_year = selected_date.strftime('%m.%Y')
        incomes = Income.query.filter_by(user=current_user, date = selected_date).all()
    
    plot2_list = []

    for income in income_all:
        if income.date.strftime("%m.%Y") == month_year:  
            plot2_list.append(income)

    plot2_data=[]
    variable_salary = 0
    variable_bonus = 0
    variable_gift = 0
    variable_rent = 0
    variable_scholarship = 0
    variable_investment = 0
    variable_other = 0


    for income in plot2_list:
        element = (str(income.date),income.amount)
        plot2_data.append(element)
        if income.category.name.lower() == 'salary':
            variable_salary += income.amount
        if income.category.name.lower() == 'bonus':
            variable_bonus += income.amount
        if income.category.name.lower() == 'gift':
            variable_gift += income.amount
        if income.category.name.lower() == 'rent':
            variable_rent += income.amount
        if income.category.name.lower() == 'scholarship':
            variable_scholarship += income.amount
        if income.category.name.lower() == 'investment':
            variable_investment += income.amount
        if income.category.name.lower() == 'other':
            variable_other += income.amount
        
    lables_pie = ['Salary','Bonus','Gift','Rent','Scholarship','Investment','Other']
    values_pie =[variable_salary,variable_bonus,variable_gift,variable_rent,variable_scholarship,variable_investment,variable_other]


    new_data = []

    for date1, value1 in plot2_data:
        found = False
        for i in range(len(new_data)):
            if new_data[i][0] == date1:
                new_data[i] = (date1, new_data[i][1] + value1)
                found = True
                break
        if not found:   
            new_data.append((date1, value1))


    lables_bar = list(set([row[0] for row in plot2_data]))

    dates_datetime = [datetime.strptime(data, "%Y-%m-%d") for data in lables_bar]
    sorted_dates = sorted(dates_datetime)
    sorted_lables = [data.strftime("%Y-%m-%d") for data in sorted_dates]

    values_bar = [row[1] for row in new_data]
 

    return render_template('income.html', incomes=incomes, sorted_lables=sorted_lables,values_bar=values_bar,lables_pie=lables_pie,values_pie=values_pie,form=form)

@app.route("/summary")
@login_required
def summary():
    return render_template('summary.html')

@app.route("/account")
@login_required
def account():
    if current_user.gender == 'Male':
        avatar = url_for('static', filename='avatars/avatar-male.png')
    else:
        avatar = url_for('static', filename='avatars/avatar-female.png')
    return render_template('account.html', avatar=avatar)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email or password!','register')
    return render_template('login.html', form = form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,email = form.email.data,gender = form.gender.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','register')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))


@app.route("/expenses/new", methods=['GET', 'POST'])
@login_required
def new_expense(): 
    form = CreateExpenseForm()
    if form.validate_on_submit():
        category = ExpenseCategory.query.filter_by(name=form.category.data).first()
        type = ExpenseType.query.filter_by(name=form.type.data).first()
        expense = Expense(name = form.name.data, category = category, expense_type = type, date = form.date.data,amount = form.amount.data,note = form.note.data, user = current_user)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('expenses'))
    return render_template('exp_create.html', form=form)    

@app.route("/income/new", methods=['GET', 'POST'])
@login_required
def new_income(): 
    form = CreateIncomeForm()
    if form.validate_on_submit():
        category = IncomeCategory.query.filter_by(name=form.category.data).first()
        income = Income(name = form.name.data, category = category,date = form.date.data,amount = form.amount.data,note = form.note.data, user = current_user)
        db.session.add(income)
        db.session.commit()
        return redirect(url_for('income'))
    return render_template('inc_create.html', form=form)    


@app.route("/expenses/<int:expense_id>/update", methods=['GET', 'POST'])
@login_required
def update_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user=current_user).first_or_404()
    form = CreateExpenseForm()
    if form.validate_on_submit():
        category = ExpenseCategory.query.filter_by(name=form.category.data).first()
        type = ExpenseType.query.filter_by(name=form.type.data).first()
        expense.name = form.name.data
        expense.expense_type = type
        expense.category = category
        expense.date = form.date.data
        expense.amount = form.amount.data
        expense.note = form.note.data
        db.session.commit()
        return redirect(url_for('expenses'))
    form.name.data = expense.name
    form.type.data = expense.expense_type
    form.category.data = expense.category
    form.date.data = expense.date
    form.amount.data = expense.amount
    form.note.data = expense.note
    return render_template('edit_expense.html',form=form)


@app.route("/income/<int:income_id>/update", methods=['GET', 'POST'])
@login_required
def update_income(income_id):
    income = Income.query.filter_by(id=income_id, user=current_user).first_or_404()
    form = CreateIncomeForm()
    if form.validate_on_submit():
        category = IncomeCategory.query.filter_by(name=form.category.data).first()
        income.name = form.name.data
        income.category = category
        income.date = form.date.data
        income.amount = form.amount.data
        income.note = form.note.data
        db.session.commit()
        return redirect(url_for('income'))
    form.name.data = income.name
    form.category.data = income.category
    form.date.data = income.date
    form.amount.data = income.amount
    form.note.data = income.note
    return render_template('edit_income.html',form=form)

@app.route("/income/<int:income_id>/delete", methods=['POST'])
@login_required
def delete_income(income_id):
    income = Income.query.filter_by(id=income_id, user=current_user).first_or_404()
    db.session.delete(income)
    db.session.commit()
    return redirect(url_for('income'))

@app.route("/expenses/<int:expense_id>/delete", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user=current_user).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('expenses'))


@app.route("/account/update", methods=['GET', 'POST'])
@login_required
def update_account():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    form = LimitForm()
    if form.validate_on_submit():
        user.needs = form.needs.data
        user.wants = form.wants.data
        user.other = form.other.data
        db.session.commit()
        return redirect(url_for('account'))
    form.needs.data = user.needs
    form.wants.data = user.wants
    form.other.data = user.other
    return render_template('edit_profile.html',form=form)

