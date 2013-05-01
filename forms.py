from flask.ext.wtf import Form, TextField, BooleanField, HiddenField, DateTimeField, PasswordField
from flask.ext.wtf import Required
from wtforms import validators as v
from wtforms.ext import dateutil


class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    # remember_me = BooleanField('remember_me', default = False)


class SignUpForm(Form):
    fname = TextField('fname', validators = [Required()])
    lname = TextField('lname', validators = [Required()])
    mobile_number = TextField('mobile_number')
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


class AddProductForm(Form):
    user_id = HiddenField('user_id')
    name = TextField('name', validators = [Required()])
    asin = TextField('Amazon Id')
    category_id = TextField('Category')
    default_photo = TextField('Default Photo')
    custom_photo = TextField('Photo')


class BorrowForm(Form):
    user_id = HiddenField('borrower_id')
    lender_id = HiddenField('lender_id')
    product_id = HiddenField('product_id')
    start_date= TextField('start_date', validators = [Required()])
    end_date = TextField('end_date', validators = [Required()])

class SearchForm(Form):
    query = TextField('query', validators = [Required()])