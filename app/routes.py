from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import FinancialAid, StudentRequest, User
from app.forms import DonorFeedbackForm, FinancialAidForm, LoginForm, RegistrationForm, SearchForm
from app.utils import requires_roles



@app.route('/role_selection')
def role_selection():
    return render_template('role_selection.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('role_selection'))

#admin side_____________________________________________________________________________-------------------------------------------
@app.route('/admin/dashboard')
@login_required
@requires_roles('admin')
def admin_dashboard():
    financial_aids = FinancialAidForm.query.all()
    return render_template('admin/dashboard.html', financial_aids=financial_aids)


@app.route('/admin/financial_aid/new', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')  # Ensure only admins can access this route
def create_financial_aid():
    form = FinancialAidForm()
    if form.validate_on_submit():
        financial_aid = FinancialAid(
            title=form.title.data,
            description=form.description.data,
            eligibility=form.eligibility.data,
            deadline=form.deadline.data,
            type=form.aid_type.data  # Include the type
        )
        db.session.add(financial_aid)
        db.session.commit()
        flash('Financial aid has been created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    # Render the template for creating financial aid with the form
    return render_template('admin/financial_aid_create.html', form=form)

    
@app.route('/admin/financial_aid/edit/<int:aid_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def edit_financial_aid(aid_id):
    financial_aid = FinancialAid.query.get_or_404(aid_id)
    form = FinancialAidForm(obj=financial_aid)
    if form.validate_on_submit():
        financial_aid.title = form.title.data
        financial_aid.description = form.description.data
        financial_aid.eligibility = form.eligibility.data
        financial_aid.deadline = form.deadline.data
        financial_aid.type = form.aid_type.data  # Update the type
        db.session.commit()
        flash('Financial aid has been updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_financial_aid.html', form=form, financial_aid=financial_aid)

@app.route('/admin/financial_aid/delete/<int:aid_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def delete_financial_aid(aid_id):
    financial_aid = FinancialAid.query.get_or_404(aid_id)

    if request.method == 'POST':
        db.session.delete(financial_aid)
        db.session.commit()
        flash('Financial aid has been deleted!', 'success')
        return redirect(url_for('admin_dashboard'))

    # For a GET request, show the confirmation page
    return render_template('admin/delete_financial_aid_confirmation.html', financial_aid=financial_aid)

@app.route('/financial_aid/<int:aid_id>')
def financial_aid_details(aid_id):
    financial_aid = FinancialAid.query.get_or_404(aid_id)
    return render_template('financial_aid_details.html', financial_aid=financial_aid)

#student Routes------------------------------------------------------------------------------------------------------------------
@app.route('/student/services')
@login_required
def student_services():
    return render_template('student/services.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit() or 'query' in request.args:
        query = form.query.data or request.args.get('query', '')
        financial_aids = FinancialAid.query.filter(FinancialAid.title.ilike(f'%{query}%')).all()
        return render_template('student/search_results.html', financial_aids=financial_aids, query=query)
    return render_template('student/search.html', form=form)

@app.route('/student/dashboard')
@login_required
@requires_roles('student')
def student_dashboard():
    # Fetch requests related to the logged-in student, including donor feedback if approved
    return render_template('student/dashboard.html', requests=StudentRequest)

#donor ___________________________________-----------------------------
@app.route('/donor/dashboard')
@login_required
@requires_roles('donor')
def donor_dashboard():
    student_requests = StudentRequest.query.filter_by(status='Pending').all()
    return render_template('donor/dashboard.html', student_requests=student_requests)

@app.route('/donor/view_request/<int:request_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('donor')
def view_student_request(request_id):
    student_request = StudentRequest.query.get_or_404(request_id)
    if request.method == 'POST':
        student_request.status = 'Approved'  # or 'Denied', based on button clicked
        db.session.commit()
        flash('Response recorded!', 'success')
        return redirect(url_for('donor_dashboard'))
    return render_template('donor/view_student_requests.html', student_request=student_request)

@app.route('/donor/approve/<int:request_id>')
@login_required
@requires_roles('donor')
def approve_request(request_id):
    request = StudentRequest.query.get_or_404(request_id)
    request.status = 'Approved'
    db.session.commit()
    # Logic to notify student goes here
    return redirect(url_for('donor_dashboard'))

@app.route('/donor/reject/<int:request_id>')
@login_required
@requires_roles('donor')
def reject_request(request_id):
    request = StudentRequest.query.get_or_404(request_id)
    request.status = 'Denied'
    db.session.commit()
    return redirect(url_for('donor_dashboard'))

@app.route('/donor/feedback/<int:request_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('donor')
def donor_feedback(request_id):
    form = DonorFeedbackForm()
    if form.validate_on_submit():
        # Logic to attach feedback to the student request and notify the student
        return redirect(url_for('donor_dashboard'))
    return render_template('donor/feedback.html', form=form)

