from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
import datetime
Base = declarative_base()
 
class Member(Base):
 	 __tablename__ = 'member'
 	 id = Column(Integer, primary_key=True)
 	 name = Column(String(255))
 	 address = Column(String(255))
 	 email = Column(String(255), unique=True)
 	 shoppingcart = relationship("shoppingcart", uselist=False, back_populates="member")
 	 photo = Column(String(255), unique=True)
 	 password_hash = Column(String(255))
 	 order = relationship("Order", back_populates="member")

 	 def hash_password(self, password):
 	 	self.password_hash = pwd_context.encrypt(password)


 	 def set_photo(self, photo):
 	 	self.photo = photo

 	 def verify_password(self, password):
 	 	return pwd_context.verify(password, self.password_hash)

	

class Post(Base):
 	__tablename__ = 'status'
 	id = Column(Integer, primary_key=True)
	name = Column(Integer)
	description = Column(String(255))


class shoppingcart(Base):
	__tablename__ = 'shoppingcart'
	id = (Column(Integer, primary_key=True))
	memberr_id = Column(Integer, ForeignKey('member.id'))
	member = relationship("Member", back_populates="shoppingcart")
	products = relationship("ShoppingcartAssociation", back_populates="shoppingcart")


class OrdersAssociation(Base):
    __tablename__ = 'OrdersAssociation'
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product_qty = Column(Integer)
    product = relationship("product", back_populates="order")
    order = relationship("Order", back_populates="products")

class ShoppingcartAssociation(Base):
    __tablename__ = 'ShoppingcartAssociation'
    shopping_cart_id = Column(Integer, ForeignKey('shoppingcart.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer)
    product = relationship("product", back_populates="shoppingcart")
    shoppingcart = relationship("shoppingcart", back_populates="products")

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    total = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    confirmation = Column(String, unique=True)
    products = relationship("OrdersAssociation", back_populates="order")
    member_id = Column(Integer, ForeignKey('member.id'))
    member = relationship("Member", back_populates="order")    

	

class product(Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	photo = Column(String)
	price = Column(Float)
	order = relationship("OrdersAssociation", back_populates="product")
	shoppingcart = relationship("ShoppingcartAssociation", back_populates="product")









engine = create_engine('sqlite:///welcome_to_you.db')

Base.metadata.create_all(engine)






