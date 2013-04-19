from flask.ext.wtf import Form, TextField, BooleanField, HiddenField, DateTimeField, PasswordField
from flask.ext.wtf import Required
from wtforms import validators as v
from wtforms.ext import dateutil

class BorrowForm(Form):
	user_id = HiddenField('borrower_id')
	lender_id = HiddenField('lender_id')
	product_id = HiddenField('product_id')
	start_date= TextField('start_date', validators = [Required()])
	end_date = TextField('end_date')

class SignUpForm(Form):
  	fname = TextField('fname', validators = [Required()])
  	lname = TextField('lname', validators = [Required()])
  	email = TextField('email',validators = [Required(),
                    v.Email(),
                    v.EqualTo('confirm_email',
                    message = "Emails must match")])
  	confirm_email = TextField('Repeat Email')
  	password = PasswordField('first_password',
                    validators = [Required(),
                    v.EqualTo('confirm_password',
                    message = 'Passwords must match')])
  	confirm_password = PasswordField('Repeat Password')