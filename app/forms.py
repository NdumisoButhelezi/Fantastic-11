from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class FinancialAidForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    eligibility = TextAreaField('Eligibility Criteria', validators=[DataRequired()])
    deadline = StringField('Deadline', validators=[DataRequired()])  # Consider using a DateField
    aid_type = SelectField('Type', choices=[('financial_assistance', 'Financial Assistance'), ('bursary', 'Bursary'), ('scholarship', 'Scholarship'), ('grant', 'Grant')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class DonorFeedbackForm(FlaskForm):
    message = TextAreaField('Message to Student', validators=[DataRequired()])
    submit = SubmitField('Send')
 