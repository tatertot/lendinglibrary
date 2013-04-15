from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String


#This is SQLAlchemy's way of interacting with the db, creating a session
engine = create_engine("postgres:///lendinglibrary.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,autocommit = False, autoflush = False))


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

# class Category(Base):

# 	__tablename__ = "categories"

# 	id = Column(Integer, primary_key = True)
# 	category = Column(String(64), nullable  = False)


class Product(Base):

	__tablename__ = "products"

	id = Column(Integer, primary_key = True)
	product = Column(String(64), nullable  = False)
	category_id = Column(Integer(8), ForeignKey('category.id'), nullable = True)
	default_photo = Column(String(128), nullable  = True)
	custom_photo = Column(String(128), nullable  = True)

class Library(Base):

	__tablename__ = "libraries"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer(8), ForeignKey('user.id'), nullable = True)
	product_id = Column(Integer(8), ForeignKey('product.id'), nullable = True)
	product_desc = Column(String(64), nullable  = False)
	status = Column(Integer(1), nullable = False)

# class Subscriber(Base):

# 	__tablename__ = "subscribers"

# 	id = Column(Integer, primary_key = True)
# 	user_id = Column(Integer(8), ForeignKey('user.id'), nullable = False)
# 	subscriber = Column(Integer(8), ForeignKey('user.id'), nullable = False)
# 	relationship_type = Column(String(64), nullable  = True)

class History(Base):

	__tablename__ = "histories"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer(8), ForeignKey('user.id'), nullable = False)
	product_id = Column(Integer(8), ForeignKey('product.id'), nullable = False)
	transaction = Column(String(12), nullable  = False)
	date_requested = Column(DateTime(),  default=datetime.datetime.now)
	date_borrowed = Column(DateTime(),  default=datetime.datetime.now)
	date_returned_est = Column(DateTime(), nullable  = True)
	date_returned = Column(DateTime(), nullable  = False)

# class Notification(Base):

#  	__tablename__ = "notifications"

#  	id = Column(Integer, primary_key = True)
#  	lender = Column(Integer(8), ForeignKey('user.id'), nullable = False)
#  	borrower = Column(Integer(8), ForeignKey('user.id'), nullable = False)
#  	message = Column(Text(), nullable  = False)
#  	date = Column(DateTime(),  default=datetime.datetime.now)

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()



