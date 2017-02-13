from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
Base = declarative_base()
 
class User(Base):
 	__tablename__ = 'user'
	id = (Column(Integer, primary_key=True))
	name = Column(String(60))
	email= Column(String(60))
	password = Column(String(60))
	weight = Column(String(60))
	height = Column(String(60))

class Post(Base):
 	__tablename__ = 'status'
	id = Column(Integer, primary_key=True)
	name = Column(Integer)
	description = Column(String(255))


class shoppingcart(Base):
	__tablename__ = 'shoppingcart'
	id = (Column(Integer, primary_key=True))
	name = Column(String(60))
	email= Column(String(60))
	password = Column(String(60))
	credit_card =  Column(String(60))


class product(Base):
	__tablename__ = 'name'
	id = (Column(Integer, primary_key=True))
	name = Column(String(60))
	type_of_product = Column(String(60))
	quality = Column(String(60))








engine = create_engine('sqlite:///welcome_to_you.db')

Base.metadata.create_all(engine)






