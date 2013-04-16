import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import ForeignKey


#This is SQLAlchemy's way of interacting with the db, creating a session
# engine = create_engine("sqlite:///library.db", echo=False)
# session = scoped_session(sessionmaker(bind=engine,autocommit = False, autoflush = False))

ENGINE = None
Session = None

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):

    __tablename__ = "users" # tells SQLAlchemy  instance stored in table named users

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = False)
    fname = Column(String(64), nullable  = False)
    lname = Column(String(64), nullable  = False)
    password = Column(String(64), nullable  = False)
    city = Column(String(64), nullable  = False)
    state = Column(String(15), nullable  = False)
    zipcode = Column(String(15),nullable=True)

class Category(Base):

	__tablename__ = "categories"

	id = Column(Integer, primary_key = True)
	category = Column(String(64), nullable  = False)


class Product(Base):

	__tablename__ = "products"

	id = Column(Integer, primary_key = True)
	name = Column(String(64), nullable  = False)
	asin = Column(String(64), nullable  = True)
	category_id = Column(Integer(8), ForeignKey('categories.id'), nullable = True)
	default_photo = Column(String(128), nullable  = True)
	custom_photo = Column(String(128), nullable  = True)

class Library(Base):

	__tablename__ = "libraries"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer(8), ForeignKey('users.id'), nullable = True)
	product_id = Column(Integer(8), ForeignKey('products.id'), nullable = True)
	product_desc = Column(String(64), nullable  = True)
	status = Column(Integer(1), nullable = False)

# class Subscriber(Base):

# 	__tablename__ = "subscribers"

# 	id = Column(Integer, primary_key = True)
# 	user_id = Column(Integer(8), ForeignKey('users.id'), nullable = False)
# 	subscriber = Column(Integer(8), ForeignKey('users.id'), nullable = False)
# 	relationship_type = Column(String(64), nullable  = True)

class History(Base):

	__tablename__ = "histories"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer(8), ForeignKey('users.id'), nullable = False)
	product_id = Column(Integer(8), ForeignKey('products.id'), nullable = False)
	transaction = Column(String(12), nullable  = False)
	date_requested = Column(DateTime(),  default=datetime.datetime.now)
	date_borrowed = Column(DateTime(),  default=datetime.datetime.now)
	date_returned_est = Column(DateTime(), nullable  = True)
	date_returned = Column(DateTime(), nullable  = False)

# class Notification(Base):

#  	__tablename__ = "notifications"

#  	id = Column(Integer, primary_key = True)
#  	lender = Column(Integer(8), ForeignKey('users.id'), nullable = False)
#  	borrower = Column(Integer(8), ForeignKey('users.id'), nullable = False)
#  	message = Column(Text(), nullable  = False)
#  	date = Column(DateTime(),  default=datetime.datetime.now)

### End class declarations
def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///library.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()



