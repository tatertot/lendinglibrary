from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required

class BorrowForm(Form):
	# #get borrower id
	# borrower_id = HiddenField('borrower_id')
	# #get lender id
	# lender_id = HiddenField('lender_id')
	# #get product id
	# product_id = HiddenField('product_id')
	#get date producted is wanted
	date_wanted = TextField('start_date')
	#get date producted is going to be returned
	date_wanted = TextField('end_date')



