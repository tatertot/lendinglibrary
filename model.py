import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import ForeignKey
from flask.ext.wtf import Form, TextField, BooleanField, HiddenField, DateTimeField
from flask.ext.wtf import Required
import flask.ext.whooshalchemy as whooshalchemy


#This is SQLAlchemy's way of interacting with the db, creating a session
engine = create_engine("sqlite:///library.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):

    __tablename__ = "users" # tells SQLAlchemy  instance stored in table named users

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = False)
    fname = Column(String(64), nullable  = False)
    lname = Column(String(64), nullable  = True)
    phone_number = Column(String(15), nullable = True)
    password = Column(String(64), nullable  = False)
    city = Column(String(64), nullable  = True)
    state = Column(String(15), nullable  = True)
    zipcode = Column(String(15),nullable=True)

    # add methods for the Flask-login to work
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Category(Base):

	__tablename__ = "categories"

	id = Column(Integer, primary_key = True)
	category = Column(String(64), nullable  = False)


class Product(Base):

	__tablename__ = "products"

	id = Column(Integer, primary_key = True)
	name = Column(String(), nullable  = False)
	asin = Column(String(), nullable  = True)
	category_id = Column(Integer(), ForeignKey('categories.id'), nullable = True)
	default_photo = Column(String(), nullable  = True)
	custom_photo = Column(String(), nullable  = True)

class Library(Base):

	__tablename__ = "libraries"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer(), ForeignKey('users.id'), nullable = True)
	product_id = Column(Integer(), ForeignKey('products.id'), nullable = True)
	product_desc = Column(String(64), nullable  = True)
	status = Column(Integer(), nullable = False)
	user = relationship("User", backref=backref("libraries", order_by=id))
	product = relationship("Product", backref=backref("libraries", order_by=id))

# class Subscriber(Base):
# 	__tablename__ = "subscribers"

# 	id = Column(Integer, primary_key = True)
# 	user_id = Column(Integer(8), ForeignKey('users.id'), nullable = False)
# 	subscriber = Column(Integer(8), ForeignKey('users.id'), nullable = False)
# 	relationship_type = Column(String(64), nullable  = True)

class History(Base):#change table to Request?

	__tablename__ = "histories"

	id = Column(Integer, primary_key = True)
	lender_id = Column(Integer(), ForeignKey('users.id'), nullable = False)
	borrower_id = Column(Integer(), ForeignKey('users.id'), nullable = False)
	product_id = Column(Integer(), ForeignKey('products.id'), nullable = False)
	date_requested = Column(DateTime(),  default=datetime.datetime.now)
	date_wanted = Column(DateTime(),  nullable  = True)
	flexible = Column(Boolean(), default=False)
	date_borrowed = Column(DateTime(),  nullable  = True)
	date_returned_est = Column(DateTime(), nullable  = True)
	date_returned = Column(DateTime(), nullable  = True)
	declined = Column(Boolean(), default=False)

	lender = relationship("User", primaryjoin="History.lender_id==User.id")
	borrower = relationship("User", primaryjoin="History.borrower_id==User.id")
	product = relationship("Product", backref=backref("histories", order_by=id))
	# By using backref you can access the product table using product.histories


#lender is you, date wanted is in the future, declined is false, date borrowed is empty

class Comment(Base):

	__tablename__ = "comments"

	id = Column(Integer, primary_key = True)
	history_id = Column(Integer(), ForeignKey('histories.id'), nullable = False)
	comment = Column(String(), nullable  = False)
	date_sent = Column(DateTime(),  default=datetime.datetime.now)

class Notification(Base):

 	__tablename__ = "notifications"

 	id = Column(Integer, primary_key = True)
 	lender = Column(Integer(8), ForeignKey('users.id'), nullable = False)
 	borrower = Column(Integer(8), ForeignKey('users.id'), nullable = False)
 	message = Column(String(), nullable  = False)
 	date = Column(DateTime(),  default=datetime.datetime.now)

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()



